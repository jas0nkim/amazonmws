import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.items import AmazonOfferItem
import amzn


class AmazonItemOfferParser(object):
    def parse_item_offer(self, response):
        if response.status != 200:
            raise IgnoreRequest

        if 'asin' not in response.meta:
            raise IgnoreRequest

        if 'revision' not in response.meta:
            raise IgnoreRequest

        asin = response.meta['asin']
        revision = response.meta['revision']

        start_index = 0
        if 'start_index' in response.meta:
            start_index = response.meta['start_index']

        max_offers_per_screen = 10
        last_screen = False
        offers = response.css('.olpOffer')

        if len(offers) < max_offers_per_screen:
            last_screen = True

        for offer in offers:
            offer_item = AmazonOfferItem()
            offer_item['asin'] = asin
            offer_item['price'] = self.__extract_price(offer)
            offer_item['quantity'] = 100 # set 100 for now
            offer_item['is_fba'] = self.__extract_is_fba(offer)
            offer_item['merchant_id'] = self.__extract_merchant_id(offer)
            offer_item['merchant_name'] = self.__extract_merchant_name(offer)
            offer_item['revision'] = revision
            yield offer_item

        if not last_screen:
            start_index += max_offers_per_screen
            yield Request(amazonmws_settings.AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT % (asin, start_index), 
                    callback=amzn.parsers.parse_amazon_item_offers,
                    meta={'asin': asin, 'start_index': start_index, 'revision': revision},
                    dont_filter=True)

    def __extract_price(self, element):
        price_element = element.css('span.olpOfferPrice::text')
        if len(price_element) > 0:
            return amazonmws_utils.money_to_float(price_element[0].extract())
        return None

    def __extract_is_fba(self, element):
        if len(element.css('div:first-of-type span.supersaver i.a-icon-prime')) > 0:
            return True
        else:
            return False

    def __extract_merchant_id(self, element):
        anchor_element = element.css('h3.olpSellerName span a')
        if len(anchor_element) < 1:
            anchor_element = element.css('.olpSellerColumn p a')
        if len(anchor_element) < 1:
            return None
        uri = anchor_element.css('::attr(href)')[0].extract().strip()
        return amazonmws_utils.extract_seller_id_from_uri(uri)

    def __extract_merchant_name(self, element):
        name_element = element.css('h3.olpSellerName span a::text')
        if len(name_element) < 1:
            name_element = element.css('h3.olpSellerName img::attr(alt)')
        if len(name_element) < 1:
            return None
        return name_element[0].extract().strip()
