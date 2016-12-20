import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings


class AliexpressStoreSpider(CrawlSpider):

    name = "aliexpress_store"

    allowed_domains = ["aliexpress.com"]
    start_urls = []
    handle_httpstatus_list = [404]

    crawlera_enabled = False
    crawlera_apikey = amazonmws_settings.APP_CRAWLERA_API_KEY

    # tor_privoxy_enabled = True
    tor_privoxy_enabled = False
    rand_user_agent_enabled = True

    _alx_store_ids = []
    _alx_store_id_cache = {}

    def __init__(self, *a, **kw):
        super(AliexpressStoreSpider, self).__init__(*a, **kw)
        if 'alx_store_ids' in kw:
            self._alx_store_ids = self._filter_alx_store_ids(alx_store_ids=kw['alx_store_ids'])
        if 'premium' in kw and kw['premium'] == True:
            self.tor_privoxy_enabled = False
            self.crawlera_enabled = True


    def start_requests(self):
        if len(self._alx_store_ids) < 1:
            raise CloseSpider

        for alx_store_id in self._alx_store_ids:
            yield Request(amazonmws_settings.ALIEXPRESS_STORE_LINK_FORMAT.format(alxstoreid=alx_store_id))

    def _filter_alx_store_ids(self, alx_store_ids):
        filtered_alxids = []
        for alx_store_id in alx_store_ids:
            alx_store_id = alx_store_id.strip()
            if alx_store_id not in self._alx_store_id_cache:
                self._alx_store_id_cache[alx_store_id] = True
                filtered_alx_store_ids.append(alx_store_id)
        return filtered_alx_store_ids
