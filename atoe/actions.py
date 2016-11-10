import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scrapers', 'amzn'))

import re
import json
import uuid
import operator
import datetime
import urllib

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
    __last_error_code = None

    def __init__(self, *a, **kw):
        if 'ebay_store' in kw:
            self.ebay_store = kw['ebay_store']
        if 'amazon_item' in kw:
            self.amazon_item = kw['amazon_item']
        if 'ebay_item' in kw:
            self.ebay_item = kw['ebay_item']
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'atoe'))

    def maxed_out(self):
        return self.__maxed_out

    def get_last_error_code(self):
        return self.__last_error_code

    def generate_upload_picture_obj(self, picture_url):
        picture_obj = amazonmws_settings.EBAY_UPLOAD_SITE_HOSTED_PICTURE;
        picture_obj['MessageID'] = uuid.uuid4()
        picture_obj['ExternalPictureURL'] = picture_url
        return picture_obj

    def _append_details_and_specifics(self, item, variations_item_specifics=None):
        try:
            specs = json.loads(self.amazon_item.specifications)
        except TypeError as e:
            specs = []
        except ValueError as e:
            specs = []
        mpn = amazonmws_utils.get_mpn(specs=specs)
        upc = amazonmws_utils.get_upc(specs=specs)

        item['Item']['ProductListingDetails'] = amazonmws_utils.build_ebay_product_listing_details(brand=self.amazon_item.brand_name, mpn=mpn, upc=upc)
        if variations_item_specifics is not None:
            item['Item']['ItemSpecifics'] = variations_item_specifics
        else:
            item['Item']['ItemSpecifics'] = amazonmws_utils.build_ebay_item_specifics(brand=self.amazon_item.brand_name, mpn=mpn, upc=upc, other_specs=specs)
        return item

    def _append_discount_price_info(self, item, price=None):
        if price is not None and self.amazon_item.market_price is not None and float(price) < self.amazon_item.market_price:
            item['Item']['DiscountPriceInfo'] = {
                'OriginalRetailPrice': self.amazon_item.market_price
            }
        return item

    def _append_variations(self, item, variations=None):
        if variations is not None:
            item['Item']['Variations'] = variations
        return item

    def _build_item_related_keywords(self, category_id):
        ebay_category = EbayItemCategoryManager.fetch_one(category_id=category_id)
        return ebay_category.category_name if ebay_category else None

    def _build_item_related_keywords_search_link(self, category_id):
        ebay_category = EbayItemCategoryManager.fetch_one(category_id=category_id)
        if not ebay_category:
            return None
        ebay_second_top_category = EbayItemCategoryManager.get_second_top_category(category_or_category_id=ebay_category)
        if not ebay_second_top_category:
            return None
        return amazonmws_settings.EBAY_SEARCH_LINK_FORMAT.format(
            querystring=urllib.urlencode({
                    '_ssn': self.ebay_store.username,
                    '_sacat': ebay_second_top_category.category_id,
                    '_nkw': ebay_category.category_name,
            }))

    def generate_add_item_obj(self, category_id, price, quantity=None, title=None, description=None, picture_urls=[], store_category_id=None, variations=None, variations_item_specifics=None):
        item = None
        item = amazonmws_settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['StartPrice'] = price
        item = self._append_discount_price_info(item=item, price=price)
        if quantity is not None:
            item['Item']['Quantity'] = int(quantity)
        else:
            item['Item']['Quantity'] = amazonmws_settings.EBAY_ITEM_DEFAULT_QUANTITY
        item['Item']['SKU'] = self.amazon_item.asin
        item['Item']['Title'] = amazonmws_utils.generate_ebay_item_title(title if title else self.amazon_item.title)
        item['Item']['Description'] = "<![CDATA[\n" + amazonmws_utils.generate_ebay_item_description(
            amazon_item=self.amazon_item,
            ebay_store=self.ebay_store,
            description=description if description else self.amazon_item.description,
            related_keywords=self._build_item_related_keywords(category_id=category_id),
            related_keywords_search_link=self._build_item_related_keywords_search_link(category_id=category_id)) + "\n]]>"
        if len(picture_urls) > 0:
            item['Item']['PictureDetails'] = {
                'PictureURL': picture_urls[:12] # max 12 pictures allowed
            }
        else:
            item['Item'].pop('PictureDetails', None)
        if store_category_id is not None:
            item['Item']['Storefront'] = {}
            item['Item']['Storefront']['StoreCategoryID'] = store_category_id
            item['Item']['Storefront']['StoreCategory2ID'] = 0
        if variations is not None:
            # remove following elements
            item['Item'].pop('SKU', None)
            item['Item'].pop('StartPrice', None)
            item['Item'].pop('Quantity', None)
            item['Item'].pop('ItemSpecifics', None)
            item = self._append_variations(item=item, variations=variations)
        else:
            item['Item'].pop('Variations', None)
        item = self._append_details_and_specifics(item=item,
            variations_item_specifics=variations_item_specifics)
        item['Item']['PayPalEmailAddress'] = self.ebay_store.paypal_username
        item['Item']['UseTaxTable'] = self.ebay_store.use_salestax_table
        item = self.__append_shipping_details(item=item)
        if not self.ebay_store.returns_accepted:
            item['Item']['ReturnPolicy']['ReturnsAcceptedOption'] = 'ReturnsNotAccepted'
        return item

    def __append_shipping_details(self, item):
        shipping_details = {
            "ExcludeShipToLocation": [
                "Alaska/Hawaii",
                "US Protectorates",
                "APO/FPO",
                "PO Box",
            ],
            "GlobalShipping": False,
            "ShippingType": "Flat",
            "ShippingServiceOptions": [],
        }
        options = []
        standard_shipping_fee = self.ebay_store.standard_shipping_fee if self.ebay_store.standard_shipping_fee is not None else amazonmws_settings.EBAY_ITEM_DEFAULT_STANDARD_SHIPPING_FEE
        expedited_shipping_fee = self.ebay_store.expedited_shipping_fee if self.ebay_store.expedited_shipping_fee is not None else amazonmws_settings.EBAY_ITEM_DEFAULT_EXPEDITED_SHIPPING_FEE
        oneday_shipping_fee = self.ebay_store.oneday_shipping_fee if self.ebay_store.oneday_shipping_fee is not None else amazonmws_settings.EBAY_ITEM_DEFAULT_ONEDAY_SHIPPING_FEE

        priority = 1
        if expedited_shipping_fee > 0.00: # append standard shipping option
            if standard_shipping_fee > 0.00:
                options.append({
                    "ShippingServicePriority": priority,
                    "ShippingService": "UPSGround",
                    "ShippingServiceCost": standard_shipping_fee,
                    "ShippingServiceAdditionalCost": 0.00,
                })
            else:
                # free standard shipping fee
                options.append({
                    "ShippingServicePriority": priority,
                    "ShippingService": "UPSGround",
                    "FreeShipping": True,
                    "ShippingServiceAdditionalCost": 0.00,
                })
            priority += 1
            # append expedited shipping option
            options.append({
                "ShippingServicePriority": priority,
                "ShippingService": "UPS3rdDay",
                "ShippingServiceCost": expedited_shipping_fee,
                "ShippingServiceAdditionalCost": 0.00,
            })
            priority += 1
        else:
            # free expedited shipping fee
            options.append({
                "ShippingServicePriority": priority,
                "ShippingService": "UPS3rdDay",
                "FreeShipping": True,
                "ShippingServiceAdditionalCost": 0.00,
            })
            priority += 1
        # append oneday shipping option
        options.append({
            "ShippingServicePriority": priority,
            "ShippingService": "UPSNextDay",
            "ShippingServiceCost": oneday_shipping_fee,
            "ShippingServiceAdditionalCost": 0.00,
        })
        shipping_details["ShippingServiceOptions"] = options
        ship_to_locations = "US"

        # international shipping
        if self.amazon_item.international_shipping:
            international_options = []
            international_options.append({
                "ShippingServicePriority": 1,
                "ShippingService": "OtherInternational",
                "ShippingServiceCost": 18.99,
                "ShippingServiceAdditionalCost": 0.00,
                "ShipToLocation": "Worldwide",
            })
            international_options.append({
                "ShippingServicePriority": 2,
                "ShippingService": "ExpeditedInternational",
                "ShippingServiceCost": 29.99,
                "ShippingServiceAdditionalCost": 0.00,
                "ShipToLocation": "Worldwide",
            })
            shipping_details["ExcludeShipToLocation"] = shipping_details["ExcludeShipToLocation"] + amazonmws_settings.EBAY_ITEM_INTERNATIONAL_EXCLUDESHIPTOLOCATIONS
            shipping_details["GlobalShipping"] = True
            shipping_details["InternationalShippingServiceOption"] = international_options
            ship_to_locations = "Worldwide"

        item["Item"]["ShippingDetails"] = shipping_details
        item["Item"]["ShipToLocations"] = ship_to_locations
        return item

    def generate_revise_item_obj(self, category_id, title=None, description=None, price=None, quantity=None, picture_urls=[], store_category_id=None, variations=None, variations_item_specifics=None):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['PrimaryCategory'] = { "CategoryID": category_id }
        if title is not None:
            item['Item']['Title'] = amazonmws_utils.generate_ebay_item_title(title if title else self.amazon_item.title)
        else:
            item['Item'].pop('Title', None)
        if description is not None:
            item['Item']['Description'] = "<![CDATA[\n" + amazonmws_utils.generate_ebay_item_description(
                    amazon_item=self.amazon_item,
                    ebay_store=self.ebay_store,
                    description=description if description else self.amazon_item.description,
                    related_keywords=self._build_item_related_keywords(category_id=category_id),
                    related_keywords_search_link=self._build_item_related_keywords_search_link(category_id=category_id)) + "\n]]>"
        else:
            item['Item'].pop('Description', None)
        if price is not None:
            item['Item']['StartPrice'] = price
            item = self._append_discount_price_info(item=item, price=price)
        else:
            item['Item'].pop('StartPrice', None)
            item['Item'].pop('DiscountPriceInfo', None)
        if quantity is not None:
            item['Item']['Quantity'] = int(quantity)
        else:
            item['Item'].pop('Quantity', None)
        if len(picture_urls) > 0:
            item['Item']['PictureDetails'] = {
                'PictureURL': picture_urls[:12] # max 12 pictures allowed
            }
        else:
            item['Item'].pop('PictureDetails', None)
        if store_category_id is not None:
            item['Item']['Storefront'] = {}
            item['Item']['Storefront']['StoreCategoryID'] = store_category_id
            item['Item']['Storefront']['StoreCategory2ID'] = 0
        else:
            item['Item'].pop('Storefront', None)
        if variations is not None:
            # remove following elements
            item['Item'].pop('SKU', None)
            item['Item'].pop('StartPrice', None)
            item['Item'].pop('Quantity', None)
            item['Item'].pop('ItemSpecifics', None)
            item = self._append_variations(item=item, variations=variations)
        else:
            item['Item'].pop('Variations', None)
        item = self._append_details_and_specifics(item=item,
                    variations_item_specifics=variations_item_specifics)
        item = self.__append_shipping_details(item=item)
        return item

    def generate_revise_item_category_obj(self, category_id=None):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['PrimaryCategory'] = {
            'CategoryID': category_id
        }
        return item

    def generate_revise_item_policy_obj(self, description=None):
        """ Deprecated: description parameter
        """
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['ReturnPolicy'] = {
            "Description": "The buyer has 30 days to return the item (the buyer pays shipping fees). The item will be refunded. 10% restocking fee may apply.",
            "RefundOption": "MoneyBackOrExchange",
            "RestockingFeeValueOption": "Percent_10",
            "ReturnsAcceptedOption": "ReturnsAccepted",
            "ReturnsWithinOption": "Days_30",
            "ShippingCostPaidByOption": "Buyer",
        }
        item['Item']['DispatchTimeMax'] = 1
        return item

    def generate_revise_item_paypal_address_obj(self):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['SKU'] = self.amazon_item.asin
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['PayPalEmailAddress'] = self.ebay_store.paypal_username
        return item

    def generate_revise_inventory_status_obj(self, price=None, quantity=None, asin=None):
        if price is None and quantity is None:
            return None

        item = amazonmws_settings.EBAY_REVISE_INVENTORY_STATUS_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['InventoryStatus']['ItemID'] = self.ebay_item.ebid
        if asin is not None:
            # multi-variation
            item['InventoryStatus']['SKU'] = asin
        else:
            item['InventoryStatus'].pop('SKU', None)
        if quantity is not None:
            item['InventoryStatus']['Quantity'] = int(quantity)
        else:
            item['InventoryStatus'].pop('Quantity', None)
        if price is not None:
            item['InventoryStatus']['StartPrice'] = price
        else:
            item['InventoryStatus'].pop('StartPrice', None)
        return item

    def generate_revise_item_title_obj(self, title=None):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['Title'] = amazonmws_utils.generate_ebay_item_title(title if title else self.amazon_item.title)
        return item

    def generate_revise_item_description_obj(self, category_id, description=None):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        item['Item']['Description'] = "<![CDATA[\n" + amazonmws_utils.generate_ebay_item_description(
            amazon_item=self.amazon_item,
            ebay_store=self.ebay_store,
            description=description if description else self.amazon_item.description,
            related_keywords=self._build_item_related_keywords(category_id=category_id),
            related_keywords_search_link=self._build_item_related_keywords_search_link(category_id=category_id)) + "\n]]>"
        return item

    """ Deprecated
    """
    def generate_revise_item_specifics_obj(self):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        # item = self._append_details_and_specifics(item)
        return item

    def generate_end_item_obj(self):
        item = amazonmws_settings.EBAY_END_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['ItemID'] = self.ebay_item.ebid
        item['EndingReason'] = 'NotAvailable'
        return item

    def generate_update_variations_obj(self, variations=None):
        item = amazonmws_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.ebay_item.ebid
        if variations is not None:
            item = self._append_variations(item=item, variations=variations)
        else:
            item['Item'].pop('Variations', None)
        return item

    def upload_pictures(self, pictures):
        """upload pictures to ebay hosted server
            Trading API - 'UploadSiteHostedPictures'
        """
        ebay_picture_details = []
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
        except ConnectionError as e:
            logger.exception("[{}|{}]".format(self.ebay_store.username, str(e)))
            return ebay_picture_details
        except Exception as e:
            logger.exception("[{}|{}]".format(self.ebay_store.username, str(e)))
            return ebay_picture_details

        for picture in pictures:
            picture_obj = self.generate_upload_picture_obj(picture)
            try:
                response = api.execute('UploadSiteHostedPictures', picture_obj)
                data = response.reply # ebaysdk.response.ResponseDataObject
                if not data.Ack:
                    logger.error("[{}] Ack not found".format(picture))
                    record = record_trade_api_error(
                        picture_obj['MessageID'],
                        u'UploadSiteHostedPictures',
                        amazonmws_utils.dict_to_json_string(picture_obj),
                        api.response.json()
                    )
                    self.__last_error_code = record.error_code
                    continue
                if data.Ack == "Success":
                    ebay_picture_details.append(data.SiteHostedPictureDetails)
                    logger.info("[{}] ebay picture url - {}".format(picture, data.SiteHostedPictureDetails.FullURL))
                # on minor Waring
                # error code 21916790: Pictures are at least 1000 pixels on the longest side
                # error code 21916791: The image be 90 or greater quality for JPG compression
                elif data.Ack == "Warning":
                    if isinstance(data.Errors, list):
                        logger.warning("{}".format(api.response.json()))
                        record = record_trade_api_error(
                            picture_obj['MessageID'], 
                            u'UploadSiteHostedPictures', 
                            amazonmws_utils.dict_to_json_string(picture_obj),
                            api.response.json()
                        )
                        self.__last_error_code = record.error_code
                        continue
                    else:
                        if amazonmws_utils.to_string(data.Errors.ErrorCode) == "21916791":
                            ebay_picture_details.append(data.SiteHostedPictureDetails)
                            logger.warning("picture url - {} : warning - {}".format(data.SiteHostedPictureDetails.FullURL, data.Errors.LongMessage))
                        else:
                            logger.warning("{}".format(api.response.json()))
                            record = record_trade_api_error(
                                picture_obj['MessageID'], 
                                u'UploadSiteHostedPictures', 
                                amazonmws_utils.dict_to_json_string(picture_obj),
                                api.response.json()
                            )
                            self.__last_error_code = record.error_code
                            continue
                else:
                    logger.error("{}".format(api.response.json()))
                    record = record_trade_api_error(
                        picture_obj['MessageID'], 
                        u'UploadSiteHostedPictures', 
                        amazonmws_utils.dict_to_json_string(picture_obj),
                        api.response.json()
                    )
                    self.__last_error_code = record.error_code
                    continue
            except ConnectionError as e:
                logger.exception("{}".format(str(e)))
                continue
            except Exception as e:
                logger.exception("{}".format(str(e)))
                continue
        return ebay_picture_details

    def add_item(self, category_id, picture_urls, eb_price, quantity, title=None, description=None, store_category_id=None, variations=None, variations_item_specifics=None, content_revised=False):
        """upload item to ebay store
            Trading API - 'AddFixedPriceItem'
        """
        ret = False
        item_obj = self.generate_add_item_obj(category_id=category_id, 
                                    price=eb_price, 
                                    quantity=quantity, 
                                    title=title,
                                    description=description,
                                    picture_urls=picture_urls, 
                                    store_category_id=store_category_id,
                                    variations=variations,
                                    variations_item_specifics=variations_item_specifics)
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('AddFixedPriceItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s] Ack not found" % (self.ebay_store.username, self.amazon_item.asin))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = amazonmws_utils.str_to_unicode(data.ItemID)
            elif data.Ack == "Warning":
                logger.warning("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
                self.__last_error_code = record.error_code
                ret = amazonmws_utils.str_to_unicode(data.ItemID)
            elif data.Ack == "Failure":
                if isinstance(data.Errors, list):
                    logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                    record = record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        amazonmws_utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        asin=self.amazon_item.asin
                    )
                    self.__last_error_code = record.error_code
                else:
                    if amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919188': # reached your selling limit
                        self.__maxed_out = True
                    elif amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919144': # exceed these call frequency limits for Add calls
                        self.__maxed_out = True

                    logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                    record = record_trade_api_error(
                        item_obj['MessageID'], 
                        u'AddFixedPriceItem', 
                        amazonmws_utils.dict_to_json_string(item_obj),
                        api.response.json(), 
                        asin=self.amazon_item.asin
                    )
                    self.__last_error_code = record.error_code
            else:
                logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'AddFixedPriceItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.amazon_item.asin
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            if "Code: 21919188," in str(e): # reached your selling limit
                self.__maxed_out = True
            elif "Code: 21919144," in str(e): # exceed these call frequency limits for Add calls
                self.__maxed_out = True
            elif "Code: 240," in str(e): # The title may contain improper words
                logger.error("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
            elif "Code: 107," in str(e): # Category is not valid
                if not content_revised and self.amazon_item.category: # you may try one more time with revised category id
                    category_route = [re.sub(r'([^\s\w]|_)+', ' ', c).strip() for c in self.amazon_item.category]
                    category_info = self.find_category('%s %s' % (category_route[0], category_route[-1]))
                    if category_info and amazonmws_utils.str_to_unicode(category_info[0]) != category_id:
                        revised_category_id = amazonmws_utils.str_to_unicode(category_info[0])
                        # new category_id. Update db!
                        cmap = AtoECategoryMapModelManager.fetch_one(amazon_category=self.amazon_item.category)
                        if cmap and AtoECategoryMapModelManager.update(cmap, 
                            ebay_category_id=revised_category_id,
                            ebay_category_name=category_info[1]):
                            content_revised = True
                            logger.info("[%s|ASIN:%s] ebay category has been revised from %s to %s - amazon category - %s" % (self.ebay_store.username, self.amazon_item.asin, category_id, revised_category_id, self.amazon_item.category))
                            return self.add_item(category_id=revised_category_id, 
                                picture_urls=picture_urls, 
                                eb_price=eb_price, 
                                quantity=quantity, 
                                title=title,
                                store_category_id=store_category_id,
                                variations=variations, 
                                variations_item_specifics=variations_item_specifics,
                                content_revised=content_revised)
                    # unable to revise category id, then just record the error
                    record = record_ebay_category_error(
                        item_obj['MessageID'], 
                        self.amazon_item.asin,
                        self.amazon_item.category,
                        category_id,
                        amazonmws_utils.dict_to_json_string(item_obj),
                    )
                    self.__last_error_code = record.error_code
                else: # revised, but still get 107 error, then just record the error
                    record = record_ebay_category_error(
                        item_obj['MessageID'], 
                        self.amazon_item.asin,
                        self.amazon_item.category,
                        category_id,
                        amazonmws_utils.dict_to_json_string(item_obj),
                    )
                    self.__last_error_code = record.error_code
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s] %s" % (self.ebay_store.username, self.amazon_item.asin, str(e)))
        return ret

    def end_item(self):
        ret = False
        item_obj = self.generate_end_item_obj()
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('EndItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s|EBID:%s] Ack not found" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error(api.response.json())
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'EndItem', 
                    utls.dict_to_json_string(item_obj),
                    api.response.json(),
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        except Exception as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret

    def oos_item(self, asin=None):
        return self.revise_inventory(eb_price=None, quantity=0, asin=asin, do_revise_item=False)

    def find_category(self, keywords):
        ret = None

        item_obj = amazonmws_settings.EBAY_GET_SUGGESTED_CATEGORIES_TEMPLATE
        item_obj['MessageID'] = uuid.uuid4()
        item_obj['Query'] = keywords

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetSuggestedCategories', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|GetSuggestedCategories|%s] Ack not found" % (self.ebay_store.username, keywords))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetSuggestedCategories', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=None,
                    ebid=None
                )
                self.__last_error_code = record.error_code
                return None
            if data.Ack == "Success":
                if int(data.CategoryCount) < 1:
                    logger.error("[GetSuggestedCategories] - Unable to find ebay category with this keywords - %s" % keywords)
                    return None
                else:
                    for sg_category in data.SuggestedCategoryArray.SuggestedCategory:
                        if sg_category.Category.CategoryID and sg_category.Category.CategoryName:
                            category_route = []
                            if sg_category.Category.CategoryParentName:
                                for ct_parent_name in sg_category.Category.CategoryParentName:
                                    category_route.append(ct_parent_name)
                            category_route.append(sg_category.Category.CategoryName)
                            return (sg_category.Category.CategoryID, ' > '.join(category_route))
                    return None
            else:
                logger.error(api.response.json())
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetSuggestedCategories', 
                    utls.dict_to_json_string(item_obj),
                    api.response.json(),
                    asin=None,
                    ebid=None
                )
                self.__last_error_code = record.error_code
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
    #         api = Finding(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))

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

    def get_category_features(self, category_id):
        ret = None

        item_obj = amazonmws_settings.EBAY_GET_CATEGORY_FEATURES_TEMPLATE
        item_obj['MessageID'] = uuid.uuid4()
        item_obj['CategoryID'] = category_id

        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetCategoryFeatures', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|GetCategoryFeatures|%s] Ack not found" % (self.ebay_store.username, keywords))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetCategoryFeatures', 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=None,
                    ebid=None
                )
                self.__last_error_code = record.error_code
                return None
            if data.Ack == "Success" and data.Category:
                return data.Category
            else:
                logger.error(api.response.json())
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetCategoryFeatures', 
                    utls.dict_to_json_string(item_obj),
                    api.response.json(),
                    asin=None,
                    ebid=None
                )
                self.__last_error_code = record.error_code
                return None
        except ConnectionError as e:
            logger.exception("[%s|GetCategoryFeatures|%s] %s" % (self.ebay_store.username, keywords, str(e)))
            return None
        except Exception as e:
            logger.exception("[%s|GetCategoryFeatures|%s] %s" % (self.ebay_store.username, keywords, str(e)))
            return None

    def fetch_one_item(self, ebid, include_watch_count=False):
        ret = None
        try:
            item_obj = amazonmws_settings.EBAY_GET_ITEM
            item_obj['MessageID'] = uuid.uuid4()
            item_obj['ItemID'] = ebid
            item_obj['IncludeWatchCount'] = include_watch_count

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetItem', item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = data.Item
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    u'GetItem', 
                    amazonmws_utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
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
    #         api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
    #         response = api.execute('GetSellerList', item_obj)
    #         data = response.reply
    #         if not data.Ack:
    #             logger.error("[%s] Ack not found" % self.ebay_store.username)
    #             record = record_trade_api_error(
    #                 item_obj['MessageID'], 
    #                 u'GetSellerList', 
    #                 amazonmws_utils.dict_to_json_string(item_obj),
    #                 api.response.json(), 
    #             )
    #             self.__last_error_code = record.error_code
    #         if data.Ack == "Success":
    #             print response
    #         else:
    #             logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
    #             record = record_trade_api_error(
    #                 item_obj['MessageID'], 
    #                 u'GetSellerList', 
    #                 amazonmws_utils.dict_to_json_string(item_obj),
    #                 api.response.json(), 
    #             )
    #             self.__last_error_code = record.error_code
    #     except ConnectionError as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     except Exception as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     return ret

    def __revise_item(self, item_obj, ebay_api=u'ReviseFixedPriceItem'):
        ret = False
        try:
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute(ebay_api, item_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s|ASIN:%s|EBID:%s] Ack not found" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    ebay_api, 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            elif data.Ack == "Warning":
                if isinstance(data.Errors, list):
                    logger.warning("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                else:
                    if amazonmws_utils.to_string(data.Errors.ErrorCode) == "21919189":
                        logger.warning("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, data.Errors.LongMessage))
                        ret = True
                    else:
                        logger.warning("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'],
                    ebay_api, 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
            elif data.Ack == "Failure":
                if isinstance(data.Errors, list):
                    logger.error("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                else:
                    if amazonmws_utils.to_string(data.Errors.ErrorCode) == '21919188':
                        self.__maxed_out = True
                    if amazonmws_utils.to_string(data.Errors.ErrorCode) == '17': # listing deleted
                        EbayItemModelManager.inactive(ebid=self.ebay_item.ebid)
                    
                    logger.error("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    ebay_api, 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
            else:
                logger.error("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, api.response.json()))
                record = record_trade_api_error(
                    item_obj['MessageID'], 
                    ebay_api, 
                    utils.dict_to_json_string(item_obj),
                    api.response.json(), 
                    asin=self.ebay_item.asin,
                    ebid=self.ebay_item.ebid
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            if "Code: 21919188," in str(e):
                self.__maxed_out = True
            elif "Code: 21916750," in str(e): # FixedPrice item ended. You are not allowed to revise an ended item
                EbayItemModelManager.inactive(ebid=self.ebay_item.ebid)
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
            record = record_trade_api_error(
                item_obj['MessageID'],
                ebay_api,
                utils.dict_to_json_string(item_obj),
                api.response.json() if api and api.response and api.response.json() else None, 
                asin=self.ebay_item.asin,
                ebid=self.ebay_item.ebid
            )
            self.__last_error_code = record.error_code
        except Exception as e:
            logger.exception("[%s|ASIN:%s|EBID:%s] %s" % (self.ebay_store.username, self.ebay_item.asin, self.ebay_item.ebid, str(e)))
        return ret

    def revise_item(self, category_id, title=None, description=None, eb_price=None, quantity=None, picture_urls=[], store_category_id=None, variations=None, variations_item_specifics=None):
        item_obj = self.generate_revise_item_obj(title=title,
            category_id=category_id,
            description=description, 
            price=eb_price, 
            quantity=quantity, 
            picture_urls=[], 
            store_category_id=store_category_id, 
            variations=variations,
            variations_item_specifics=variations_item_specifics)
        return self.__revise_item(item_obj=item_obj, ebay_api=u'ReviseFixedPriceItem')

    def revise_item_title(self, title=None):
        return self.__revise_item(
            item_obj=self.generate_revise_item_title_obj(title=title),
            ebay_api=u'ReviseFixedPriceItem')

    def revise_item_description(self, description=None):
        return self.__revise_item(
            item_obj=self.generate_revise_item_description_obj(description=description),
            ebay_api=u'ReviseFixedPriceItem')

    """ Deprecated
    """
    def revise_item_specifics(self):
        return self.__revise_item(
            item_obj=self.generate_revise_item_specifics_obj(),
            ebay_api=u'ReviseFixedPriceItem')

    def revise_item_policy(self, description=None):
        return self.__revise_item(
            item_obj=self.generate_revise_item_policy_obj(description=description),
            ebay_api=u'ReviseFixedPriceItem')

    def revise_item_paypal_address(self):
        return self.__revise_item(
            item_obj=self.generate_revise_item_paypal_address_obj(),
            ebay_api=u'ReviseFixedPriceItem')

    def revise_item_category(self, category_id=None):
        if not category_id:
            return False

        return self.__revise_item(
            item_obj=self.generate_revise_item_category_obj(category_id=category_id),
            ebay_api=u'ReviseFixedPriceItem')

    def revise_inventory(self, eb_price, quantity, asin=None, do_revise_item=False):
        if self.amazon_item and do_revise_item:
            return self.revise_item(category_id=self.ebay_item.ebay_category_id,
                eb_price=eb_price,
                quantity=quantity)
        else:
            return self.__revise_item(
                item_obj=self.generate_revise_inventory_status_obj(price=eb_price, quantity=quantity, asin=asin),
                ebay_api=u'ReviseInventoryStatus')

    def update_variations(self, variations=None):
        """ delete or add into existing variations
        """
        return self.__revise_item(
            item_obj=self.generate_update_variations_obj(variations=variations),
            ebay_api=u'ReviseFixedPriceItem')

    # deprecated
    #   due to following ebay error
    #   Error: Variation cannot be deleted during restricted revise. (#21916608)
    # use delete_variation() function instead
    #
    # def delete_variations(self, variations=None):
    #     """ delete existing variations
    #     """
    #     return self.update_variations(variations=variations)

    def delete_variation(self, asin):
        """ delete existing variations
        """
        delete_variation_obj = {
            "Variation": [
                {
                    "Delete": True,
                    "SKU": asin,
                    "Quantity": 0, # don't know why.. but ebay api throws error on delete variation without quantity - Error Code: 515, Quantity is not valid. The quantity must be a valid number greater than 0
                }
            ],
        }
        return self.update_variations(variations=delete_variation_obj)


class EbayStorePreferenceAction(object):
    ebay_store = None

    __last_error_code = None

    def __init__(self, ebay_store):
        self.ebay_store = ebay_store

    def get_last_error_code(self):
        return self.__last_error_code

    def set_notification_pref(self):
        ret = False
        try:
            notification_obj = amazonmws_settings.EBAY_NOTIFICATION_PREFERENCE_TEMPLATE
            notification_obj['MessageID'] = uuid.uuid4()
            notification_obj['ApplicationDeliveryPreferences']['AlertEmail'] = "mailto://%s" % self.ebay_store.email

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('SetNotificationPreferences', notification_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    notification_obj['MessageID'], 
                    u'SetNotificationPreferences', 
                    amazonmws_utils.dict_to_json_string(notification_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    notification_obj['MessageID'], 
                    u'SetNotificationPreferences', 
                    amazonmws_utils.dict_to_json_string(notification_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
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
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('SetUserPreferences', user_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    user_obj['MessageID'], 
                    u'SetUserPreferences', 
                    amazonmws_utils.dict_to_json_string(user_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    user_obj['MessageID'], 
                    u'SetUserPreferences', 
                    amazonmws_utils.dict_to_json_string(user_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret


class EbayOrderAction(object):
    ebay_store = None
    transaction = None

    __last_error_code = None

    def __init__(self, ebay_store, transaction=None):
        self.ebay_store = ebay_store
        self.transaction = transaction

    def get_last_error_code(self):
        return self.__last_error_code

    def generate_shipment_obj(self, ebay_order, carrier, tracking_number):
        shipment_obj = amazonmws_settings.EBAY_SHIPMENT_TEMPLATE
        shipment_obj['MessageID'] = uuid.uuid4()
        shipment_obj['OrderID'] = ebay_order.order_id
        shipment_obj['Shipment']['ShipmentTrackingDetails']['ShipmentTrackingNumber'] = tracking_number
        # allowed characters - ref: http://developer.ebay.com/devzone/xml/docs/reference/ebay/completesale.html#Request.Shipment.ShipmentTrackingDetails.ShippingCarrierUsed
        shipment_obj['Shipment']['ShipmentTrackingDetails']['ShippingCarrierUsed'] = re.sub(r'[^a-zA-Z\d\s\-]', ' ', carrier)
        return shipment_obj

    def generate_feedback_obj(self, ebay_order, comment="Thank you for an easy, pleasant transaction. Excellent buyer. A++++++"):
        feedback_obj = amazonmws_settings.EBAY_FEEDBACK_TEMPLATE
        feedback_obj['MessageID'] = uuid.uuid4()
        feedback_obj['OrderID'] = ebay_order.order_id
        feedback_obj['FeedbackInfo']['CommentText'] = comment
        # allowed characters - ref: http://developer.ebay.com/devzone/xml/docs/reference/ebay/completesale.html#Request.Shipment.ShipmentTrackingDetails.ShippingCarrierUsed
        feedback_obj['FeedbackInfo']['TargetUser'] = ebay_order.buyer_user_id
        return feedback_obj


    # def generate_shipment_obj(self, carrier, tracking_number):
    #     shipment_obj = amazonmws_settings.EBAY_SHIPMENT_TEMPLATE
    #     shipment_obj['MessageID'] = uuid.uuid4()
    #     shipment_obj['ItemID'] = self.transaction.item_id
    #     shipment_obj['TransactionID'] = self.transaction.transaction_id
    #     shipment_obj['OrderID'] = self.transaction.order_id
    #     shipment_obj['FeedbackInfo']['CommentText'] = self.ebay_store.feedback_comment
    #     shipment_obj['FeedbackInfo']['TargetUser'] = self.transaction.buyer_user_id
    #     shipment_obj['Shipment']['ShipmentTrackingDetails']['ShipmentTrackingNumber'] = tracking_number
    #     # allowed characters - ref: http://developer.ebay.com/devzone/xml/docs/reference/ebay/completesale.html#Request.Shipment.ShipmentTrackingDetails.ShippingCarrierUsed
    #     shipment_obj['Shipment']['ShipmentTrackingDetails']['ShippingCarrierUsed'] = re.sub(r'[^a-zA-Z\d\s\-]', ' ', carrier)
    #     return shipment_obj

    def generate_member_message_obj(self, ebay_order, ebid, question_type, subject, body):

        # ebay_item = ebay_order.items.all()[:1].get()

        message_obj = amazonmws_settings.EBAY_MEMBER_MESSAGE_TEMPLATE
        message_obj['MessageID'] = uuid.uuid4()
        message_obj['ItemID'] = ebid
        message_obj['MemberMessage']['Subject'] = subject
        message_obj['MemberMessage']['Body'] = body[:2000] # limited to 2000 characters
        message_obj['MemberMessage']['QuestionType'] = question_type
        message_obj['MemberMessage']['RecipientID'] = ebay_order.buyer_user_id
        return message_obj

    def generate_get_orders_obj(self, order_ids=[], create_time_from=None, create_time_to=None, mod_time_from=None, mod_time_to=None, page_number=1):
        orders_obj = amazonmws_settings.EBAY_GET_ORDERS
        orders_obj['MessageID'] = uuid.uuid4()
        if create_time_from is not None:
            orders_obj['CreateTimeFrom'] = create_time_from
        else:
            orders_obj.pop('CreateTimeFrom', None)
        if create_time_to is not None:
            orders_obj['CreateTimeTo'] = create_time_to
        else:
            orders_obj.pop('CreateTimeTo', None)
        if mod_time_from is not None:
            orders_obj['ModTimeFrom'] = mod_time_from
        else:
            orders_obj.pop('ModTimeFrom', None)
        if mod_time_to is not None:
            orders_obj['ModTimeTo'] = mod_time_to
        else:
            orders_obj.pop('ModTimeTo', None)
        if len(order_ids) > 0:
            orders_obj['OrderIDArray'] = {
                'OrderID': order_ids
            }
        else:
            orders_obj.pop('OrderIDArray', None)
        orders_obj['Pagination']['PageNumber'] = page_number
        return orders_obj

    def set_shipping_tracking_info(self, ebay_order, carrier, tracking_number):
        ret = False
        try:
            shipment_obj = self.generate_shipment_obj(ebay_order, carrier, tracking_number)

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('CompleteSale', shipment_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    shipment_obj['MessageID'],
                    u'CompleteSale',
                    amazonmws_utils.dict_to_json_string(shipment_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    shipment_obj['MessageID'],
                    u'CompleteSale',
                    amazonmws_utils.dict_to_json_string(shipment_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def leave_feedback(self, ebay_order):
        ret = False
        try:
            feedback_obj = self.generate_feedback_obj(ebay_order)
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('CompleteSale', feedback_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    feedback_obj['MessageID'],
                    u'CompleteSale',
                    amazonmws_utils.dict_to_json_string(feedback_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    feedback_obj['MessageID'],
                    u'CompleteSale',
                    amazonmws_utils.dict_to_json_string(feedback_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret


    # def update_shipping_tracking(self, carrier, tracking_number):
    #     ret = False
    #     try:
    #         shipment_obj = self.generate_shipment_obj(carrier, tracking_number)

    #         token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
    #         api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
    #         response = api.execute('CompleteSale', shipment_obj)
    #         data = response.reply
    #         if not data.Ack:
    #             logger.error("[%s] Ack not found" % self.ebay_store.username)
    #             record = record_trade_api_error(
    #                 shipment_obj['MessageID'], 
    #                 u'CompleteSale', 
    #                 amazonmws_utils.dict_to_json_string(shipment_obj),
    #                 api.response.json(), 
    #             )
    #             self.__last_error_code = record.error_code
    #         if data.Ack == "Success":
    #             ret = True
    #         else:
    #             logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
    #             record = record_trade_api_error(
    #                 shipment_obj['MessageID'], 
    #                 u'CompleteSale', 
    #                 amazonmws_utils.dict_to_json_string(shipment_obj),
    #                 api.response.json(), 
    #             )
    #             self.__last_error_code = record.error_code
    #     except ConnectionError as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     except Exception as e:
    #         logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
    #     return ret


    def send_message_to_buyer(self, ebay_order, ebid, question_type, subject, body):
        ret = False
        try:
            member_message_obj = self.generate_member_message_obj(ebay_order=ebay_order, ebid=ebid, question_type=question_type, subject=subject, body=body)

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('AddMemberMessageAAQToPartner', member_message_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    member_message_obj['MessageID'], 
                    u'AddMemberMessageAAQToPartner', 
                    amazonmws_utils.dict_to_json_string(member_message_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                ret = True
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    member_message_obj['MessageID'], 
                    u'AddMemberMessageAAQToPartner', 
                    amazonmws_utils.dict_to_json_string(member_message_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def __filter_orders_not_placed_at_origin(self, orders):
        """ THIS FUNCTION NEED TO BE REWRITTEN
            COMPARE 'transaction_amazon_orders' table
        """
        ret = []
        try:
            for order in orders:
                try:
                    for transaction in order.TransactionArray.Transaction:
                        # amazon order id
                        if amazonmws_utils.is_valid_amazon_order_id(transaction.Item.get('SKU', '')):
                            raise GetOutOfLoop("[%s:%s] amazon order already placed" % (self.ebay_store.username, transaction.Item.get('SKU', '')))
                except GetOutOfLoop as e:
                    logger.info(e)
                    continue
                ret.append(order)
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def __get_orders(self, order_ids=[], create_time_from=None, create_time_to=None, mod_time_from=None, mod_time_to=None, page_number=1):
        ret = []
        try:
            get_orders_obj = self.generate_get_orders_obj(order_ids=order_ids,
                create_time_from=create_time_from,
                create_time_to=create_time_to,
                mod_time_from=mod_time_from,
                mod_time_to=mod_time_to,
                page_number=1)

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetOrders', get_orders_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    get_orders_obj['MessageID'], 
                    u'GetOrders', 
                    amazonmws_utils.dict_to_json_string(get_orders_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                if int(data.ReturnedOrderCountActual) == 0:
                    return ret
                orders = data.OrderArray.Order
                # __filter_orders_not_placed_at_origin function doesn't do anything
                # commented out for now
                #
                # TODO: if not placed at origin only option enabled:
                #     orders = self.__filter_orders_not_placed_at_origin(orders=orders)

                if data.HasMoreOrders == True or data.HasMoreOrders == 'true':
                    return orders + self.__get_orders(
                        order_ids=order_ids,
                        create_time_from=create_time_from,
                        create_time_to=create_time_to,
                        mod_time_from=mod_time_from,
                        mod_time_to=mod_time_to,
                        page_number=page_number+1)
                else:
                    return orders
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    get_orders_obj['MessageID'], 
                    u'GetOrders', 
                    amazonmws_utils.dict_to_json_string(get_orders_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def get_orders(self, order_ids=[], modified=False, since_hours_ago=24):
        ret = []
        try:
            if len(order_ids) > 0:
                return self.__get_orders(order_ids=order_ids)

            now = datetime.datetime.now(tz=amazonmws_utils.get_utc())
            if not modified:
                return self.__get_orders(
                    create_time_from=(now - datetime.timedelta(hours=since_hours_ago)).isoformat(),
                    create_time_to=now.isoformat())
            else:
                return self.__get_orders(
                    mod_time_from=(now - datetime.timedelta(hours=since_hours_ago)).isoformat(),
                    mod_time_to=now.isoformat())
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret

    def get_sale_record(self, order_id, transaction_id=None):
        ret = None
        try:
            get_sale_record_obj = { 'MessageID': uuid.uuid4(), 'OrderID': order_id }
            if transaction_id is not None:
                get_sale_record_obj['TransactionID'] = transaction_id

            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetSellingManagerSaleRecord', get_sale_record_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    get_sale_record_obj['MessageID'],
                    u'GetSellingManagerSaleRecord',
                    amazonmws_utils.dict_to_json_string(get_sale_record_obj),
                    api.response.json(),
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                return data.SellingManagerSoldOrder
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    get_sale_record_obj['MessageID'],
                    u'GetSellingManagerSaleRecord',
                    amazonmws_utils.dict_to_json_string(get_sale_record_obj),
                    api.response.json(),
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret


class EbayItemCategoryAction(object):
    ebay_store = None

    __last_error_code = None

    def __init__(self, ebay_store):
        self.ebay_store = ebay_store

    def get_last_error_code(self):
        return self.__last_error_code

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
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('GetCategories', category_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    category_obj['MessageID'], 
                    u'GetCategories', 
                    amazonmws_utils.dict_to_json_string(category_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success" and int(data.CategoryCount) > 0:
                if int(data.CategoryCount) == 1:
                    return [data.CategoryArray.Category, ] # make array
                else:
                    return data.CategoryArray.Category
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    category_obj['MessageID'], 
                    u'GetCategories', 
                    amazonmws_utils.dict_to_json_string(category_obj),
                    api.response.json(), 
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret


class EbayStoreCategoryAction(object):
    ebay_store = None

    __last_error_code = None

    def __init__(self, ebay_store):
        self.ebay_store = ebay_store

    def get_last_error_code(self):
        return self.__last_error_code

    def generate_add_ebay_store_category_obj(self, name, parent_category_id=-999, order=0):
        categories_obj = amazonmws_settings.EBAY_SET_STORE_CATEGORIES_TEMPLATE
        categories_obj["MessageID"] = uuid.uuid4()
        categories_obj["Action"] = "Add"
        categories_obj["DestinationParentCategoryID"] = parent_category_id
        store_categories_obj = {
            "CustomCategory": [
                {
                    "Name": amazonmws_utils.generate_ebay_store_category_name(name),
                },
            ],
        }
        if order > 0:
            store_categories_obj["CustomCategory"][0]['Order'] = order
        categories_obj["StoreCategories"] = store_categories_obj
        return categories_obj

    def add(self, name, parent_category_id=-999, order=0):
        ret = None
        try:
            set_store_categories_obj = self.generate_add_ebay_store_category_obj(name=name,
                parent_category_id=parent_category_id,
                order=order)
            token = None if amazonmws_settings.APP_ENV == 'stage' else self.ebay_store.token
            api = Trading(debug=amazonmws_settings.EBAY_API_DEBUG, warnings=amazonmws_settings.EBAY_API_WARNINGS, domain=amazonmws_settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(amazonmws_settings.CONFIG_PATH, 'ebay.yaml'))
            response = api.execute('SetStoreCategories', set_store_categories_obj)
            data = response.reply
            if not data.Ack:
                logger.error("[%s] Ack not found" % self.ebay_store.username)
                record = record_trade_api_error(
                    set_store_categories_obj['MessageID'],
                    u'SetStoreCategories',
                    amazonmws_utils.dict_to_json_string(set_store_categories_obj),
                    api.response.json(),
                )
                self.__last_error_code = record.error_code
            if data.Ack == "Success":
                # passing only one CustomCategory, not a list
                if data.CustomCategory.CustomCategory and data.CustomCategory.CustomCategory.CategoryID:
                    ret = data.CustomCategory.CustomCategory.CategoryID
                return ret
            else:
                logger.error("[%s] %s" % (self.ebay_store.username, api.response.json()))
                record = record_trade_api_error(
                    set_store_categories_obj['MessageID'],
                    u'SetStoreCategories',
                    amazonmws_utils.dict_to_json_string(set_store_categories_obj),
                    api.response.json(),
                )
                self.__last_error_code = record.error_code
        except ConnectionError as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        except Exception as e:
            logger.exception("[%s] %s" % (self.ebay_store.username, str(e)))
        return ret
