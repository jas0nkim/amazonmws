from amazon_item_parser import AmazonItemParser
from amazon_item_offer_parser import AmazonItemOfferParser
from amazon_bestseller_parser import AmazonBestsellerParser
from amazon_apparel_parser import AmazonApparelParser

from aliexpress.item_parser import AliexpressItemParser
from aliexpress.store_parser import AliexpressStoreParser


def parse_amazon_item(response):
    parser = AmazonItemParser()
    return parser.parse_item(response)

def parse_amazon_item_offers(response):
    parser = AmazonItemOfferParser()
    return parser.parse_item_offer(response)

def parse_amazon_bestseller(response):
    parser = AmazonBestsellerParser()
    return parser.parse_bestseller(response)

def parse_amazon_apparel(response):
    parser = AmazonApparelParser()
    return parser.parse_apparel_size_chart(response)


def parse_aliexpress_item(response):
    parser = AliexpressItemParser()
    return parser.parse_item(response)

def parse_aliexpress_store(response):
    parser = AliexpressStoreParser()
    return parser.parse_store(response)
