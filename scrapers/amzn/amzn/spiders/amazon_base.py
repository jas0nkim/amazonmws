import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.parsers import parse_amazon_item

class AmazonBaseSpider(CrawlSpider):
    
    name = "amazon_base"

    allowed_domains = ["amazon.com"]
    start_urls = []

    _category_links_cache = {}
    _page_links_cache = {}
    _asin_cache = {}

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            process_links='filter_category_links'
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#pagn .pagnLink']),
            process_links='filter_page_links'
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
            if link.url not in self._category_links_cache:
                self._category_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_page_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self._page_links_cache:
                self._page_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_item_links(self, links):
        filtered_links = []
        for link in links:
            asin = amazonmws_utils.extract_asin_from_url(link)
            if asin not in self._asin_cache:
                self._asin_cache[asin] = True
                filtered_links.append(link)
        return filtered_links
