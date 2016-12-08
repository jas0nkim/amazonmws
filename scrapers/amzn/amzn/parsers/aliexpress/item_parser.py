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

from amzn.items import AliexpressItem


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
                aliexpress_item['store_number'] = self.__extract_store_number(response)
                aliexpress_item['store_name'] = self.__extract_store_name(response)
                aliexpress_item['store_location'] = self.__extract_store_location(response)
                aliexpress_item['store_openedsince'] = self.__extract_store_openedsince(response)
                aliexpress_item['title'] = self.__extract_title(response)
                aliexpress_item['market_price'] = self.__extract_market_price(response) # 'Price' on the screen
                aliexpress_item['price'] = self.__extract_price(response) # 'Discount Price' on the screen
                aliexpress_item['description'] = self.__extract_description(response)
                aliexpress_item['specifications'] = self.__extract_specifications(response)
                aliexpress_item['skus'] = self.__extract_skus(response)
                aliexpress_item['pictures'] = self.__extract_pictures(response)
                aliexpress_item['review_count'] = self.__extract_review_count(response)
                aliexpress_item['review_rating'] = self.__extract_review_rating(response)
                aliexpress_item['orders'] = self.__extract_orders(response)
                aliexpress_item['_category_route'] = self.__extract_category_route(response)

                # aliexpress_item['is_buyerprotected'] = self.__extract_is_buyerprotected(response)
                # aliexpress_item['delivery_guarantee_days'] = self.__extract_delivery_guarantee_days(response)
                # aliexpress_item['return_policy'] = self.__extract_return_policy(response)
            except Exception as e:
                aliexpress_item['status'] = False
                logger.exception('[ALXID:{}] Failed to parse item - {}'.format(self.__alxid, str(e)))

        yield aliexpress_item

    def __extract_store_number(self, response):
        try:
            store_link_element = response.css('span.shop-name a')
            if len(store_link_element) < 1:
                raise Exception('No store element found')
            return amazonmws_utils.extract_aliexpress_store_id_from_url(url=store_link_element.css('::attr(href)')[0].extract().strip())
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store number - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_store_name(self, response):
        try:
            store_link_element = response.css('span.shop-name a')
            if len(store_link_element) < 1:
                raise Exception('No store element found')
            return store_link_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing store name - {}'.format(self.__alxid, str(e)))
            return None

    def __extract_store_location(self, response):
        pass

    def __extract_store_openedsince(self, response):
        pass

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
        pass

    def __extract_specifications(self, response):
        pass

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

    def __extract_skus(self, response):
        pass

    def __extract_pictures(self, response):
        pass

    def __extract_category_route(self, response):
        """ store all category route (branches)
            i.e. [
                    { level: 1, id: 100003109 name: Women's Clothing & Accessories, is_leaf: false },
                    { level: 2, id: 200000783 name: Sweaters, is_leaf: false },
                    { level: 3, id: 200000879 name: Pullovers, is_leaf: true },
                ]
        """
        try:
            ret = []
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
                ret.append({
                    'level': current_cat_level,
                    'id': category_id,
                    'name': category_name,
                    'is_leaf': is_leaf,
                })
            return ret
        except Exception as e:
            logger.error('[ALXID:{}] error on parsing category route - {}'.format(self.__alxid, str(e)))
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

