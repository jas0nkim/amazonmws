import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn import parsers


class AmazonAsinSpider(CrawlSpider):
    
    name = "amazon_asin"

    allowed_domains = ["amazon.com"]
    handle_httpstatus_list = [404]

    crawlera_enabled = False
    crawlera_apikey = amazonmws_settings.APP_CRAWLERA_API_KEY

    tor_privoxy_enabled = True
    rand_user_agent_enabled = True

    # task related
    task_id = None
    ebay_store_id = None

    # other task related options
    max_amazon_price = None
    min_amazon_price = None
    
    _asins = []
    _asin_cache = {}
    _dont_parse_pictures = False
    _dont_parse_variations = False

    def __init__(self, *a, **kw):
        super(AmazonAsinSpider, self).__init__(*a, **kw)
        if 'asins' in kw:
            self._asins = self._filter_asins(kw['asins'])
        if 'dont_parse_pictures' in kw:
            self._dont_parse_pictures = kw['dont_parse_pictures']
        if 'dont_parse_variations' in kw:
            self._dont_parse_variations = kw['dont_parse_variations']
        if 'premium' in kw and kw['premium'] == True:
            self.tor_privoxy_enabled = False
            self.crawlera_enabled = True
        if 'task_id' in kw:
            self.task_id = kw['task_id']
        if 'ebay_store_id' in kw:
            self.ebay_store_id = kw['ebay_store_id']
        if 'max_amazon_price' in kw:
            self.max_amazon_price = kw['max_amazon_price']
        if 'min_amazon_price' in kw:
            self.min_amazon_price = kw['min_amazon_price']

    def start_requests(self):
        if len(self._asins) < 1:
            raise CloseSpider

        for asin in self._asins:
            yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin,
                        callback=parsers.parse_amazon_item,
                        meta={
                            'dont_parse_pictures': self._dont_parse_pictures,
                            'dont_parse_variations': self._dont_parse_variations,
                        })

    def _filter_asins(self, asins):
        filtered_asins = []
        for asin in asins:
            asin = asin.strip()
            if asin not in self._asin_cache:
                self._asin_cache[asin] = True
                filtered_asins.append(asin)
        return filtered_asins
