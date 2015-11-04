import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import re
import json

from scrapy import Request

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amzn.items import AmazonItem, AmazonPictureItem, AmazonBestsellerItem


class AmazonItemParser(object):
    def parse_item(self, response):
        if response.status == 200:
            match = re.match(amazonmws_settings.AMAZON_ITEM_LINK_PATTERN, response.url)
            if match:
                asin = match.group(3)

                amazon_item = AmazonItem()
                amazon_item['asin'] = amazonmws_utils.str_to_unicode(asin)
                amazon_item['url'] = amazonmws_utils.str_to_unicode(response.url)
                amazon_item['category'] = self.__extract_category(response)
                amazon_item['title'] = self.__extract_title(response)
                amazon_item['price'] = self.__extract_price(response)
                amazon_item['quantity'] = self.__extract_quantity(response)
                amazon_item['features'] = self.__extract_features(response)
                amazon_item['description'] = self.__extract_description(response)
                amazon_item['review_count'] = self.__extract_review_count(response)
                amazon_item['avg_rating'] = self.__extract_avg_rating(response)
                amazon_item['is_fba'] = self.__extract_is_fba(response)
                amazon_item['is_fba_by_other_seller'] = False
                amazon_item['is_addon'] = self.__extract_is_addon(response)
                amazon_item['status'] = True

                if not amazon_item['is_fba']:
                    yield Request(amazonmws_settings.AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT % asin, 
                        callback=self.parse_item_offer_listing, 
                        meta={'amazon_item': amazon_item})
                else:
                    yield amazon_item

                for pic_url in self.__extract_picture_urls(response):
                    amazon_pic_item = AmazonPictureItem()
                    amazon_pic_item['asin'] = amazonmws_utils.str_to_unicode(asin)
                    amazon_pic_item['picture_url'] = pic_url
                    yield amazon_pic_item
            else:
                yield None
        else: # broken link or inactive amazon item
            match = re.match(amazonmws_settings.AMAZON_ITEM_LINK_PATTERN, response.request.url)
            if match:
                asin = match.group(3)
                amazon_item = AmazonItem()
                amazon_item['asin'] = amazonmws_utils.str_to_unicode(asin)
                amazon_item['status'] = False
            else:
                yield None

    def parse_item_offer_listing(self, response):
        if 'amazon_item' not in response.meta:
            return None
        amazon_item = response.meta['amazon_item']

        if response.status != 200:
            return amazon_item

        first_appeared_prime_icon = response.xpath('(//*[@id="olpTabContent"]/div/div[@role="main"]/div[contains(@class, "olpOffer")]/div[1]/span[contains(@class, "supersaver")]/i[contains(@class, "a-icon-prime")])[1]')
        if len(first_appeared_prime_icon) > 0:
            amazon_item['is_fba'] = True
            amazon_item['is_fba_by_other_seller'] = True
            # update price with fba seller's
            amazon_item['price'] = amazonmws_utils.money_to_float(first_appeared_prime_icon.xpath('../../span[1]/text()')[0].extract())
        else:
            amazon_item['is_fba'] = False
            amazon_item['is_fba_by_other_seller'] = False

        return amazon_item

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
            element2s = response.css('#merchant-info a::text')
            for element2 in element2s:
                if 'fulfilled by amazon' in element2.extract().strip().lower():
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
                price_element = price_element[0].extract()
                return amazonmws_utils.money_to_float(price_element)
        except Exception, e:
            raise e
            # return False

    def __extract_quantity(self, response):
        try:
            quantity = 0
            element_text = response.css('#availability span::text')[0].extract().strip().lower()
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


class AmazonBestsellerParser(object):
    def parse_bestseller(self, response):
        if response.status == 200:
            bs_category = self.__extract_bs_category(response)
            item_containers = response.css('#zg_centerListWrapper .zg_itemImmersion')
            for item_container in item_containers:
                bs_item = AmazonBestsellerItem()
                bs_item['bestseller_category'] = bs_category
                bs_item['rank'] = self.__extract_rank(item_container)
                bs_item['asin'] = self.__extract_asin(item_container)
                yield bs_item

                yield Request(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % bs_item['asin'],
                       callback=parse_amazon_item)
        else:
            yield None

    def __extract_bs_category(self, response):
        return response.css('h1#zg_listTitle span.category::text')[0].extract().strip()

    def __extract_rank(self, container):
        return amazonmws_utils.extract_int(container.css('.zg_rankDiv span.zg_rankNumber::text')[0].extract())

    def __extract_asin(self, container):
        url = container.css('.zg_title a::attr(href)')[0].extract().strip()
        match = re.match(amazonmws_settings.AMAZON_ITEM_LINK_PATTERN, url)
        if match:
            return match.group(3)
        else:
            return None

def parse_amazon_item(response):
    parser = AmazonItemParser()
    return parser.parse_item(response)

def parse_amazon_bestseller(response):
    parser = AmazonBestsellerParser()
    return parser.parse_bestseller(response)
