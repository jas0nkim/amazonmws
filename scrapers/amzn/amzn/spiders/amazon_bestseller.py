import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amzn.spiders import AmazonBaseSpider
from amzn import parsers


class AmazonBestsellerSpider(AmazonBaseSpider):
    
    name = "amazon_bestseller"

    rules = []

    def start_requests(self):
        if len(self.start_urls) < 1:
            raise CloseSpider
        for url in self.start_urls:
            for i in range (1, 6): # append page links here
                yield Request('%s?_encoding=UTF8&pg=%d' % (url, i),
                           callback=parsers.parse_amazon_bestseller)

