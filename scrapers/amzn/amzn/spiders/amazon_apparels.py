import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn import parsers


class AmazonApparelSpider(CrawlSpider):
    
    name = "amazon_apparel"

    allowed_domains = ["amazon.com"]
    handle_httpstatus_list = [404]

    crawlera_enabled = False
    crawlera_apikey = amazonmws_settings.APP_CRAWLERA_API_KEY

    tor_privoxy_enabled = True
    rand_user_agent_enabled = True

    _asins = []
    _asin_cache = {}

    def __init__(self, *a, **kw):
        super(AmazonApparelSpider, self).__init__(*a, **kw)
        if 'asins' in kw:
            self._asins = self._filter_asins(kw['asins'])
        if 'premium' in kw and kw['premium'] == True:
            self.tor_privoxy_enabled = False
            self.crawlera_enabled = True

    def start_requests(self):
        if len(self._asins) < 1:
            raise CloseSpider
        
        for asin in self._asins:
            start_index = 0
            yield Request(amazonmws_settings.AMAZON_ITEM_APPAREL_SIZE_CHART_LINK_FORMAT % asin,
                    callback=parsers.parse_amazon_apparel,
                    meta={'asin': asin},
                    dont_filter=True) # we have own filtering function: _filter_asins()

    def _filter_asins(self, asins):
        filtered_asins = []
        for asin in asins:
            asin = asin.strip()
            if asin not in self._asin_cache:
                self._asin_cache[asin] = True
                filtered_asins.append(asin)
        return filtered_asins
