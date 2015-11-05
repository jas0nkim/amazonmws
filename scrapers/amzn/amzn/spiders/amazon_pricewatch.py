import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request

from amazonmws import settings as amazonmws_settings
from amzn.parsers import parse_amazon_item
from amzn.spiders.amazon_asin import AmazonAsinSpider


class AmazonPricewatchSpider(AmazonAsinSpider):
    name = "amazon_pricewatch"    

    def start_requests(self):
        if len(self._asins) < 1:
            yield None
        else:
            for asin in self._asins:
                url = amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin
                yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin,
                           callback=parse_amazon_item,
                           meta={'dont_parse_pictures': True})
