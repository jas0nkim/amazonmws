# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    asin = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    review_count = scrapy.Field()
    avg_rating = scrapy.Field()
    is_fba = scrapy.Field()
    is_fba_by_other_seller = scrapy.Field()
    is_addon = scrapy.Field()
    status = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AmazonPictureItem(scrapy.Item):
    asin = scrapy.Field()
    picture_url = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AmazonBestsellerItem(scrapy.Item):
    asin = scrapy.Field()
    bestseller_category = scrapy.Field()
    rank = scrapy.Field()
    # ts = scrapy.Field(serializer=str)
    