import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AliexpressBaseSpider
from amzn import parsers


class AliexpressAlidSpider(AliexpressBaseSpider):

    name = "aliexpress_alid"

    _alids = []

    def __init__(self, *a, **kw):
        super(AliexpressAlidSpider, self).__init__(*a, **kw)
        if 'alids' in kw:
            self._alids = self._filter_alids(alids=kw['alids'])

    def start_requests(self):
        if len(self._alids) < 1:
            raise CloseSpider

        for alid in self._alids:
            yield Request(amazonmws_settings.ALIEXPRESS_ITEM_LINK_FORMAT.format(alid=alid),
                        callback=parsers.parse_aliexpress_item)

    def _filter_alids(self, alids):
        filtered_alids = []
        for alid in alids:
            alid = alid.strip()
            if alid not in self._alid_cache:
                self._alid_cache[alid] = True
                filtered_alids.append(alid)
        return filtered_alids
