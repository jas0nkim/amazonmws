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

from amzn.items import AliexpressStoreItem, AliexpressStoreItemFeedback, AliexpressStoreItemFeedbackDetailed


class AliexpressStoreParser(object):

    __store_id = None

    def __init__(self):
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'aliexpress_store_parser'))

    def parse_store(self, response):
        if 'storeid' not in response.meta or not response.meta['storeid']:
            raise IgnoreRequest
        
        self.__store_id = response.meta['storeid']

        alx_store_item = AliexpressStoreItem()
        alx_store_item['store_id'] = self.__store_id
        alx_store_item['store_name'] = self.__extract_store_name(response)
        alx_store_item['company_id'] = self.__extract_company_id(response)
        alx_store_item['owner_member_id'] = self.__extract_owner_member_id(response)
        alx_store_item['store_location'] = self.__extract_store_location(response)
        alx_store_item['store_opened_since'] = self.__extract_store_opened_since(response)
        alx_store_item['is_topratedseller'] = self.__extract_is_topratedseller(response)
        alx_store_item['deliveryguarantee_days'] = self.__extract_deliveryguarantee_days(response)
        alx_store_item['return_policy'] = self.__extract_return_policy(response)
        alx_store_item['has_buyerprotection'] = self.__extract_has_buyerprotection(response)
        yield alx_store_item

        # store feedback
        yield Request(amazonmws_settings.ALIEXPRESS_STORE_FEEDBACK_INFO_LINK_FORMAT.format(
                    companyid=alx_store_item['company_id'],
                    ownermemberid=alx_store_item['owner_member_id']),
                callback=self.parse_store_feedback,
                meta={'storeid': self.__store_id},
                dont_filter=True)

        # store feedback detailed
        yield Request(amazonmws_settings.ALIEXPRESS_STORE_FEEDBACK_DETAILED_INFO_LINK_FORMAT.format(        ownermemberid=alx_store_item['owner_member_id']),
                callback=self.parse_store_feedback_detailed,
                meta={'storeid': self.__store_id},
                dont_filter=True)


    def parse_store_feedback(self, response):
        if 'storeid' not in response.meta or not response.meta['storeid']:
            raise IgnoreRequest

        self.__store_id = response.meta['storeid']

        try:
            feedback_data = response._get_body().strip().split(',')[-1]

            alx_store_feedback = AliexpressStoreItemFeedback()
            alx_store_feedback['store_id'] = self.__store_id
            alx_store_feedback['feedback_score'] = feedback_data[-1]
            alx_store_feedback['feedback_percentage'] = feedback_data[1]
            yield alx_store_feedback
        
        except Exception as e:
            logger.error('[ALXSTOREID:{}] Failed to parse store feedback - {}'.format(self.__store_id, str(e)))
            raise IgnoreRequest


    def parse_store_feedback_detailed(self, response):
        if 'storeid' not in response.meta or not response.meta['storeid']:
            raise IgnoreRequest

        self.__store_id = response.meta['storeid']
        try:
            feedback_detailed_data = json.loads(response._get_body().strip())

            alx_store_feedback_dtld = AliexpressStoreItemFeedbackDetailed()
            alx_store_feedback_dtld['store_id'] = self.__store_id
            alx_store_feedback_dtld['itemasdescribed_score'] = feedback_detailed_data['desc']['score']
            alx_store_feedback_dtld['itemasdescribed_ratings'] = feedback_detailed_data['desc']['ratings']
            alx_store_feedback_dtld['itemasdescribed_percent'] = feedback_detailed_data['desc']['percent']
            alx_store_feedback_dtld['communication_score'] = feedback_detailed_data['seller']['score']
            alx_store_feedback_dtld['communication_ratings'] = feedback_detailed_data['seller']['ratings']
            alx_store_feedback_dtld['communication_percent'] = feedback_detailed_data['seller']['percent']
            alx_store_feedback_dtld['shippingspeed_score'] = feedback_detailed_data['shipping']['score']
            alx_store_feedback_dtld['shippingspeed_ratings'] = feedback_detailed_data['shipping']['ratings']
            alx_store_feedback_dtld['shippingspeed_percent'] = feedback_detailed_data['shipping']['percent']
            yield alx_store_feedback_dtld

        except Exception as e:
            logger.error('[ALXSTOREID:{}] Failed to parse store feedback detailed - {}'.format(self.__store_id, str(e)))
            raise IgnoreRequest

    def __extract_store_name(self, response):
        try:
            store_link_element = response.css('span.shop-name a')
            if len(store_link_element) < 1:
                raise Exception('No store link element found')
            return store_link_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store name - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_company_id(self, response):
        try:
            m = re.search(r"companyId: '(.+?(?=',))", response._get_body())
            if m:
                return m.group(1)
            return None
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing company id - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_owner_member_id(self, response):
        try:
            m = re.search(r"ownerMemberId: '(.+?(?=',))", response._get_body())
            if m:
                return m.group(1)
            return None
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing owner member id - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_store_location(self, response):
        try:
            store_location_element = response.css('.store-info-header .store-location')
            if len(store_location_element) < 1:
                logger.error('[ALXSTOREID:{}] no location element found'.format(self.__store_id))
                return None
            return ' '.join(store_location_element.css('::text')[0].extract().strip().split())
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store location - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_store_opened_since(self, response):
        try:
            store_time_element = response.css('.store-info-header .store-time em')
            if len(store_time_element) < 1:
                logger.error('[ALXSTOREID:{}] no time element found'.format(self.__store_id))
                return None
            return store_time_element.css('::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store opened since - {}'.format(self.__store_id, str(e)))
            return None

    def __extract_is_topratedseller(self, response):
        try:
            top_rated_element = response.css('.top-rated-seller')
            if len(top_rated_element) < 1:
                return False
            return True
        except Exception as e:
            logger.error('[ALXSTOREID:{}] error on parsing store opened since - {}'.format(self.__store_id, str(e)))
            return False

    def __extract_deliveryguarantee_days(self, response):
        pass

    def __extract_return_policy(self, response):
        pass

    def __extract_has_buyerprotection(self, response):
        pass

