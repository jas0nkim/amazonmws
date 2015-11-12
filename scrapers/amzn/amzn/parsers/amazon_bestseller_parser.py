import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re

from scrapy.exceptions import IgnoreRequest

from amazonmws import utils as amazonmws_utils
from amzn.items import AmazonBestsellerItem


class AmazonBestsellerParser(object):
    def parse_bestseller(self, response):
        if response.status != 200:
            raise IgnoreRequest

        bs_category = self.__extract_bs_category(response)
        item_containers = response.css('#zg_centerListWrapper .zg_itemImmersion')
        for item_container in item_containers:
            bs_item = AmazonBestsellerItem()
            bs_item['bestseller_category'] = bs_category
            bs_item['bestseller_category_url'] = amazonmws_utils.str_to_unicode(re.sub(r'(\?_encoding=UTF8&pg=.*)$', '', response.url))
            bs_item['rank'] = self.__extract_rank(item_container)
            bs_item['asin'] = self.__extract_asin(item_container)
            yield bs_item

            # yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % bs_item['asin'],
            #        callback=parse_amazon_item,
            #        dont_filter=True)

    def __extract_bs_category(self, response):
        return response.css('h1#zg_listTitle span.category::text')[0].extract().strip()

    def __extract_rank(self, container):
        return amazonmws_utils.extract_int(container.css('.zg_rankDiv span.zg_rankNumber::text')[0].extract())

    def __extract_asin(self, container):
        url = container.css('.zg_title a::attr(href)')[0].extract().strip()
        return amazonmws_utils.extract_asin_from_url(url)
