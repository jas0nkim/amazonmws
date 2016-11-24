import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn import parsers


class AliexpressBaseSpider(CrawlSpider):
    
    name = "aliexpress_base"

    allowed_domains = ["aliexpress.com"]
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
    max_source_price = None
    min_source_price = None

    force_crawl = False
    dont_list_ebay = False

    _category_links_cache = {}
    # _page_links_cache = {}
    _alid_cache = {}
    _scraped_parent_alids_cache = {}

    rules = []

    def __init__(self, *a, **kw):
        super(AliexpressBaseSpider, self).__init__(*a, **kw)
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
        if 'max_source_price' in kw:
            self.max_source_price = kw['max_source_price']
        if 'min_source_price' in kw:
            self.min_source_price = kw['min_source_price']
        if 'force_crawl' in kw:
            self.force_crawl = kw['force_crawl']
        if 'dont_list_ebay' in kw:
            self.dont_list_ebay = kw['dont_list_ebay']

    def filter_item_links(self, links):
        filtered_links = []
        for link in links:
            alid = amazonmws_utils.extract_alid_from_url(link.url)
            if alid not in self._alid_cache:
                self._alid_cache[alid] = True
                # massaged link - in order to trim amazon's '?ref='
                filtered_links.append(Link(amazonmws_settings.ALIEXPRESS_ITEM_LINK_FORMAT % alid, 
                    link.text, link.fragment, link.nofollow))
        return filtered_links

    def pre_item_request(self, request):
        """ replace Request.url to http://www.amazon.com/dp/xxxxxxxx format
        """
        alid = amazonmws_utils.extract_alid_from_url(request.url)
        n_url = amazonmws_settings.ALIEXPRESS_ITEM_LINK_FORMAT % alid
        if request.url != n_url:
            request.replace(url=n_url)
        return request
