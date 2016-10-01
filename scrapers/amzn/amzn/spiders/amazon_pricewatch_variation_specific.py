import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy import Request
from scrapy.exceptions import CloseSpider

from amazonmws import settings as amazonmws_settings
from amzn.spiders import AmazonAsinSpider
from amzn import parsers


class AmazonPricewatchVariationSpecificSpider(AmazonPricewatchSpider):
    name = "amazon_pricewatch_variation_specific"

    """ _asins format:
        i.e.
        _asins = [
            {
                'asin': 'ABEASDF381',
                'is_variation': False,
            },
            {
                'asin': 'ABEEBSDF38',
                'is_variation': True,
            },
            ...
        ]
    """

    def start_requests(self):
        if len(self._asins) < 1:
            raise CloseSpider

        for data in self._asins:
            if 'is_variation' in data and data['is_variation'] == True:
                amazon_item_link = amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % asin
            else:
                amazon_item_link = amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % asin
            yield Request(amazon_item_link,
                    callback=parsers.parse_amazon_item,
                    meta={
                        'dont_parse_pictures': False,
                        'dont_parse_variations': True,
                    })

    def _filter_asins(self, asins):
        filtered_asins = []
        for data in asins:
            if 'asin' not in data:
                continue
            asin = data['asin'].strip()
            if asin not in self._asin_cache:
                self._asin_cache[asin] = True
                filtered_asins.append(data)
        return filtered_asins
