import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn import parsers


class AmazonBaseSpider(CrawlSpider):
    
    name = "amazon_base"

    allowed_domains = ["amazon.com"]
    start_urls = []
    handle_httpstatus_list = [404]

    crawlera_enabled = False
    crawlera_apikey = amazonmws_settings.APP_CRAWLERA_API_KEY

    tor_privoxy_enabled = True
    rand_user_agent_enabled = True

    # task related
    task_id = None
    ebay_store_id = None

    # other task related options
    list_new = False
    revise_inventory_only = False
    max_amazon_price = None
    min_amazon_price = None

    force_crawl = False

    _category_links_cache = {}
    # _page_links_cache = {}
    _asin_cache = {}
    _scraped_parent_asins_cache = {}

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            process_links='filter_category_links'
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#pagnNextLink'])
            # process_links='filter_page_links'
        ),

        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[amazonmws_settings.AMAZON_ITEM_LINK_PATTERN],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback=parsers.parse_amazon_item,
            process_links='filter_item_links',
            process_request='pre_item_request',
            follow=True
        ),
    ]

    def __init__(self, *a, **kw):
        super(AmazonBaseSpider, self).__init__(*a, **kw)
        if 'start_urls' in kw:
            self.start_urls = kw['start_urls']
        if 'premium' in kw and kw['premium'] == True:
            self.tor_privoxy_enabled = False
            self.crawlera_enabled = True
        if 'task_id' in kw:
            self.task_id = kw['task_id']
        if 'ebay_store_id' in kw:
            self.ebay_store_id = kw['ebay_store_id']
        if 'list_new' in kw:
            self.list_new = kw['list_new']
        if 'revise_inventory_only' in kw:
            self.revise_inventory_only = kw['revise_inventory_only']
        if 'max_amazon_price' in kw:
            self.max_amazon_price = kw['max_amazon_price']
        if 'min_amazon_price' in kw:
            self.min_amazon_price = kw['min_amazon_price']
        if 'force_crawl' in kw:
            self.force_crawl = kw['force_crawl']

    def filter_category_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self._category_links_cache:
                self._category_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    # def filter_page_links(self, links):
    #     filtered_links = []
    #     for link in links:
    #         if link.url not in self._page_links_cache:
    #             self._page_links_cache[link.url] = True
    #             filtered_links.append(link)
    #     return filtered_links

    def filter_item_links(self, links):
        filtered_links = []
        for link in links:
            asin = amazonmws_utils.extract_asin_from_url(link.url)
            if asin not in self._asin_cache:
                self._asin_cache[asin] = True
                # massaged link - in order to trim amazon's '?ref='
                filtered_links.append(Link(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin, 
                    link.text, link.fragment, link.nofollow))
        return filtered_links

    def pre_item_request(self, request):
        """ replace Request.url to http://www.amazon.com/dp/xxxxxxxx format
        """
        asin = amazonmws_utils.extract_asin_from_url(request.url)
        n_url = amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin
        if request.url != n_url:
            request.replace(url=n_url)
        return request
