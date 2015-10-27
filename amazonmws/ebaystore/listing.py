import sys, os, traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from os.path import basename
import json
import uuid
import datetime
import re

from decimal import Decimal

from storm.exceptions import StormError
from storm.expr import Desc

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

import RAKE

from amazonmws import utils
from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, EbayItem, Task, ItemQuantityHistory, EbayStore, LookupAmazonItem, Lookup, LookupOwnership
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.ebayapi.request_objects import generate_revise_inventory_status_obj

class FromAmazonToEbay(object):
    ebay_store = None
    amazon_item = None
    ebay_item = None
    quantity = 20

    TASK_ID = Task.ebay_task_listing

    reached_ebay_limit = False

    def __init__(self, ebay_store, amazon_item, ebay_item=None):
        self.ebay_store = ebay_store
        self.amazon_item = amazon_item
        self.ebay_item = ebay_item
        self.quantity = settings.EBAY_ITEM_DEFAULT_QUANTITY
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))

    def list(self):
        if self.ebay_item:
            """use ReviseInventoryStatus to restock item on ebay
            """
            return self.__restock_ebay_item()

        else:
            if self.amazon_item.ebay_category_id and self.amazon_item.ebay_category_id > 0:
                category_id = self.amazon_item.ebay_category_id
            else:
                logger.error("[ASIN: " + self.amazon_item.asin + "] " + "No ebay category found")
                return False

            listing_price = utils.calculate_profitable_price(self.amazon_item.price,
                self.ebay_store.margin_percentage,
                self.ebay_store.margin_max_dollar,
                not self.ebay_store.use_salestax_table)

            if listing_price < 0:
                logger.error("[ASIN: " + self.amazon_item.asin + "] " + "No listing price available")
                return False

            item_picture_urls = self.__get_item_picture_urls()

            if len(item_picture_urls) < 1:
                logger.error("[ASIN: " + self.amazon_item.asin + "] " + "No item pictures available")
                return False

            item_obj = self.__generate_ebay_add_item_obj(category_id, listing_price, item_picture_urls)
            
            # let's take this verified part off... not necessary...
            # verified = self.__verify_add_item(item_obj)        
            # if verified:
                # self.__add_item(item_obj, category_id, listing_price)
            # else:
                # return False

            return self.__add_item(item_obj, category_id, listing_price)

    def __restock_ebay_item(self):
        ret = False

        item_obj = generate_revise_inventory_status_obj(self.ebay_item, self.ebay_item.price, settings.EBAY_ITEM_DEFAULT_QUANTITY)

        try:
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('ReviseInventoryStatus', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True
                    self.__record_ebay_item_quantity_history(settings.EBAY_ITEM_DEFAULT_QUANTITY)

                elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

                    if data['Errors']['ErrorCode'] == "21919189" or data['Errors']['ErrorCode'] == 21919189:
                        ret = True
                        logger.warning("[EBID: " + self.ebay_item.ebid + "] " + data['Errors']['  LongMessage'])
                        self.__record_ebay_item_quantity_history(settings.EBAY_ITEM_DEFAULT_QUANTITY)
                    else:
                        logger.warning(api.response.json())
                        record_trade_api_error(
                            item_obj['MessageID'], 
                            u'ReviseInventoryStatus', 
                            utils.dict_to_json_string(item_obj),
                            api.response.json(), 
                            amazon_item_id=self.ebay_item.amazon_item_id,
                            asin=self.ebay_item.asin,
                            ebay_item_id=self.ebay_item.id,
                            ebid=self.ebay_item.ebid
                        )

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'ReviseInventoryStatus', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.ebay_item.amazon_item_id,
                        asin=self.ebay_item.asin,
                        ebay_item_id=self.ebay_item.id,
                        ebid=self.ebay_item.ebid
                    )

        except ConnectionError, e:
            logger.exception("[EBID:" + self.ebay_item.ebid + "] " + str(e))

        return ret

    def __record_ebay_item_quantity_history(self, quantity):
        try:
            self.ebay_item.status = settings.STATUS_ACTIVE
            StormStore.add(self.ebay_item)

            quantity_history = ItemQuantityHistory()
            quantity_history.amazon_item_id = self.ebay_item.amazon_item_id
            quantity_history.asin = self.ebay_item.asin
            quantity_history.ebay_item_id = self.ebay_item.id
            quantity_history.ebid = self.ebay_item.ebid
            quantity_history.quantity = quantity
            quantity_history.created_at = datetime.datetime.now()
            quantity_history.updated_at = datetime.datetime.now()
            StormStore.add(quantity_history)
            StormStore.commit()
            return True

        except StormError, e:
            logger.exception("[EBID: " + self.ebay_item.ebid + "] " + str(e))
            StormStore.rollback()
            return False

    def __generate_ebay_add_item_obj(self, category_id, listing_price, picture_urls):

        title = re.sub(r'([^\s\w\(\)\[\]\-\']|_)+', ' ', self.amazon_item.title) + u', Fast Shipping'

        item = settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['Title'] = title[:80] # limited to 80 characters
        item['Item']['Description'] = "<![CDATA[\n" + utils.apply_ebay_listing_template(self.amazon_item.title,
            self.amazon_item.description,
            self.amazon_item.features,
            self.ebay_store.policy_shipping,
            self.ebay_store.policy_payment,
            self.ebay_store.policy_return,
            self.ebay_store.item_description_template) + "\n]]>"
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['PictureDetails']['PictureURL'] = picture_urls
        item['Item']['StartPrice'] = listing_price
        item['Item']['Quantity'] = self.quantity
        item['Item']['PayPalEmailAddress'] = self.ebay_store.paypal_username
        item['Item']['UseTaxTable'] = self.ebay_store.use_salestax_table

        return item

    def __store_internally_ebay_image_url(self, item_picture, ebay_image_url):
        ret = False

        item_picture.ebay_picture_url = ebay_image_url

        try:
            StormStore.add(item_picture)
            StormStore.commit()
            ret = True

        except StormError, e:
            StormStore.rollback()
            logger.exception("[" + ebay_image_url + "] " + "Image uploaded to ebay, but unable to store information in amazon_item_pictures table")
            
        return ret

    def __upload_pictures_to_ebay(self, item_pictures):

        picture_urls = []

        try:
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))

        except ConnectionError, e:
            logger.exception("[ASIN:" + self.amazon_item.asin + "] " + str(e))
            return picture_urls

        for item_picture in item_pictures:
            picture_obj = settings.EBAY_UPLOAD_SITE_HOSTED_PICTURE;
            picture_obj['ExternalPictureURL'] = item_picture.converted_picture_url

            try:
                api.execute('UploadSiteHostedPictures', picture_obj)

            except ConnectionError, e:
                logger.exception("[ASIN:" + self.amazon_item.asin + "] " + str(e))
                continue

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):

                    is_stored = self.__store_internally_ebay_image_url(item_picture, data['SiteHostedPictureDetails']['FullURL'])

                    if not is_stored:
                        continue

                    picture_urls.append(data['SiteHostedPictureDetails']['FullURL'])

                # on minor Waring
                # error code 21916790: Pictures are at least 1000 pixels on the longest side
                # error code 21916791: The image be 90 or greater quality for JPG compression
                elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

                    if (data['Errors']['ErrorCode'] == "21916790") or (data['Errors']['ErrorCode'] == "21916791"):

                        is_stored = self.__store_internally_ebay_image_url(item_picture, data['SiteHostedPictureDetails']['FullURL'])

                        if not is_stored:
                            continue

                        picture_urls.append(data['SiteHostedPictureDetails']['FullURL'])
                        logger.info(item_picture.converted_picture_url + ": " + data['Errors']['LongMessage'])
                    else:
                        logger.warning(api.response.json())
                        record_trade_api_error(
                            picture_obj['MessageID'], 
                            u'UploadSiteHostedPictures', 
                            utils.dict_to_json_string(picture_obj),
                            api.response.json(), 
                            amazon_item_id=self.amazon_item.id,
                            asin=self.amazon_item.asin
                        )
                        continue
                
                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        picture_obj['MessageID'], 
                        u'UploadSiteHostedPictures', 
                        utils.dict_to_json_string(picture_obj),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )
                    continue    

            else:
                logger.error("[" + item_picture.converted_picture_url + "] " + "UploadSiteHostedPictures error - no response content")
                continue

        return picture_urls

    def __get_item_picture_urls(self):

        item_pictures = StormStore.find(AmazonItemPicture, AmazonItemPicture.amazon_item_id == self.amazon_item.id)

        if item_pictures.count() < 1:
            logger.error("[ASIN:" + self.amazon_item.asin + "] " + "No item pictures found in amazon_item_pictures table")
            return []

        return self.__upload_pictures_to_ebay(item_pictures)


    # comment out this code for now...
    # def __verify_add_item(self, item_obj):
    #     ret = False

    #     try:
    #         token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
    #         api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
    #         api.execute('VerifyAddFixedPriceItem', item_obj)

    #         if api.response.content:
    #             data = json.loads(api.response.json())

    #             # print json.dumps(data, indent=4, sort_keys=True)

    #             if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
    #                 ret = True

    #             # error code 21917236: Funds from your sales will be unavailable and show as pending in your PayPal account for a period of time.
    #             elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

    #                 if data['Errors']['ErrorCode'] == 21917236:
    #                     ret = True
                
    #             else:
    #                 self.__log_on_error(unicode(api.response.json()), u'VerifyAddFixedPriceItem')

    #     except ConnectionError, e:
    #         self.__log_on_error(e, unicode(e.response.dict()), u'VerifyAddFixedPriceItem')

    #     return ret

    def __add_item(self, item_obj, category_id, price):
        ret = False

        try:
            token = None if settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
            api.execute('AddFixedPriceItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    
                    ret = True
                    self.__store_ebay_item(data['ItemID'], category_id, price)

                elif ('ack' in data and data['ack'] == "Warning") or ('Ack' in data and data['Ack'] == "Warning"):

                    logger.warning(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )

                    ret = True
                    self.__store_ebay_item(data['ItemID'], category_id, price)

                elif ('ack' in data and data['ack'] == "Failure") or ('Ack' in data and data['Ack'] == "Failure"):

                    if data['Errors']['ErrorCode'] == 21919188:
                        self.reached_ebay_limit = True

                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )
                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )

        except ConnectionError, e:
            if "Code: 21919188," in str(e):
                self.reached_ebay_limit = True
            
            logger.exception("[ASIN:" + self.amazon_item.asin  + "] " + str(e))

        return ret

    def __store_ebay_item(self, ebay_item_id, category_id, price):
        try:
            ebay_item = EbayItem()
            ebay_item.ebay_store_id = self.ebay_store.id
            ebay_item.amazon_item_id = self.amazon_item.id
            ebay_item.asin = self.amazon_item.asin
            ebay_item.ebid = ebay_item_id
            ebay_item.ebay_category_id = category_id
            ebay_item.ebay_category_id = category_id
            ebay_item.eb_price = price
            ebay_item.quantity = self.quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.created_at = datetime.datetime.now()
            ebay_item.updated_at = datetime.datetime.now()

            StormStore.add(ebay_item)
            StormStore.commit()

        except StormError:
            logger.exception("Listed at ebay, but unable to store information in ebay_items table")


