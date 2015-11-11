import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scrapers', 'amzn'))

import re
import json
import uuid

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.errors import record_trade_api_error


class EbayItemAction(object):
    """ebay item actions
        Trading api
    """
    
    amazon_item = None
    ebay_store = None
    ebay_item = None

    __maxed_out = False

    def __init__(self, *a, **kw):
        if 'ebay_store' not in kw:
            raise KeyError('ebay_store not found')
        self.ebay_store = kw['ebay_store']
        if 'amazon_item' in kw:
            self.amazon_item = kw['amazon_item']
        if 'ebay_item' in kw:
            self.ebay_item = kw['ebay_item']

    def generate_upload_picture_obj(self, picture_url):
        picture_obj = amazonmws_settings.EBAY_UPLOAD_SITE_HOSTED_PICTURE;
        picture_obj['ExternalPictureURL'] = picture_url
        return picture_obj


    def generate_add_item_obj(self, category_id, picture_urls, price, quantity):
        title = re.sub(r'([^\s\w\(\)\[\]\-\']|_)+', ' ', self.amazon_item.title) + u', Fast Shipping'

        item = amazonmws_settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['Title'] = title[:80] # limited to 80 characters
        item['Item']['Description'] = "<![CDATA[\n" + amazonmws_utils.apply_ebay_listing_template(self.amazon_item, self.ebay_store) + "\n]]>"
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['PictureDetails']['PictureURL'] = picture_urls
        item['Item']['StartPrice'] = price
        item['Item']['Quantity'] = quantity
        item['Item']['PayPalEmailAddress'] = self.ebay_store.paypal_username
        item['Item']['UseTaxTable'] = self.ebay_store.use_salestax_table
        return item

    def generate_revise_inventory_status_obj(self, price=None, quantity=None):
        if price == None and quantity == None:
            return None

        item = amazonmws_settings.EBAY_REVISE_INVENTORY_STATUS_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['InventoryStatus']['ItemID'] = self.ebay_item.ebid
        if quantity != None:
            item['InventoryStatus']['Quantity'] = quantity
        else:
            item['InventoryStatus'].pop("Quantity", None)
        if price != None:
            item['InventoryStatus']['StartPrice'] = price
        else:
            item['InventoryStatus'].pop("StartPrice", None)
        return item

    def upload_pictures(self, pictures):
        """upload pictures to ebay hosted server
            Trading API - 'UploadSiteHostedPictures'
        """
        picture_urls = []
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
        except ConnectionError, e:
            logger.exception("[ASIN:%s] %s" % (self.amazon_item.asin, str(e)))
            return picture_urls

        for picture in pictures:
            picture_obj = self.generate_upload_picture_obj(picture.picture_url)
            try:
                response = api.execute('UploadSiteHostedPictures', picture_obj)
                data = response.reply # ebaysdk.response.ResponseDataObject
                if not data.Ack:
                    logger.error("[%s|ASIN:%s] Ack not found" % (self.ebay_store.username, self.amazon_item.asin))
                    record_trade_api_error(
                        picture_obj['MessageID'], 
                        u'UploadSiteHostedPictures', 
                        amazonmws_utils.dict_to_json_string(picture_obj),
                        api.response.json(), 
                        asin=self.amazon_item.asin
                    )
                    continue
                if data.Ack == "Success":
                    picture_urls.append(data.SiteHostedPictureDetails.FullURL)
                    logger.info("[ASIN:%s] picture url - %s" % (self.amazon_item.asin, data.SiteHostedPictureDetails.FullURL))

                # on minor Waring
                # error code 21916790: Pictures are at least 1000 pixels on the longest side
                # error code 21916791: The image be 90 or greater quality for JPG compression
                elif data.Ack == "Warning":
                    if amazonmws_utils.to_string(data.Errors.ErrorCode) == "21916790" or amazonmws_utils.to_string(data.Errors.ErrorCode) == "21916791":

                        picture_urls.append(data.SiteHostedPictureDetails.FullURL)
                        logger.warning("[ASIN:%s] picture url - %s : warning - %s" % (self.amazon_item.asin, data.SiteHostedPictureDetails.FullURL, data.Errors.LongMessage))
                    else:
                        logger.warning("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                        record_trade_api_error(
                            picture_obj['MessageID'], 
                            u'UploadSiteHostedPictures', 
                            amazonmws_utils.dict_to_json_string(picture_obj),
                            api.response.json(), 
                            asin=self.amazon_item.asin
                        )
                        continue
                else:
                    logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                    record_trade_api_error(
                        picture_obj['MessageID'], 
                        u'UploadSiteHostedPictures', 
                        amazonmws_utils.dict_to_json_string(picture_obj),
                        api.response.json(), 
                        asin=self.amazon_item.asin
                    )
                    continue
            except ConnectionError, e:
                logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
                continue
        return picture_urls

    def add_item(self, category_id, picture_urls, eb_price, quantity):
        """upload item to ebay store
            Trading API - 'AddFixedPriceItem'
        """
        ret = False
        item_obj = self.generate_add_item_obj(category_id, picture_urls, eb_price, quantity)

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('AddFixedPriceItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s] Ack not found" % (self.ebay_store.username, self.amazon_item.asin))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
            if data.Ack == "Success":
                ret = amazonmws_utils.str_to_unicode(data.ItemID)
            elif data.Ack == "Warning":
                logger.warning("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
                ret = amazonmws_utils.str_to_unicode(data.ItemID)
            elif data.Ack == "Failure":
                if amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919188':
                    self.__maxed_out = True
                logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
            else:
                logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
        except ConnectionError, e:
            if "Code: 21919188," in str(e):
                self.__maxed_out = True
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
        return ret

    def restock_item(self, eb_price, quantity):
        ret = False
        item_obj = self.generate_revise_inventory_status_obj(eb_price, quantity)

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('ReviseInventoryStatus', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s|EBID:%s] Ack not found" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'ReviseInventoryStatus', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
            if data.Ack == "Success":
                ret = True
            elif data.Ack == "Warning":
                if amazonmws_utils.to_string(data.Errors.ErrorCode) == "21919189":
                    logger.warning("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, data.Errors.LongMessage))
                    ret = True
                else:
                    logger.warning("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                    record_trade_api_error(
                        item_obj['MessageID'], 
                        u'ReviseInventoryStatus', 
                        utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        asin=self.ebay_item.asin,
                        ebid=self.ebay_item.ebid
                    )
            elif data.Ack == "Failure":
                if amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919188':
                    self.__maxed_out = True
                logger.error("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'ReviseInventoryStatus', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
            else:
                logger.error("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'ReviseInventoryStatus', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
        except ConnectionError, e:
            if "Code: 21919188," in str(e):
                self.__maxed_out = True
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret

    def maxed_out(self):
        return self.__maxed_out

