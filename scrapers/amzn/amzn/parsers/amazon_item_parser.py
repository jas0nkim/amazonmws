import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import re
import json

from scrapy.exceptions import IgnoreRequest

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.items import AmazonItem, AmazonPictureItem


class AmazonItemParser(object):
    def parse_item(self, response):
        asin = amazonmws_utils.extract_asin_from_url(response.url)
        if not asin:
            raise IgnoreRequest

        amazon_item = AmazonItem()
        amazon_item['asin'] = amazonmws_utils.str_to_unicode(asin)

        if response.status != 200:
            # broken link or inactive amazon item
            amazon_item['status'] = False
            yield amazon_item

        else:
            parse_picture = True
            if 'dont_parse_pictures' in response.meta and response.meta['dont_parse_pictures']:
                parse_picture = False

            amazon_item['url'] = amazonmws_utils.str_to_unicode(response.url)
            amazon_item['category'] = self.__extract_category(response)
            amazon_item['title'] = self.__extract_title(response)
            amazon_item['price'] = self.__extract_price(response)
            amazon_item['market_price'] = self.__extract_market_price(response, amazon_item['price'])
            amazon_item['quantity'] = self.__extract_quantity(response)
            amazon_item['features'] = self.__extract_features(response)
            amazon_item['description'] = self.__extract_description(response)
            amazon_item['review_count'] = self.__extract_review_count(response)
            amazon_item['avg_rating'] = self.__extract_avg_rating(response)
            amazon_item['is_fba'] = self.__extract_is_fba(response)
            amazon_item['is_addon'] = self.__extract_is_addon(response)
            amazon_item['merchant_id'] = self.__extract_merchant_id(response)
            amazon_item['merchant_name'] = self.__extract_merchant_name(response)
            amazon_item['status'] = True
            yield amazon_item

            # if not amazon_item['is_fba']:
            #     start_index = 0
            #     yield Request(amazonmws_settings.AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT % (asin, start_index), 
            #         callback=parse_item_offer_by_other_seller, 
            #         meta={'amazon_item': amazon_item, 'start_index': start_index},
            #         dont_filter=True)
            # else:

            if parse_picture:
                for pic_url in self.__extract_picture_urls(response):
                    amazon_pic_item = AmazonPictureItem()
                    amazon_pic_item['asin'] = amazonmws_utils.str_to_unicode(asin)
                    amazon_pic_item['picture_url'] = pic_url
                    yield amazon_pic_item

    # def parse_item_offer_listing(self, response):
    #     if 'amazon_item' not in response.meta:
    #         return None
    #     amazon_item = response.meta['amazon_item']

    #     if response.status != 200:
    #         return amazon_item

    #     first_appeared_prime_icon = response.xpath('(//*[@id="olpTabContent"]/div/div[@role="main"]/div[contains(@class, "olpOffer")]/div[1]/span[contains(@class, "supersaver")]/i[contains(@class, "a-icon-prime")])[1]')
    #     if len(first_appeared_prime_icon) > 0:
    #         amazon_item['is_fba'] = True
    #         # update price with fba seller's
    #         amazon_item['price'] = amazonmws_utils.money_to_float(first_appeared_prime_icon.xpath('../../span[1]/text()')[0].extract())
    #     else:
    #         amazon_item['is_fba'] = False

    #     return amazon_item

    def __extract_category(self, response):
        try:
            category_pieces = map(unicode.strip, response.css('#wayfinding-breadcrumbs_feature_div > ul li:not(.a-breadcrumb-divider) > span > a::text').extract())
            if len(category_pieces) < 1:
                return None
            return ' : '.join(category_pieces)
        except Exception, e:
            raise e
            # return None

    def __extract_title(self, response):
        try:            
            summary_col = response.css('#centerCol')
            if len(summary_col) < 1:
                summary_col = response.css('#leftCol')
            if len(summary_col) < 1:
                return None
            return summary_col.css('h1#title > span::text')[0].extract().strip()
        except Exception, e:
            raise e
            # return None

    def __extract_features(self, response):
        try:
            feature_block = response.css('#feature-bullets')
            if len(feature_block) < 1:
                feature_block = response.css('#fbExpandableSectionContent')
            if len(feature_block) < 1:
                return None
            return feature_block[0].extract().strip()
        except Exception, e:
            raise e
            # return None

    def __extract_description(self, response):
        try:
            description_block = response.css('#productDescription')
            if len(description_block) < 1:
                description_block = response.css('#descriptionAndDetails')
            if len(description_block) < 1:
                return None
            description = description_block[0].extract()
            disclaim_block = description_block.css('.disclaim')
            if len(disclaim_block) > 0:
                disclaim = description_block.css('.disclaim')[0].extract()
                description.replace(disclaim, '')
            return description.strip()
        except Exception, e:
            raise e
            # return None

    def __extract_review_count(self, response):
        try:
            return int(response.css('#summaryStars a::text')[1].extract().strip().replace(',', ''))
        except Exception, e:
            # raise e
            return 0

    def __extract_avg_rating(self, response):
        try:
            return float(response.css('#avgRating a > span::text')[0].extract().replace('out of 5 stars', '').strip())
        except Exception, e:
            # raise e
            return 0.0

    def __extract_is_addon(self, response):
        try:
            addon = response.css('#addOnItem_feature_div i.a-icon-addon')
            return True if len(addon) > 0 else False
        except Exception, e:
            raise e
            # return None

    def __extract_is_fba(self, response):
        try:
            if 'sold by amazon.com' in response.css('#merchant-info::text')[0].extract().strip().lower():
                return True
            element = response.css('#merchant-info a#SSOFpopoverLink::text')
            if len(element) > 0 and 'fulfilled by amazon' in element[0].extract().strip().lower():
                return True
            return False
        except Exception, e:
            raise e
            # return False

    def __extract_price(self, response):
        # 1. check deal price block first
        # 2. check sale price block second
        # 3. if no deal/sale price block exists, check our price block
        try:
            price_element = response.css('#priceblock_dealprice::text')
            if len(price_element) < 1:
                price_element = response.css('#priceblock_saleprice::text')
                if len(price_element) < 1:
                    price_element = response.css('#priceblock_ourprice::text')
            if len(price_element) < 1:
                return None
            else:
                price_string = price_element[0].extract()
                return amazonmws_utils.money_to_float(price_string)
        except Exception, e:
            raise e
            # return False

    def __extract_market_price(self, response, default_price):
        try:
            market_price_element = response.css('#price table tr td.a-text-strike::text')
            if len(market_price_element) < 1:
                return default_price
            else:
                market_price_string = market_price_element[0].extract()
                return amazonmws_utils.money_to_float(market_price_string)
        except Exception, e:
            raise e

    def __extract_quantity(self, response):
        try:
            quantity = 0
            element = response.css('#availability span::text')
            if len(element) < 1:
                element = response.css('#pantry-availability span::text')
            if len(element) < 1:
                return quantity # element not found
            
            element_text = element[0].extract().strip().lower()
            if 'out' in element_text:
                quantity = 0 # out of stock
            elif 'only' in element_text:
                quantity = amazonmws_utils.extract_int(element_text)
            else:
                quantity = 1000 # enough stock
            return quantity
        except Exception, e:
            raise e
            # return 0

    def __extract_picture_urls(self, response):
        ret = []
        try:
            html_source = response._get_body()
            m = re.search(r"'colorImages': \{(.+)\},\n", html_source)
            if m:
                # work with json
                json_dump = "{%s}" % m.group(1).replace('\'', '"')
                image_data = json.loads(json_dump)
                for key in image_data:
                    images = image_data[key]
                    for image in images:
                        if "hiRes" in image and image["hiRes"] != None:
                            ret.append(image["hiRes"])
                        elif "large" in image and image["large"] != None:
                            ret.append(image["large"])
                    break
                return ret

            if len(ret) > 0:
                return ret
            else:
                original_image_url = response.css('#main-image-container > ul li.image.item img::attr(src)')
                # try primary image url
                converted_picture_url = re.sub(amazonmws_settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, amazonmws_settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY, original_image_url)
                if not amazonmws_utils.validate_url(converted_picture_url) or not amazonmws_utils.validate_image_size(converted_picture_url):
                    # try secondary image url
                    converted_picture_url = re.sub(amazonmws_settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, amazonmws_settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY, original_image_url)
                    if not amazonmws_utils.validate_url(converted_picture_url) or not amazonmws_utils.validate_image_size(converted_picture_url):
                        ret.append(original_image_url)
                if len(ret) < 1:
                    ret.append(converted_picture_url)
                return ret
        except Exception, e:
            raise e
            # return []

    def __extract_merchant_id(self, response):
        try:
            if 'amazon.com' in response.css('#merchant-info::text')[0].extract().strip().lower():
                return None
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)')
            if len(element) > 0:
                uri = element.css('::attr(href)')[0].extract().strip()
                return amazonmws_utils.extract_seller_id_from_uri(uri)
            return None
        except Exception, e:
            raise e
            # return False

    def __extract_merchant_name(self, response):
        try:
            if 'amazon.com' in response.css('#merchant-info::text')[0].extract().strip().lower():
                return u'Amazon.com'
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)')
            if len(element) > 0:
                return element.css('::text')[0].extract().strip()
            return None
        except Exception, e:
            raise e
            # return False