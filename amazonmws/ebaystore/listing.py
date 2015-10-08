import sys, os, traceback

sys.path.append('%s/../../' % os.path.dirname(__file__))

from os.path import basename
import json
import uuid
import datetime
import operator

from decimal import Decimal

from storm.exceptions import StormError
from storm.expr import Desc

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from amazonmws import utils
from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, Task
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

class FromAmazonToEbay(object):

    amazon_item = None
    quantity = 20

    TASK_ID = Task.ebay_task_listing

    reached_ebay_limit = False

    def __init__(self, amazon_item):
        self.amazon_item = amazon_item
        self.quantity = settings.EBAY_ITEM_DEFAULT_QUANTITY
        logger.addFilter(StaticFieldFilter(get_logger_name(), Task.get_name(self.TASK_ID)))
        pass

    def list(self):
        category_id = self.__find_ebay_category_id()

        if category_id < 0:
            return False

        listing_price = calculate_profitable_price(self.amazon_item.price)

        if listing_price < 0:
            return False

        item_picture_urls = self.__get_item_picture_urls()

        item_obj = self.__generate_ebay_add_item_obj(category_id, listing_price, item_picture_urls)
        
        # let's take this verified part off... not necessary...
        # verified = self.__verify_add_item(item_obj)        
        # if verified:
            # self.__add_item(item_obj, category_id, listing_price)
        # else:
            # return False

        self.__add_item(item_obj, category_id, listing_price)

        return True

    def __generate_ebay_add_item_obj(self, category_id, listing_price, picture_urls):

        title = self.amazon_item.title + u', Fast Shipping'

        item = settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['Title'] = title[:80] # limited to 80 characters
        item['Item']['Description'] = "<![CDATA[\n" + utils.apply_ebay_listing_template(self.amazon_item.description) + "\n]]>"
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['PictureDetails']['PictureURL'] = picture_urls
        item['Item']['StartPrice'] = listing_price
        item['Item']['Quantity'] = self.quantity

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
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)

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
                            api.request.json(),
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
                        api.request.json(),
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

    def __find_ebay_category_id(self):
        desired_category_id = -1

        try:
            api = Finding(debug=False, warnings=True)

            api_request = {
                'keywords': self.amazon_item.title,
                'itemFilter': [
                    # {
                    #     'name': 'Condition',
                    #     'value': 'Used'
                    # },
                    {
                        'name': 'LocatedIn',
                        'value': 'US'
                    },
                ],
                'sortOrder': 'BestMatch',
                'paginationInput': {
                    'entriesPerPage': 50,
                    'pageNumber': 1,
                },
            }

            api.execute('findItemsAdvanced', api_request)

            category_set = {}

            if api.response.content:
                data = json.loads(api.response.json())

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):

                    # print json.dumps(data, indent=4, sort_keys=True)

                    if int(data['searchResult']['_count']) > 0:
                        for searched_item in data['searchResult']['item']:
                            try:
                                searched_category_id = searched_item['primaryCategory']['categoryId']

                                category_set[searched_category_id] = category_set[searched_category_id] + 1 if searched_category_id in category_set else 1
                            
                            except KeyError:
                                logger.exception('Category id key not found')
                                continue
            else:
                logger.error("[" + self.amazon_item.title + "] " + "findItemsAdvanced error - no content on response")

            if len(category_set) < 1:
                logger.error("[" + self.amazon_item.title + "] " + "Unable to find ebay category for this item")
            else:
                # get most searched caregory id
                desired_category_id = max(category_set.iteritems(), key=operator.itemgetter(1))[0]

        except ConnectionError, e:
            logger.exception("[" + self.amazon_item.asin + "] " + str(e))

        if desired_category_id < 0:
            # store in seperate database
            logger.error("[ASIN:" + self.amazon_item.asin + "] " + "Unable to find primary category at ebay")

        return desired_category_id

    # comment out this code for now...
    # def __verify_add_item(self, item_obj):
    #     ret = False

    #     try:
    #         api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
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
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
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
                        api.request.json(),
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
                        api.request.json(),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )
                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        api.request.json(),
                        api.response.json(), 
                        amazon_item_id=self.amazon_item.id,
                        asin=self.amazon_item.asin
                    )

        except ConnectionError, e:
            if "Code: 21919188," in str(e) or "Code: 240," in str(e):
                self.reached_ebay_limit = True
            
            logger.exception("[ASIN:" + self.amazon_item.asin  + "] " + str(e))

        return ret

    def __store_ebay_item(self, ebay_item_id, category_id, price):
        try:
            ebay_item = EbayItem()
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

    scraper_id = None
    min_review_count = 10

    def __init__(self, scraper_id=None):
        self.scraper_id = scraper_id

    def run(self):
        items = self.__filter_items()

        count = 0

        for item in items:
            to_ebay = FromAmazonToEbay(item)
            listed = to_ebay.list()

            if listed:
                count += 1

            if to_ebay.reached_ebay_limit:
                logger.error('REACHED EBAY ITEM LIST LIMITATION')
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
            if self.scraper_id:
                filtered_items = StormStore.find(AmazonItem,
                    ScraperAmazonItem.amazon_item_id == AmazonItem.id,
                    ScraperAmazonItem.scraper_id == self.scraper_id,
                    AmazonItem.status == AmazonItem.STATUS_ACTIVE,
                    AmazonItem.review_count >= self.min_review_count).order_by(Desc(AmazonItem.avg_rating), Desc(AmazonItem.review_count))
            
            else:
                filtered_items = StormStore.find(AmazonItem, AmazonItem.status == AmazonItem.STATUS_ACTIVE)

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
        num_new_items = 0

        for item in filtered_items:
            already_exists = False
            try:
                already_exists = StormStore.find(EbayItem, EbayItem.amazon_item_id == item.id).one()
            
            except StormError:
                logger.exception('Error on finding item in ebay_items table')

            if not already_exists:
                # print 'New item!'
                num_new_items += 1
                result.append(item)

        logger.info("[" + basename(__file__) + "] " + "Number of new items to list on ebay: " + str(num_new_items) + " items")

        return result

def calculate_profitable_price(amazon_item_price, margin_percentage=3):
    """i.e. with 3 percent margin
        
        ((cost * 1.10 * 1.09 + .20) * 1.029 + .30) * 1.03

        - * 1.10:   10 percent sales tax - also changed on amazon.com
        - * 1.09:   9 percent final value fee charged by ebay
        - + .20:    20 cent listing fee charged by ebay
        - * 1.029:  2.9 percent transaction fee charged by paypal
        - + .30:    30 cent transaction fee by paypal
        - * 1.03:   and my 3 percent margin
    """
    
    profitable_price = -1

    try:
        profitable_price = Decimal(((float(amazon_item_price) * 1.10 * 1.09 + 0.20) * 1.029 + 0.30) * (1.00 + float(margin_percentage) / 100)).quantize(Decimal('1.00'))

    except Exception:
        logger.exception("Unable to calculate profitable price")

    return profitable_price

if __name__ == "__main__":
    handler = ListingHandler(Scraper.amazon_keywords_kidscustume)
    handler.run()
