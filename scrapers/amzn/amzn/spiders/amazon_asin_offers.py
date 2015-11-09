import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AmazonAsinSpider
from amzn import parsers


class AmazonAsinOffersSpider(AmazonAsinSpider):
    
    name = "amazon_asin_offers"

    def start_requests(self):
        if len(self._asins) < 1:
            raise CloseSpider
        
        for asin in self._asins:
            start_index = 0
            yield Request(amazonmws_settings.AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT % (asin, start_index),
                    callback=parsers.parse_amazon_item_offers,
                    meta={'asin': asin, 'start_index': start_index},
                    dont_filter=True) # since loop multiple pages
