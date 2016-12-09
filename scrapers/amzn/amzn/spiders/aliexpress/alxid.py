import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AliexpressBaseSpider
from amzn import parsers


class AliexpressAlxidSpider(AliexpressBaseSpider):

    name = "aliexpress_alxid"

    _alxids = []

    def __init__(self, *a, **kw):
        super(AliexpressAlxidSpider, self).__init__(*a, **kw)
        if 'alxids' in kw:
            self._alxids = self._filter_alxids(alxids=kw['alxids'])

    def start_requests(self):
        if len(self._alxids) < 1:
            raise CloseSpider

        for alxid in self._alxids:
            yield Request(amazonmws_settings.ALIEXPRESS_ITEM_LINK_FORMAT.format(alxid=alxid),
                        callback=parsers.parse_aliexpress_item)

    def _filter_alxids(self, alxids):
        filtered_alxids = []
        for alxid in alxids:
            alxid = alxid.strip()
            if alxid not in self._alxid_cache:
                self._alxid_cache[alxid] = True
                filtered_alxids.append(alxid)
        return filtered_alxids
