import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AmazonAsinSpider
from amzn import parsers


class AmazonPricewatchSpider(AmazonAsinSpider):
    name = "amazon_pricewatch"

    popularity = amazonmws_settings.EBAY_ITEM_POPULARITY_PERCENTAGES

    _sync_ebay_item_first = False
    _synced_ebids_cache = {}

    def __init__(self, *a, **kw):
        super(AmazonPricewatchSpider, self).__init__(*a, **kw)
        if 'popularity' in kw:
            self.popularity = kw['popularity']
        if 'sync_ebay_item_first' in kw:
            self._sync_ebay_item_first = kw['sync_ebay_item_first']
