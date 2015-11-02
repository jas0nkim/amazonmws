import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from amzn import settings
from amzn.items import AmazonItem, AmazonPictureItem

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'amazonmws'))

import amazonmws


class AmazonBaseSpider(CrawlSpider):
    
    name = "amazon_base"

    allowed_domains = ["amazon.com"]
    start_urls = [
        'http://www.amazon.com/b?ie=UTF8&node=12896641',
    ]

    __page_links_cache = {}
    __asin_cache = {}

    rules = [
        # Extract all links under category section
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#refinements .categoryRefinementsSection ul li:not(.shoppingEngineExpand)']),
            callback='parse_category',
            follow=True
        ),

        # Extract page links under each categories
        Rule(LinkExtractor(allow=[r'.*'],
                restrict_css=['#pagn .pagnLink']),
            callback='parse_page',
            process_links='filter_page_links',
            follow=True
        ),

        # Extract amazon item links under main result section
        Rule(LinkExtractor(allow=[settings.AMAZON_ITEM_LINK_PATTERN],
                restrict_css=['ul.s-result-list li.s-result-item']),
            callback='parse_item',
            process_links='filter_item_links',
            follow=True
        ),
    ]

    def filter_page_links(self, links):
        filtered_links = []
        for link in links:
            if link.url not in self.__page_links_cache:
                self.__page_links_cache[link.url] = True
                filtered_links.append(link)
        return filtered_links

    def filter_item_links(self, links):
        filtered_links = []
        for link in links:
            match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, link.url)
            asin = match.group(3)
            if asin not in self.__asin_cache:
                self.__asin_cache[asin] = True
                filtered_links.append(link)
        return filtered_links

    def parse_category(self, response):
        # print "category - " + response.url
        pass

    def parse_page(self, response):
        # print "page - " + response.url
        pass

    def parse_item(self, response):
        match = re.match(settings.AMAZON_ITEM_LINK_PATTERN, response.url)
        asin = match.group(3)

        amazon_item = AmazonItem()
        amazon_item['asin'] = asin
        amazon_item['url'] = response.url
        amazon_item['category'] = self.__extract_category(response)
        amazon_item['title'] = self.__extract_title(response)
        amazon_item['features'] = self.__extract_features(response)
        amazon_item['description'] = self.__extract_description(response)
        amazon_item['review_count'] = self.__extract_review_count(response)
        amazon_item['avg_rating'] = self.__extract_avg_rating(response)
        amazon_item['is_addon'] = self.__extract_is_addon(response)
        amazon_item['is_fba'] = self.__extract_is_fba(response)
        amazon_item['price'] = self.__extract_price(response)
        amazon_item['quantity'] = self.__extract_quantity(response)

        yield amazon_item

        for pic_url in self.__extract_picture_urls(response):
            amazon_pic_item = AmazonPictureItem()
            amazon_pic_item['asin'] = asin
            amazon_pic_item['picture_url'] = pic_url
            yield amazon_pic_item

    def __extract_category(self, response):
        try:
            category_pieces = map(unicode.strip, response.css('#wayfinding-breadcrumbs_feature_div > ul li:not(.a-breadcrumb-divider) > span > a::text').extract())
            if len(category_pieces) < 1:
                return None
            return ' : '.join(category_pieces)
        except Exception:
            return None

    def __extract_title(self, response):
        try:            
            summary_col = response.css('#centerCol')
            if len(summary_col) < 1:
                summary_col = response.css('#leftCol')
            if len(summary_col) < 1:
                return None
            return summary_col.css('h1#title > span::text')[0].extract().strip()
        except Exception:
            return None

    def __extract_features(self, response):
        try:
            feature_block = response.css('#feature-bullets')
            if len(feature_block) < 1:
                feature_block = response.css('#fbExpandableSectionContent')
            if len(feature_block) < 1:
                return None
            return feature_block[0].extract().strip()
        except Exception:
            return None

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
        except Exception:
            return None

    def __extract_review_count(self, response):
        try:
            return int(response.css('#summaryStars a::text')[1].extract().strip().replace(',', ''))
        except Exception:
            return None

    def __extract_avg_rating(self, response):
        try:
            return float(response.css('#avgRating a > span::text')[0].extract().replace('out of 5 stars', '').strip())
        except Exception:
            return None

    def __extract_is_addon(self, response):
        try:
            addon = response.css('#addOnItem_feature_div i.a-icon-addon')
            return True if len(addon) > 0 else False
        except Exception:
            return None

    def __extract_is_fba(self, response):
        pass

    def __extract_price(self, response):
        pass

    def __extract_quantity(self, response):
        pass                

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
                converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY, original_image_url)
                if not amazonmws.utils.validate_url(converted_picture_url) or not amazonmws.utils.validate_image_size(converted_picture_url):
                    # try secondary image url
                    converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY, original_image_url)
                    if not amazonmws.utils.validate_url(converted_picture_url) or not amazonmws.utils.validate_image_size(converted_picture_url):
                        ret.append(original_image_url)
                if len(ret) < 1:
                    ret.append(converted_picture_url)
                return ret
        except Exception:
            return []