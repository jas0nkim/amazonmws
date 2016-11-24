# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    asin = scrapy.Field()
    parent_asin = scrapy.Field()
    variation_asins = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    market_price = scrapy.Field()
    quantity = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    specifications = scrapy.Field()
    variation_specifics = scrapy.Field()
    review_count = scrapy.Field()
    avg_rating = scrapy.Field()
    is_fba = scrapy.Field()
    is_addon = scrapy.Field()
    is_pantry = scrapy.Field()
    has_sizechart = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant_name = scrapy.Field()
    brand_name = scrapy.Field()
    status = scrapy.Field()
    # ts = scrapy.Field(serializer=str)
    _redirected_asins = scrapy.Field()
    _cached = scrapy.Field()


class AmazonPictureItem(scrapy.Item):
    asin = scrapy.Field()
    picture_urls = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AmazonApparelItem(scrapy.Item):
    parent_asin = scrapy.Field()
    size_chart = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AmazonOfferItem(scrapy.Item):
    asin = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    is_fba = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant_name = scrapy.Field()
    revision = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AmazonBestsellerItem(scrapy.Item):
    bestseller_category = scrapy.Field()
    bestseller_category_url = scrapy.Field()
    rank = scrapy.Field()
    asin = scrapy.Field()
    avg_rating = scrapy.Field()
    review_count = scrapy.Field()
    # ts = scrapy.Field(serializer=str)


class AliexpressItem(scrapy.Item):
    alid = scrapy.Field()
    title = scrapy.Field()