class ListingHandler(object):

    ebay_store = None
    min_review_count = 10
    max_num_listing = None

    def __init__(self, ebay_store, max_num_listing=None):
        self.ebay_store = ebay_store
        self.max_num_listing = max_num_listing

    def run(self):
        items = self.__filter_items()
        count = 0

        for (amazon_item, ebay_item) in items:
            to_ebay = FromAmazonToEbay(self.ebay_store, amazon_item, ebay_item)
            listed = to_ebay.list()

            if listed:
                count += 1

            if isinstance(self.max_num_listing, int) and count > self.max_num_listing:
                logger.error("[" + self.ebay_store.username + "] " + "STOP LISTING - REACHED MAX NUMBER OF LISTING - " + str(self.max_num_listing))
                break

            if to_ebay.reached_ebay_limit:
                logger.error("[" + self.ebay_store.username + "] " + "STOP LISTING - REACHED EBAY ITEM LIST LIMITATION")
                break


        return True

    def __filter_items(self):
        """filter amazon item by:
            - amazon active item
            - item which has not listed at ebay store
            - scraper (if applicable)

            return type: list
        """

        result = []
        try:
            filtered_items = StormStore.find(AmazonItem,
                LookupAmazonItem.amazon_item_id == AmazonItem.id,
                LookupOwnership.lookup_id == LookupAmazonItem.lookup_id,
                LookupOwnership.ebay_store_id == self.ebay_store.id,
                AmazonItem.status == AmazonItem.STATUS_ACTIVE,
                AmazonItem.review_count >= self.min_review_count).order_by(Desc(AmazonItem.avg_rating), Desc(AmazonItem.review_count))
        except StormError:
            logger.exception('Unable to filter amazon items')

        # workaround solution - stupid but storm doesn't support outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_items = 0

        for amazon_item in filtered_items:
            ebay_item = False
            try:
                ebay_item = StormStore.find(EbayItem, 
                    EbayItem.amazon_item_id == amazon_item.id,
                    EbayItem.ebay_store_id == self.ebay_store.id).one()
            
            except StormError:
                logger.exception("[ASIN:" + amazon_item.asin + "] " + "Error on finding item in ebay_items table")
                continue

            if not ebay_item:
                num_items += 1
                item_set = (amazon_item, None)
                result.append(item_set)
            
            elif ebay_item.status == EbayItem.STATUS_OUT_OF_STOCK:
                """add OOS ebay item - need to restock to ebay because it's been restocked on amazon!
                """
                num_items += 1
                item_set = (amazon_item, ebay_item)
                result.append(item_set)

        logger.info("[" + self.ebay_store.username + "] " + "Number of items to list on ebay: " + str(num_items) + " items")

        return result


if __name__ == "__main__":
    ebay_stores = StormStore.find(EbayStore)

    if ebay_stores.count() > 0:
        for ebay_store in ebay_stores:
            handler = ListingHandler(ebay_store)
            handler.run()
