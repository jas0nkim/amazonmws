from storm.locals import *

from . import settings
from .utils import merge_two_dicts
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
    STATUS_INACTIVE = 0 # asin is not available any longer (amazon link not available)
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
    review_count = Int()
    avg_rating = Float()
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
    amazon_bestsellers_toyandgames = 1000
    amazon_keywords_kidscustume = 1001

    scraper_names = {
        1000: "amazon best sellers scraper - toy and games",
        1001: "amazon keywords scraper - kids custume",
    }

    @staticmethod
    def get_name(id_):
        try:
            return Scraper.scraper_names[id_]

        except KeyError, e:
            logger.exception(e)
            return "general"


class Task(object):
    """Tasks are super-set of Scrapers
    """
    
    ebay_task_listing = 1
    ebay_task_monitoring_price_changes = 2
    ebay_task_monitoring_status_changes = 3
    ebay_task_monitoring_quantity_changes = 4
    ebay_task_monitoring_amazon_items = 5

    task_names = {
        1: "ebay task - listing",
        2: "ebay task - monitoring amazon item price changes",
        3: "ebay task - monitoring amazon item status changes",
        4: "ebay task - monitoring ebay item quantity",
        5: "ebay task - monitoring amazon items",
    }

    @staticmethod
    def get_name(id_):
        names = merge_two_dicts(Task.task_names, Scraper.scraper_names)

        try:
            return names[id_]

        except KeyError, e:
            logger.exception(e)
            return "general"

        else:
            return name


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
    TYPE_ERROR_ON_REVISE_PRICE = 2 # listed, but failed on revise
    TYPE_ERROR_ON_END = 3 # failed on end listing, which means still listed but needs to end immediately
    TYPE_ERROR_ON_REVISE_QUANTITY = 4 # failed on revise quantity of listing
    TYPE_ERROR_ON_SET_NOTIFICATION = 5 # error on setting ebay notification preference
    TYPE_RESOLVED = 100 # resolved

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


class EbayTradingApiError(object):
    __storm_table__ = 'ebay_trading_api_errors'

    id = Int(primary=True)
    message_id = RawStr()
    trading_api = Unicode()
    request = Unicode() # json object
    response = Unicode() # json object
    error_code = Int()
    description = Unicode()
    amazon_item_id = Int()
    asin = Unicode()
    ebay_item_id = Int()
    ebid = Unicode()
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


class ItemStatusHistory(object):
    __storm_table__ = 'item_status_history'

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    ebay_item_id = Int()
    ebid = Unicode()
    am_status = Int()
    am_status = Int()
    created_at = DateTime()
    updated_at = DateTime()


class ItemQuantityHistory(object):
    __storm_table__ = 'item_quantity_history'

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    ebay_item_id = Int()
    ebid = Unicode()
    am_status = Int()
    am_status = Int()
    created_at = DateTime()
    updated_at = DateTime()



__db = create_database('mysql://'+settings.APP_MYSQL_USERNAME+':'+settings.APP_MYSQL_PASSWORD+'@'+settings.APP_MYSQL_HOST+'/'+settings.APP_MYSQL_DATABASE)
StormStore = Store(__db)
