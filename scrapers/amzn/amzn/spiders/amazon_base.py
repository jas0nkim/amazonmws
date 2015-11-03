import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from amazonmws import settings as amazonmws_settings
from amzn.parsers import parse_amazon_item

class AmazonBaseSpider(CrawlSpider):
    
    name = "amazon_base"

    allowed_domains = ["amazon.com"]
    start_urls = []

    __category_links_cache = {}
    __page_links_cache = {}
    __asin_cache = {}

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            callback='parse_category',
            process_links='filter_category_links',
            follow=True
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#pagn .pagnLink']),
            callback='parse_page',
            process_links='filter_page_links',
            follow=True
        ),

        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[amazonmws_settings.AMAZON_ITEM_LINK_PATTERN],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback=parse_amazon_item,
            process_links='filter_item_links',
            follow=True
        ),
    ]

    def __init__(self, *a, **kw):
        super(AmazonBaseSpider, self).__init__(*a, **kw)
        if 'start_urls' in kw:
            self.start_urls = kw['start_urls']

    def filter_category_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self.__category_links_cache:
                self.__category_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_page_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self.__page_links_cache:
                self.__page_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_item_links(self, links):
        filtered_links = []
        for link in links:
            match = re.match(amazonmws_settings.AMAZON_ITEM_LINK_PATTERN, link.url)
            asin = match.group(3)
            if asin not in self.__asin_cache:
                self.__asin_cache[asin] = True
                filtered_links.append(link)
        return filtered_links

    def parse_category(self, response):
        pass

    def parse_page(self, response):
        pass

