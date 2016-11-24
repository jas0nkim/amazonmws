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

    __alid = None

    def __init__(self):
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'aliexpress_item_parser'))

    def parse_item(self, response):
        alid = amazonmws_utils.extract_alid_from_url(response.url)
        if not alid:
            raise IgnoreRequest

        self.__alid = alid

        aliexpress_item = AliexpressItem()
        aliexpress_item['alid'] = self.__alid
        aliexpress_item['title'] = self.__extract_title(response)
        yield aliexpress_item

    def __extract_title(self, response):
        try:
            title_element = response.css('h1.product-name')
            if len(title_element) < 1:
                raise Exception('No title element found')
            return title_element.css('h1.product-name::text')[0].extract().strip()
        except Exception as e:
            logger.error('[ASIN:{}] error on parsing title'.format(self.__alid))
            return None
