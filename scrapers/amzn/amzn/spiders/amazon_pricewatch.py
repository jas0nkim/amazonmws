import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AmazonAsinSpider
from amzn import parsers


class AmazonPricewatchSpider(AmazonAsinSpider):
    name = "amazon_pricewatch"

    popularity = 2

    def __init__(self, *a, **kw):
        super(AmazonPricewatchSpider, self).__init__(*a, **kw)
        if 'popularity' in kw and kw['popularity'] in [1, 2, 3]:
            self.popularity = kw['popularity']

    def start_requests(self):
        if len(self._asins) < 1:
            raise CloseSpider
        
        for asin in self._asins:
            yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin,
                    callback=parsers.parse_amazon_item,
                    meta={
                        'dont_parse_pictures': False,
                        'dont_parse_variations': False,
                    })
