from amazon_item_parser import AmazonItemParser
from amazon_item_offer_parser import AmazonItemOfferParser
from amazon_bestseller_parser import AmazonBestsellerParser


def parse_amazon_item(response):
    parser = AmazonItemParser()
    return parser.parse_item(response)

def parse_amazon_item_offers(response):
    parser = AmazonItemOfferParser()
    return parser.parse_item_offer(response)

def parse_amazon_bestseller(response):
    parser = AmazonBestsellerParser()
    return parser.parse_bestseller(response)