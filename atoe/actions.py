import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scrapers', 'amzn'))

import re
import json
import uuid
import operator

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.errors import record_trade_api_error, record_ebay_category_error


class EbayItemAction(object):
    """ebay item actions
        Trading api
    """
    
    amazon_item = None
    ebay_store = None
    ebay_item = None

    __maxed_out = False

    def __init__(self, *a, **kw):
        if 'ebay_store' in kw:
            self.ebay_store = kw['ebay_store']
        if 'amazon_item' in kw:
            self.amazon_item = kw['amazon_item']
        if 'ebay_item' in kw:
            self.ebay_item = kw['ebay_item']
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe'))

    def generate_upload_picture_obj(self, picture_url):
        picture_obj = amazonmws_settings.EBAY_UPLOAD_SITE_HOSTED_PICTURE;
        picture_obj['ExternalPictureURL'] = picture_url
        return picture_obj

    def generate_add_item_obj(self, category_id, picture_urls, price, quantity):
        item = amazonmws_settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['SKU'] = self.amazon_item.asin
        item['Item']['Title'] = amazonmws_utils.generate_ebay_item_title(self.amazon_item.title)
        item['Item']['Description'] = "<![CDATA[\n" + amazonmws_utils.apply_ebay_listing_template(self.amazon_item, self.ebay_store) + "\n]]>"
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['PictureDetails']['PictureURL'] = picture_urls[:12] # max 12 pictures allowed
        item['Item']['StartPrice'] = price
        item['Item']['Quantity'] = quantity
        item['Item']['PayPalEmailAddress'] = self.ebay_store.paypal_username
        item['Item']['UseTaxTable'] = self.ebay_store.use_salestax_table
        if not self.ebay_store.returns_accepted:
            item['Item']['ReturnPolicy']['ReturnsAcceptedOption'] = 'ReturnsNotAccepted'
        if self.amazon_item.brand_name:
            mpn = amazonmws_utils.generate_mpn()
            
            item['Item']['ProductListingDetails']['BrandMPN']['Brand'] = self.amazon_item.brand_name
            item['Item']['ProductListingDetails']['BrandMPN']['MPN'] = mpn
            item['Item']['ProductListingDetails']['UPC'] = amazonmws_utils.generate_upc()
            item['Item']['ItemSpecifics']['NameValueList'] = [
                {
                    'Name': 'Brand',
                    'Value': self.amazon_item.brand_name,
                },
                {
                    'Name': 'MPN',
                    'Value': mpn,
                },
            ]
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

    def generate_end_item_obj(self):
        item = amazonmws_settings.EBAY_END_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['ItemID'] = self.ebay_item.ebid
        item['EndingReason'] = 'NotAvailable'
        return item

    def upload_pictures(self, pictures):
        """upload pictures to ebay hosted server
            Trading API - 'UploadSiteHostedPictures'
        """
        picture_urls = []
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
        except ConnectionError as e:
            logger.exception("[ASIN:%s] %s" % (self.amazon_item.asin, str(e)))
            return picture_urls
        except Exception as e:
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
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
            except ConnectionError as e:
                logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
                continue
            except Exception as e:
                logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
                continue
        return picture_urls

    def add_item(self, category_id, picture_urls, eb_price, quantity, content_revised=False):
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
                if amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919188': # reached your selling limit
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
        except ConnectionError as e:
            if "Code: 21919188," in str(e): # reached your selling limit
                self.__maxed_out = True
            elif "Code: 240," in str(e): # The title may contain improper words
                logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
            elif "Code: 107," in str(e): # Category is not valid
                if not content_revised: # you may try one more time with revised category id
                    category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in self.amazon_item.category]
                    category_info = self.find_category('%s %s' % (category_route[0], category_route[-1]))
                    if category_info and amazonmws_utils.str_to_unicode(category_info[0]) != category_id:
                        revised_category_id = amazonmws_utils.str_to_unicode(category_info[0])
                        # new category_id. Update db!
                        cmap = AtoECategoryMapModelManager.fetch_one(self.amazon_item.category)
                        if cmap and AtoECategoryMapModelManager.update(cmap, 
                            ebay_category_id=revised_category_id,
                            ebay_category_name=category_info[1]):
                            content_revised = True
                            logger.info("[%s|ASIN:%s] ebay category has been revised from %s to %s - amazon category - %s" % (self.ebay_store.username, self.amazon_item.asin, category_id, revised_category_id, self.amazon_item.category))
                            return self.add_item(revised_category_id, picture_urls, eb_price, quantity, content_revised)
                    # unable to revise category id, then just record the error
                    record_ebay_category_error(
                        item_obj['MessageID'], 
                        self.amazon_item.asin,
                        self.amazon_item.category,
                        category_id,
                        amazonmws_utils.dict_to_json_string(item_obj),
                    )
                else: # revised, but still get 107 error, then just record the error
                    record_ebay_category_error(
                        item_obj['MessageID'], 
                        self.amazon_item.asin,
                        self.amazon_item.category,
                        category_id,
                        amazonmws_utils.dict_to_json_string(item_obj),
                    )
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
        return ret

    def revise_item(self, eb_price, quantity):
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
                if amazonmws_utils.to_string(data.Errors.ErrorCode) == '17': # listing deleted
                    EbayItemModelManager.inactive(ebid=self.ebay_item.ebid)
                
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
        except ConnectionError as e:
            if "Code: 21919188," in str(e):
                self.__maxed_out = True
            elif "Code: 21916750," in str(e): # FixedPrice item ended. You are not allowed to revise an ended item
                EbayItemModelManager.inactive(ebid=self.ebay_item.ebid)
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret

    def end_item(self):
        ret = False
        item_obj = self.generate_end_item_obj()
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('EndItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s|EBID:%s] Ack not found" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
            if data.Ack == "Success":
                ret = True
            else:
                logger.error(api.response.json())
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utls.dict_to_json_string(item_obj),
                    api.response.json(),
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
        except ConnectionError as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret

    def oos_item(self):
        pass

    def find_category(self, keywords):
        ret = None

        item_obj = amazonmws_settings.EBAY_GET_SUGGESTED_CATEGORIES_TEMPLATE
        item_obj['MessageID'] = uuid.uuid4()
        item_obj['Query'] = keywords

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetSuggestedCategories', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|GetSuggestedCategories|%s] Ack not found" % (self.ebay_store.username, keywords))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=None,
                    ebid=None
                )
                return None
            if data.Ack == "Success":
                if int(data.CategoryCount) < 1:
                    logger.error("[GetSuggestedCategories] - Unable to find ebay category with this keywords - %s" % keywords)
                    return None
                else:
                    for sg_category in data.SuggestedCategoryArray.SuggestedCategory:
                        if sg_category.Category.CategoryID and sg_category.Category.CategoryName:
                            return (sg_category.Category.CategoryID, sg_category.Category.CategoryName)
                    return None
            else:
                logger.error(api.response.json())
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utls.dict_to_json_string(item_obj),
                    api.response.json(),
                    asin=None,
                    ebid=None
                )
                return None
        except ConnectionError as e:
            logger.exception("[%s|GetSuggestedCategories|%s] %s" % (self.ebay_store.username, keywords, str(e)))
            return None
        except Exception as e:
            logger.exception("[%s|GetSuggestedCategories|%s] %s" % (self.ebay_store.username, keywords, str(e)))
            return None


    ####
    #
    #   DEPRECATED
    # 
    # def find_category(self, keywords):
    #     """return tuple (category_id, category_name) or None
    #     """
    #     try:
    #         api = Finding(debug=True, warnings=True, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))

    #         api_request = amazonmws_settings.EBAY_ADVANCED_FIND_ITEMS_TEMPLATE
    #         api_request["keywords"] = keywords

    #         category_set = {}
    #         category_id_counts = {}
            
    #         response = api.execute('findItemsAdvanced', api_request)
    #         data = response.reply
    #         if not data.ack:
    #             logger.error("[findItemsAdvanced] - ack not found")
    #             return None
    #         if data.ack == "Success":
    #             if int(data.searchResult._count) > 0:
    #                 for searched_item in data.searchResult.item:
    #                     try:
    #                         searched_category_id = searched_item.primaryCategory.categoryId
    #                         searched_category_name = searched_item.primaryCategory.categoryName
                            
    #                         category_set[searched_category_id] = searched_category_name
    #                         category_id_counts[searched_category_id] = category_id_counts[searched_category_id] + 1 if searched_category_id in category_id_counts else 1
    #                     except KeyError as e:
    #                         logger.exception('[findItemsAdvanced] - Category id key not found - %s' % str(e))
    #                         continue
    #         if len(category_id_counts) < 1:
    #             logger.error("[findItemsAdvanced] - Unable to find ebay category with this keywords - %s" % keywords)
    #             return None
    #         else:
    #             # get most searched caregory id
    #             desired_category_id = max(category_id_counts.iteritems(), key=operator.itemgetter(1))[0]
    #             desired_category_name = category_set[desired_category_id]
    #             return (desired_category_id, desired_category_name)

    #     except ConnectionError as e:
    #         logger.exception('[findItemsAdvanced] - %s' % str(e))
    #         return None
    #     except Exception as e:
    #         logger.exception('[findItemsAdvanced] - %s' % str(e))
    #         return None

    def find_category_id(self, keywords):
        category = self.find_category(keywords)
        if category != None:
           return amazonmws_utils.str_to_unicode(category[0])
        return None

    def maxed_out(self):
        return self.__maxed_out

    def fetch_one_item(self, ebay_item_id):
        ret = None
        try:
            item_obj = amazonmws_settings.EBAY_GET_ITEM
            item_obj['MessageID'] = uuid.uuid4()
            item_obj['ItemID'] = ebay_item_id

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success":
                ret = data.Item
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    # def fetch_all_items(self):
    #     ret = []
    #     try:
    #         item_obj = amazonmws_settings.EBAY_GET_SELLER_LIST_TEMPLATE
    #         item_obj['MessageID'] = uuid.uuid4()

    #         token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
    #         api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
    #         response = api.execute('GetSellerList', item_obj)
    #         data = response.reply
    #         if not data.Ack:
    #             logger.error("[%s] Ack not found" % self.ebay_store.username)
    #             record_trade_api_error(
    #                 item_obj['MessageID'], 
    #                 u'GetSellerList', 
    #                 amazonmws_utils.dict_to_json_string(item_obj),
    #                 api.response.json(), 
    #             )
    #         if data.Ack == "Success":
    #             print response
    #         else:
    #             logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
    #             record_trade_api_error(
    #                 item_obj['MessageID'], 
    #                 u'GetSellerList', 
    #                 amazonmws_utils.dict_to_json_string(item_obj),
    #                 api.response.json(), 
    #             )
    #     except ConnectionError as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     except Exception as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     return ret

    def revise_item_title(self):
        ret = False
        item_obj = {
            "MessageID": uuid.uuid4(),
            "Item": {
                "ItemID": self.ebay_item.ebid,
                "Title": amazonmws_utils.generate_ebay_item_title(self.amazon_item.title)
            }
        }

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('ReviseFixedPriceItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s|EBID:%s] Ack not found" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid))
                record_trade_api_error(
                    item_obj['MessageID'], 
                    u'ReviseFixedPriceItem', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
            if data.Ack == "Success":
                ret = True
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
        except ConnectionError as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret


class EbayStorePreferenceAction(object):
    ebay_store = None

    def __init__(self, ebay_store):
        self.ebay_store = ebay_store

    def set_notification_pref(self):
        ret = False
        try:
            notification_obj = amazonmws_settings.EBAY_NOTIFICATION_PREFERENCE_TEMPLATE
            notification_obj['MessageID'] = uuid.uuid4()
            notification_obj['ApplicationDeliveryPreferences']['AlertEmail'] = "mailto://%s" % self.ebay_store.email

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('SetNotificationPreferences', notification_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    notification_obj['MessageID'], 
                    u'SetNotificationPreferences', 
                    amazonmws_utils.dict_to_json_string(notification_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    notification_obj['MessageID'], 
                    u'SetNotificationPreferences', 
                    amazonmws_utils.dict_to_json_string(notification_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def set_user_pref(self):
        ret = False
        try:
            user_obj = amazonmws_settings.EBAY_USER_PREFERENCE_TEMPLATE
            user_obj['MessageID'] = uuid.uuid4()

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('SetUserPreferences', user_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    user_obj['MessageID'], 
                    u'SetUserPreferences', 
                    amazonmws_utils.dict_to_json_string(user_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    user_obj['MessageID'], 
                    u'SetUserPreferences', 
                    amazonmws_utils.dict_to_json_string(user_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret


class EbayOrderAction(object):
    ebay_store = None
    transaction = None

    def __init__(self, ebay_store, transaction):
        self.ebay_store = ebay_store
        self.transaction = transaction

    def generate_shipment_obj(self, carrier, tracking_number):
        shipment_obj = amazonmws_settings.EBAY_SHIPMENT_TEMPLATE
        shipment_obj['MessageID'] = uuid.uuid4()
        shipment_obj['ItemID'] = self.transaction.item_id
        shipment_obj['TransactionID'] = self.transaction.transaction_id
        shipment_obj['OrderID'] = self.transaction.order_id
        shipment_obj['FeedbackInfo']['CommentText'] = self.ebay_store.feedback_comment
        shipment_obj['FeedbackInfo']['TargetUser'] = self.transaction.buyer_user_id
        shipment_obj['Shipment']['ShipmentTrackingDetails']['ShipmentTrackingNumber'] = tracking_number
        # allowed characters - ref: http://developer.ebay.com/devzone/xml/docs/reference/ebay/completesale.html#Request.Shipment.ShipmentTrackingDetails.ShippingCarrierUsed
        shipment_obj['Shipment']['ShipmentTrackingDetails']['ShippingCarrierUsed'] = re.sub(r'[^a-zA-Z\d\s\-]', ' ', carrier)
        return shipment_obj

    def generate_member_message_obj(self, subject, body, question_type):
        shipment_obj = amazonmws_settings.EBAY_SHIPMENT_TEMPLATE
        shipment_obj['MessageID'] = uuid.uuid4()
        shipment_obj['ItemID'] = self.transaction.item_id
        shipment_obj['MemberMessage']['Subject'] = subject
        shipment_obj['MemberMessage']['Body'] = body[:2000] # limited to 2000 characters
        shipment_obj['MemberMessage']['QuestionType'] = question_type
        shipment_obj['MemberMessage']['RecipientID'] = self.transaction.buyer_user_id
        return shipment_obj
    
    def update_shipping_tracking(self, carrier, tracking_number):
        ret = False
        try:
            shipment_obj = self.generate_shipment_obj(carrier, tracking_number)

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('CompleteSale', shipment_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    shipment_obj['MessageID'], 
                    u'CompleteSale', 
                    amazonmws_utils.dict_to_json_string(shipment_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    shipment_obj['MessageID'], 
                    u'CompleteSale', 
                    amazonmws_utils.dict_to_json_string(shipment_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def send_message_to_buyer(self):
        ret = False
        try:
            subject = self.ebay_store.message_on_shipping_subject
            body = self.ebay_store.message_on_shipping_body
            question_type = 'Shipping'
            member_message_obj = self.generate_member_message_obj(subject, body, question_type)

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('AddMemberMessageAAQToPartner', member_message_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    member_message_obj['MessageID'], 
                    u'AddMemberMessageAAQToPartner', 
                    amazonmws_utils.dict_to_json_string(member_message_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    member_message_obj['MessageID'], 
                    u'AddMemberMessageAAQToPartner', 
                    amazonmws_utils.dict_to_json_string(member_message_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

class EbayItemCategoryAction(object):
    ebay_store = None

    def __init__(self, ebay_store):
        self.ebay_store = ebay_store

    def get_top_level_categories(self):
        return self.get_categories(level_limit=1)

    def get_categories(self, parent_category_id=None, level_limit=None):
        ret = []
        try:
            category_obj = amazonmws_settings.EBAY_GET_CATEGORIES_TEMPLATE
            category_obj['MessageID'] = uuid.uuid4()
            if level_limit != None:
                category_obj['LevelLimit'] = level_limit
            if parent_category_id != None:
                category_obj['CategoryParent'] = parent_category_id

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=True, warnings=True, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetCategories', category_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record_trade_api_error(
                    category_obj['MessageID'], 
                    u'GetCategories', 
                    amazonmws_utils.dict_to_json_string(category_obj),
                    api.response.json(), 
                )
            if data.Ack == "Success" and int(data.CategoryCount) > 0:
                if int(data.CategoryCount) == 1:
                    return [data.CategoryArray.Category, ] # make array
                else:
                    return data.CategoryArray.Category
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record_trade_api_error(
                    category_obj['MessageID'], 
                    u'GetCategories', 
                    amazonmws_utils.dict_to_json_string(category_obj),
                    api.response.json(), 
                )
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

