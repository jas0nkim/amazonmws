from storm.locals import *

from . import settings
from .loggers import GrayLogger as logger


class DiscoveredItem(object):
    __storm_table__ = 'discovered_items'

    id = Int(primary=True)
    url = Unicode()
    asin = Unicode()
    title = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class AmazonItem(object):
    __storm_table__ = 'amazon_items'

    # AmazonItem.status values
    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_OUT_OF_STOCK = 2
    STATUS_NOT_FBA = 3 # not fulfilled by amazon

    id = Int(primary=True)
    url = Unicode()
    asin = Unicode()
    category = Unicode()
    subcategory = Unicode()
    title = Unicode()
    price = Decimal()
    description = Unicode()
    status = Int() # 0 - inactive, 1 - active, 2 - out of stock, 3 - not FBA
    created_at = DateTime()
    updated_at = DateTime()


class AmazonItemPicture(object):
    __storm_table__ = 'amazon_item_pictures'

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    original_picture_url = Unicode()
    converted_picture_url = Unicode()
    ebay_picture_url = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class Scraper(object):
    amazon_bestsellers_toyandgames = 1
    amazon_keywords_halloween = 2

    @staticmethod
    def get_name(id_):
        scraper_names = {
            1: "amazon bestsellers toy and games",
            2: "amazon halloween"
        }

        try:
            return scraper_names[id_]

        except KeyError, e:
            logger.exception(e)
            return "general"


class ScraperAmazonItem(object):
    __storm_table__ = 'scraper_amazon_items'

    id = Int(primary=True)
    scraper_id = Int()
    amazon_item_id = Int()
    asin = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class EbayItem(object):
    __storm_table__ = 'ebay_items'

    # EbayItem.status values
    STATUS_INACTIVE = 0 # ended item
    STATUS_ACTIVE = 1 # listed item
    STATUS_OUT_OF_STOCK = 2

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    ebid = Unicode()
    ebay_category_id = Unicode()
    eb_price = Decimal()
    quantity = Int()
    status = Int()
    created_at = DateTime()
    updated_at = DateTime()


class EbayListingError(object):
    __storm_table__ = 'ebay_listing_errors'

    # EbayItem.status values
    TYPE_UNLISTED = 1 # still unlisted item
    TYPE_ERROR_ON_REVISE = 2 # listed, but failed on revise
    TYPE_RESOLVED = 3 # resolved

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    ebay_item_id = Int()
    ebid = Unicode()
    reason = Unicode()
    related_ebay_api = Unicode() 
    resolved_howto = Unicode()
    type = Int()
    created_at = DateTime()
    updated_at = DateTime()


class ItemPriceHistory(object):
    __storm_table__ = 'item_price_history'

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    ebay_item_id = Int()
    ebid = Unicode()
    am_price = Decimal()
    eb_price = Decimal()
    created_at = DateTime()
    updated_at = DateTime()


__db = create_database('mysql://'+settings.APP_MYSQL_USERNAME+':'+settings.APP_MYSQL_PASSWORD+'@'+settings.APP_MYSQL_HOST+'/'+settings.APP_MYSQL_DATABASE)
StormStore = Store(__db)
