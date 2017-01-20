import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re
import json
import uuid
import urllib
import urlparse

from scrapy import Request
from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from amzn.items import AliexpressItem, AliexpressItemDescription, AliexpressItemSizeInfo, AliexpressItemShipping


class AliexpressItemParser(object):

    __alxid = None

    def __init__(self):
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'aliexpress_item_parser'))

    def parse_item(self, response):
        alxid = amazonmws_utils.extract_alxid_from_url(response.url)
        if not alxid:
            raise IgnoreRequest

        self.__alxid = alxid

        aliexpress_item = AliexpressItem()
        aliexpress_item['alxid'] = self.__alxid

        if response.status != 200:
            # broken link or inactive aliexpress item
            aliexpress_item['status'] = False
        else:
            try:
                aliexpress_item['url'] = amazonmws_utils.str_to_unicode(response.url)
                aliexpress_item['store_id'] = self.__extract_store_id(response)
                aliexpress_item['store_name'] = self.__extract_store_name(response)
                aliexpress_item['store_location'] = self.__extract_store_location(response)
                aliexpress_item['store_openedsince'] = self.__extract_store_openedsince(response)
                aliexpress_item['title'] = self.__extract_title(response)
                aliexpress_item['market_price'] = self.__extract_market_price(response) # 'Price' on the screen
                aliexpress_item['price'] = self.__extract_price(response) # 'Discount Price' on the screen
                aliexpress_item['quantity'] = None
                aliexpress_item['specifications'] = self.__extract_specifications(response)
                aliexpress_item['pictures'] = self.__extract_pictures(response)
                aliexpress_item['review_count'] = self.__extract_review_count(response)
                aliexpress_item['review_rating'] = self.__extract_review_rating(response)
                aliexpress_item['orders'] = self.__extract_orders(response)
                aliexpress_item['_category_route'] = self.__extract_category_route(response)
                aliexpress_item['_skus'] = self.__extract_skus(response)
                aliexpress_item['status'] = True

                # scrape description
                yield Request(amazonmws_settings.ALIEXPRESS_ITEM_DESC_LINK_FORMAT.format(alxid=self.__alxid),
                        callback=self.parse_item_description,
                        meta={'alxid': self.__alxid},
                        dont_filter=True)

                # scrape shipping information
                for epacket_available_country_code in amazonmws_settings.ALIEXPRESS_ITEM_SHIPPING_EPACKET_AVAILABLE_COUNTRIES:
                    yield Request(amazonmws_settings.ALIEXPRESS_ITEM_SHIPPING_INFO_LINK_FORMAT.format(
                            alxid=self.__alxid, countrycode=epacket_available_country_code),
                        callback=self.parse_item_shipping,
                        meta={'alxid': self.__alxid, 'countrycode': epacket_available_country_code},
                        dont_filter=True)

                # scrape size info (apparel only)
                yield self.__extract_sizeinfo(response)

            except Exception as e:
                aliexpress_item['status'] = False
                logger.exception('[ALXID:{}] Failed to parse item - {}'.format(self.__alxid, str(e)))

        yield aliexpress_item

    def parse_item_description(self, response):
        if response.status != 200:
            raise IgnoreRequest

        alxid = None
        if 'alxid' in response.meta:
            alxid = response.meta['alxid']
        if not alxid:
            raise IgnoreRequest

        self.__alxid = alxid

        alx_item_description = AliexpressItemDescription()
        alx_item_description['alxid'] = self.__alxid
        try:
            alx_item_description['description'] = self.__extract_description(response)
        except Exception as e:
            logger.exception('[ALXID:{}] Failed to parse item description - {}'.format(self.__alxid, str(e)))
        yield alx_item_description

    def parse_item_sizeinfo(self, response):
        if response.status != 200:
            raise IgnoreRequest

        alxid = None
        if 'alxid' in response.meta:
            alxid = response.meta['alxid']
        if not alxid:
            raise IgnoreRequest

        self.__alxid = alxid

        alx_item_sizeinfo = AliexpressItemSizeInfo()
        alx_item_sizeinfo['alxid'] = self.__alxid
        try:
            alx_item_sizeinfo['_size_data'] = self.__extract_sizedata(response)
        except Exception as e:
            logger.exception('[ALXID:{}] Failed to parse item size data - {}'.format(self.__alxid, str(e)))
        yield alx_item_sizeinfo

    def parse_item_shipping(self, response):
        if response.status != 200:
            raise IgnoreRequest

        alxid = None
        countrycode = None
        if 'alxid' in response.meta:
            alxid = response.meta['alxid']
        if 'countrycode' in response.meta:
            countrycode = response.meta['countrycode']
        if not alxid or not countrycode:
            raise IgnoreRequest

        self.__alxid = alxid

        alx_item_shipping = AliexpressItemShipping()
        alx_item_shipping['alxid'] = self.__alxid
        alx_item_shipping['country_code'] = countrycode
        try:
            alx_item_shipping['_shippings'] = self.__extract_shippings(response)
        except Exception as e:
            logger.exception('[ALXID:{}|COUNTRY:{}] Failed to parse item shipping - {}'.format(self.__alxid, countrycode, str(e)))
        yield alx_item_shipping

    def __extract_store_id(self, response):
        try:
            store_link_element = response.css('span.shop-name a')
            if len(store_link_element) < 1:
                raise Exception('No store link element found')
            return amazonmws_utils.extract_aliexpress_store_id_from_url(url=store_link_element.css('::attr(href)')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store number - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_store_name(self, response):
        try:
            store_link_element = response.css('span.shop-name a')
            if len(store_link_element) < 1:
                raise Exception('No store link element found')
            return store_link_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store name - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_store_location(self, response):
        try:
            store_location_element = response.css('.store-info-header .store-location')
            if len(store_location_element) < 1:
                raise Exception('No store location element found')
            return ' '.join(store_location_element.css('::text')[0].extract().strip().split())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store location - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_store_openedsince(self, response):
        try:
            store_time_element = response.css('.store-info-header .store-time em')
            if len(store_time_element) < 1:
                raise Exception('No store time element found')
            return store_time_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store opened since - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_title(self, response):
        try:
            title_element = response.css('h1.product-name')
            if len(title_element) < 1:
                raise Exception('No title element found')
            return title_element.css('h1.product-name::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing title - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_market_price(self, response):
        try:
            market_price_element = response.css('#j-sku-price')
            if len(market_price_element) < 1:
                raise Exception('No market price element found')
            return amazonmws_utils.money_to_float(market_price_element.css('::text')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing market price - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_price(self, response):
        try:
            price_element = response.css('#j-sku-discount-price')
            if len(price_element) < 1:
                raise Exception('No price element found')
            return amazonmws_utils.money_to_float(price_element.css('::text')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing price - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_description(self, response):
        try:
            # remove "window.productDescription='" from the beginning and "';" at the end
            return response.body.strip()[27:-2]
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing description - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_specifications(self, response):
        try:
            spec_elements = response.css('#j-product-desc ul.product-property-list li.property-item')
            if len(spec_elements) < 1:
                raise Exception('No spec elements found')
            specs = []
            for spec_el in spec_elements:
                key = spec_el.css('.propery-title::text')[0].extract().strip().rstrip(':')
                val = spec_el.css('.propery-des::text')[0].extract().strip()
                specs.append({ key: val })
            if len(specs) > 0:
                return json.dumps(specs)
            return None
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing specifications - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_review_count(self, response):
        try:
            reviews_element = response.css('#j-customer-reviews-trigger')
            if len(reviews_element) < 1:
                raise Exception('No reviews element found')
            return int(reviews_element.css('span[itemprop=reviewCount]::text')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing review count - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_review_rating(self, response):
        try:
            reviews_element = response.css('#j-customer-reviews-trigger')
            if len(reviews_element) < 1:
                raise Exception('No reviews element found')
            return float(reviews_element.css('span[itemprop=ratingValue]::text')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing review rating - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_orders(self, response):
        try:
            orders_element = response.css('#j-order-num')
            if len(orders_element) < 1:
                raise Exception('No orders element found')
            return amazonmws_utils.extract_int(orders_element.css('::text')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing orders - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_pictures(self, response):
        try:
            m = re.search(r"window.runParams.imageBigViewURL=((.|\n)+?(?=;))", response._get_body())
            if m:
                # work with json / verify value with json functions
                return json.dumps(list(json.loads(m.group(1))))
            return None
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item pictures - {}'.format(self.__alxid, str(e)))
            return None


    def __extract_category_route(self, response):
        """ store all category route (branches)
            i.e. [
                    { level: 1, id: 100003109 name: Women's Clothing & Accessories, is_leaf: false },
                    { level: 2, id: 200000783 name: Sweaters, is_leaf: false },
                    { level: 3, id: 200000879 name: Pullovers, is_leaf: true },
                ]
        """
        try:
            ret = {}
            _route = []
            _cat_names = []
            _cat_elements = response.xpath('//div[@class="ui-breadcrumb"]//a[re:test(@href, "{}")]'.format(amazonmws_settings.ALIEXPRESS_CATEGORY_LINK_PATTERN))
            _cat_elements_length = len(_cat_elements)
            if _cat_elements_length < 1:
                raise Exception('No category element found')
            current_cat_level = 1
            is_leaf = False
            for category_element in _cat_elements:
                if current_cat_level == _cat_elements_length:
                    is_leaf = True
                category_id = amazonmws_utils.extract_aliexpress_category_id_from_url(url=category_element.xpath('.//@href')[0].extract())
                category_name = category_element.xpath('.//text()')[0].extract()
                current_cat_level += 1
                _route.append({
                    'level': current_cat_level,
                    'id': category_id,
                    'name': category_name,
                    'is_leaf': is_leaf,
                })
                _cat_names.append(category_name)
            return { 'category': ' > '.join(_cat_names), 'route': _route }
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing category route - {}'.format(self.__alxid, str(e)))
            return {}

    def __extract_skus(self, response):
        try:
            ret = []
            m = re.search(r"var skuProducts=((.|\n)+?(?=\];)\])", response._get_body())
            if m:
                # work with json
                _sku_data = json.loads(m.group(1))
                for each_sku_data in _sku_data:
                    sku_specifics = self.__extract_sku_specifics(response=response,
                        sku_prop_ids=each_sku_data['skuPropIds'].split(','))
                    each_sku_data['skuSpec'] = sku_specifics['specifics']
                    each_sku_data['skuPics'] = sku_specifics['pictures']
                    ret.append(each_sku_data)
            return ret
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item skus - {}'.format(self.__alxid, str(e)))
            return []

    def __extract_sku_specifics(self, response, sku_prop_ids):
        """ sku title/picture
            - skuPropIds
            - specifics
            - pictures
        """
        specifics = {}
        pictures = []
        try:
            sku_id_index = 1
            for sku_id in sku_prop_ids:
                sku_block = response.css('#j-product-info-sku dl:nth-of-type({})'.format(sku_id_index))
                if len(sku_block) < 1:
                    break
                specific_name = sku_block.css('dt.p-item-title::text')[0].extract().strip().rstrip(':')
                sku_element = sku_block.css('#sku-{index}-{id}'.format(
                                index=sku_id_index,
                                id=sku_id)
                            )
                specific_value = "{id} {val}".format(id=sku_id, val=sku_element.css('::attr(title)')[0].extract().strip()) if len(sku_element.css('::attr(title)')) > 0 else sku_element.css('::text')[0].extract().strip() if len(sku_element.css('::text')) > 0 else sku_id
                specifics[specific_name] = specific_value
                sku_image_element = sku_element.css('img::attr(bigpic)')
                if len(sku_element.css('img::attr(bigpic)')) > 0:
                    pictures.append(sku_image_element[0].extract().strip())
                sku_id_index += 1
            return {
                'specifics': specifics,
                'pictures': pictures,
            }
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item sku specifics/pictures - {}'.format(self.__alxid, str(e)))
            return {
                'specifics': specifics,
                'pictures': pictures,
            }

    def __extract_shippings(self, response):
        try:
            return json.loads(response._get_body().strip().lstrip('(').rstrip(')'))
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item shippings - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_sizeinfo(self, response):
        try:
            m_adminseq = re.search(r"window.runParams.adminSeq=\"(.+?(?=\";))", response._get_body())
            m_pagesizeid = re.search(r"window.runParams.pageSizeID=\"(.+?(?=\";))", response._get_body())
            m_pagesizetype = re.search(r"window.runParams.pageSizeType=\"(.+?(?=\";))", response._get_body())
            if m_adminseq and m_pagesizeid and m_pagesizetype:
                return Request(amazonmws_settings.ALIEXPRESS_ITEM_SIZEINFO_LINK_FORMAT.format(
                            pagesizeid=m_pagesizeid.group(1).strip(),
                            sellerid=m_adminseq.group(1).strip(),
                            pagesizetype=m_pagesizetype.group(1).strip()),
                        callback=self.parse_item_sizeinfo,
                        meta={'alxid': self.__alxid},
                        dont_filter=True)
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item size info - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_sizedata(self, response):
        try:
            return json.loads(response._get_body().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing item size data - {}'.format(self.__alxid, str(e)))
            return None


    # def __extract_is_buyerprotected(self, response):
    #     try:
    #         return response.css('#j-bp-banner') and response.css('#j-bp-banner .buy-protection-info')
    #         if len(bp_element) < 1:
    #             return False
    #         return True
    #     except Exception as e:
    #         logger.error('[ALXID:{}] error on parsing buyer protection - {}'.format(self.__alxid, str(e)))
    #         return False

    # def __extract_delivery_guarantee_days(self, response):
    #     pass

    # def __extract_return_policy(self, response):
    #     pass

