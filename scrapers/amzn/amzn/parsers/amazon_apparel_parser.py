import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re
import json
import uuid
import urllib

from scrapy import Request
from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amzn.items import AmazonApparelItem

class AmazonApparelParser(object):

    __parent_asin = None

    def __init__(self):
        logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_apparel_parser'))

    def parse_apparel_size_chart(self, response):
        if response.status != 200:
            raise IgnoreRequest

        parent_asin = response.meta['asin'] if 'asin' in response.meta and response.meta['asin'] else None
        if not parent_asin:
            raise IgnoreRequest

        amazon_apparel_item = AmazonApparelItem()
        amazon_apparel_item['parent_asin'] = amazonmws_utils.str_to_unicode(parent_asin)
        self.__parent_asin = amazon_apparel_item['parent_asin']

        try:
            amazon_apparel_item['size_chart'] = self.__extract_size_chart(response)
        except Exception as e:
            error_id = uuid.uuid4()
            logger.exception('[ASIN:%s] Failed to parse item <%s> - %s' % (self.__parent_asin, error_id, str(e)))
            raise IgnoreRequest
        
        yield amazon_apparel_item

    def __extract_size_chart(self, response):
        try:
            size_chart_block = response.css('#contentAlignment')
            if len(size_chart_block) < 1:
                return None
            size_chart = size_chart_block[0].extract()
            return amazonmws_utils.replace_html_anchors_to_spans(size_chart.strip())
        except Exception as e:
            raise e
