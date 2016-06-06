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
            bs_item['avg_rating'] = self.__extract_avg_rating(item_container)
            bs_item['review_count'] = self.__extract_review_count(item_container)
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

    def __extract_avg_rating(self, container):
        try:
            return float(container.css('.zg_reviews span span:nth-of-type(1) span.a-icon-alt::text')[0].extract().replace('out of 5 stars', '').strip())
        except IndexError as e:
            return 0.0
        except TypeError as e:
            return 0.0
        except Exception as e:
            return 0.0

    def __extract_review_count(self, container):
        try:
            return int(container.css('.zg_reviews span span:nth-of-type(2) a::text')[0].extract().strip().replace(',', ''))
        except IndexError as e:
            return 0
        except TypeError as e:
            return 0
        except Exception as e:
            return 0
