import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy import Request
from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from . import amazon_item_parser


class AmazonBestsellerParser(object):
    def parse_bestseller(self, response):
        if response.status != 200:
            raise IgnoreRequest

        bs_category = self.__extract_bs_category(response)
        item_containers = response.css('#zg_centerListWrapper .zg_itemImmersion')
        for item_container in item_containers:
            rank = self.__extract_rank(item_container)
            asin = self.__extract_asin(item_container)
            avg_rating = self.__extract_avg_rating(item_container)
            review_count = self.__extract_review_count(item_container)

            if 'min_amazon_rating' in response.meta and response.meta['min_amazon_rating'] and avg_rating < response.meta['min_amazon_rating']:
                # skip low rating items if 'min_amazon_rating' set
                continue

            parser = amazon_item_parser.AmazonItemParser()
            yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin,
                        callback=parser.parse_item,
                        meta={
                            'dont_parse_pictures': False,
                            'dont_parse_variations': False,
                        })

    def __extract_bs_category(self, response):
        return response.css('h1#zg_listTitle span.category::text')[0].extract().strip()

    def __extract_rank(self, container):
        return amazonmws_utils.extract_int(container.css('.zg_rankDiv span.zg_rankNumber::text')[0].extract())

    def __extract_asin(self, container):
        url = container.css('.zg_title a::attr(href)')[0].extract().strip()
        return amazonmws_utils.extract_asin_from_url(url)

    def __extract_avg_rating(self, container):
        try:
            return float(container.css('.zg_reviews span span:nth-of-type(1) span.a-icon-alt::text')[0].extract().replace('out of 5 stars', '').strip())
        except IndexError as e:
            return 0.0
        except TypeError as e:
            return 0.0
        except Exception as e:
            return 0.0

    def __extract_review_count(self, container):
        try:
            return int(container.css('.zg_reviews span span:nth-of-type(2) a::text')[0].extract().strip().replace(',', ''))
        except IndexError as e:
            return 0
        except TypeError as e:
            return 0
        except Exception as e:
            return 0
