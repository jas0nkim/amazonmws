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

    def __init__(self, *a, **kw):
        super(AmazonPricewatchSpider, self).__init__(*a, **kw)
        if 'popularity' in kw:
            self.popularity = kw['popularity']
