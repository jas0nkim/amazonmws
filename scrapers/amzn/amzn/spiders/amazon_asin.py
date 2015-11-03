import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from amazonmws import settings as amazonmws_settings
from amzn.parsers import parse_amazon_item

class AmazonAsinSpider(CrawlSpider):
    
    name = "amazon_asin"

    allowed_domains = ["amazon.com"]
    
    __asins = []
    __asin_cache = {}

    def __init__(self, *a, **kw):
        super(AmazonAsinSpider, self).__init__(*a, **kw)
        if 'asins' in kw:
            self.__asins = self.__filter_asins(kw['asins'])

    def start_requests(self):
        if len(self.__asins) < 1:
            yield None
        else:
            for asin in self.__asins:
                url = amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin
                yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin,
                           callback=parse_amazon_item)


    def __filter_asins(self, asins):
        filtered_asins = []
        for asin in asins:
            asin = asin.strip()
            if asin not in self.__asin_cache:
                self.__asin_cache[asin] = True
                filtered_asins.append(asin)
        return filtered_asins
