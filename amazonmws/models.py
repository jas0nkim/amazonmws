from storm.locals import *

from . import settings
from .utils import merge_two_dicts
from .loggers import GrayLogger as logger

# DEPRECATED
#
# class DiscoveredItem(object):
#     __storm_table__ = 'discovered_items'

#     id = Int(primary=True)
#     url = Unicode()
#     asin = Unicode()
#     title = Unicode()
#     created_at = DateTime()
#     updated_at = DateTime()


# class AmazonItem(object):
#     __storm_table__ = 'amazon_items'

#     # AmazonItem.status values
#     STATUS_INACTIVE = 0 # asin is not available any longer (amazon link not available)
#     STATUS_ACTIVE = 1
#     STATUS_OUT_OF_STOCK = 2
#     STATUS_NOT_FBA = 3 # not fulfilled by amazon
#     STATUS_EXCLUDED = 100 # not include this item from updating/listing

#     id = Int(primary=True)
#     url = Unicode()
#     asin = Unicode()
#     category = Unicode()
#     title = Unicode()
#     price = Decimal()
#     features = Unicode()
#     description = Unicode()
#     review_count = Int()
#     avg_rating = Float()
#     status = Int() # 0 - inactive, 1 - active, 2 - out of stock, 3 - not FBA
#     ebay_category_id = Unicode()
#     created_at = DateTime()
#     updated_at = DateTime()


class zzAmazonItem(object):
    __storm_table__ = 'zz__amazon_items'

    STATUS_INACTIVE = 0 # asin is not available any longer (amazon link not available)
    STATUS_ACTIVE = 1

    id = Int(primary=True)
    asin = Unicode()
    url = Unicode()
    category = Unicode()
    title = Unicode()
    price = Decimal()
    market_price = Decimal()
    quantity = Int()
    features = Unicode()
    description = Unicode()
    review_count = Int()
    avg_rating = Float()
    is_fba = Int()
    is_addon = Int()
    merchant_id = Unicode()
    merchant_name = Unicode()
    brand_name = Unicode()
    status = Int() # 0 - inactive, 1 - active
    # ebay_category_id = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


# class AmazonItemPicture(object):
#     __storm_table__ = 'amazon_item_pictures'

#     id = Int(primary=True)
#     amazon_item_id = Int()
#     asin = Unicode()
#     original_picture_url = Unicode()
#     converted_picture_url = Unicode()
#     ebay_picture_url = Unicode()
#     created_at = DateTime()
#     updated_at = DateTime()


class zzAmazonItemPicture(object):
    __storm_table__ = 'zz__amazon_item_pictures'

    id = Int(primary=True)
    asin = Unicode()
    picture_url = Unicode()
    # ebay_picture_url = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class zzAmazonItemOffer(object):
    __storm_table__ = 'zz__amazon_item_offers'

    id = Int(primary=True)
    asin = Unicode()
    price = Decimal()
    quantity = Int()
    is_fba = Int()
    merchant_id = Unicode()
    merchant_name = Unicode()
    revision = Int()
    # ebay_picture_url = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class zzAtoECategoryMap(object):
    __storm_table__ = 'zz__a_to_e_category_maps'

    id = Int(primary=True)
    amazon_category = Unicode()
    ebay_category_id = Unicode()
    ebay_category_name = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class zzAmazonBestsellers(object):
    __storm_table__ = 'zz__amazon_bestsellers'

    id = Int(primary=True)
    bestseller_category = Unicode()
    bestseller_category_url = Unicode()
    rank = Int()
    asin = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class zzAmazonBestsellersArchived(object):
    __storm_table__ = 'zz__amazon_bestsellers_archived'

    id = Int(primary=True)
    bestseller_category = Unicode()
    bestseller_category_url = Unicode()
    rank = Int()
    asin = Unicode()
    created_at = DateTime()


class Scraper(object):
    amazon_category_dblookup = 1001
    amazon_bestsellers_dblookup = 1002
    amazon_keywords_dblookup = 1003
    amazon_category_kidscustume = 2001
    amazon_bestsellers_toyandgames = 2002

    scraper_names = {
        1001: "amazon_category_scraper__database_lookups",
        1002: "amazon_best_sellers_scraper__database_lookups",
        1003: "amazon_keywords_scraper__database_lookups",
        2001: "amazon_category_scraper__kids_custume",
        2002: "amazon_best_sellers_scraper__toy_and_games",
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
    ebay_task_revise_item = 6
    
    amazon_task_exclude_item = 1001

    task_names = {
        1: "ebay_task__listing",
        2: "ebay_task__monitoring_amazon_item_price_changes",
        3: "ebay_task__monitoring_amazon_item_status_changes",
        4: "ebay_task__monitoring_ebay_item_quantity",
        5: "ebay_task__monitoring_amazon_items",

        1001: "amazon_task__exclude_item",
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

# DEPRECATED
#
# class ScraperAmazonItem(object):
#     __storm_table__ = 'scraper_amazon_items'

#     id = Int(primary=True)
#     scraper_id = Int()
#     amazon_item_id = Int()
#     asin = Unicode()
#     created_at = DateTime()
#     updated_at = DateTime()


class EbayItem(object):
    __storm_table__ = 'ebay_items'

    # EbayItem.status values
    STATUS_INACTIVE = 0 # ended item
    STATUS_ACTIVE = 1 # active item
    STATUS_OUT_OF_STOCK = 2

    id = Int(primary=True)
    ebay_store_id = Int()
    asin = Unicode()
    ebid = Unicode()
    ebay_category_id = Unicode()
    eb_price = Decimal()
    quantity = Int()
    status = Int()
    created_at = DateTime()
    updated_at = DateTime()

# DEPRECATED
#
# class EbayListingError(object):
#     __storm_table__ = 'ebay_listing_errors'

#     # EbayItem.status values
#     TYPE_UNLISTED = 1 # still unlisted item
#     TYPE_ERROR_ON_REVISE_PRICE = 2 # listed, but failed on revise
#     TYPE_ERROR_ON_END = 3 # failed on end listing, which means still listed but needs to end immediately
#     TYPE_ERROR_ON_REVISE_QUANTITY = 4 # failed on revise quantity of listing
#     TYPE_ERROR_ON_SET_NOTIFICATION = 5 # error on setting ebay notification preference
#     TYPE_RESOLVED = 100 # resolved

#     id = Int(primary=True)
#     amazon_item_id = Int()
#     asin = Unicode()
#     ebay_item_id = Int()
#     ebid = Unicode()
#     reason = Unicode()
#     related_ebay_api = Unicode() 
#     resolved_howto = Unicode()
#     type = Int()
#     created_at = DateTime()
#     updated_at = DateTime()


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


class EbayStore(object):
    __storm_table__ = 'ebay_stores'

    id = Int(primary=True)
    email = Unicode()
    username = Unicode()
    password = Unicode()
    token = Unicode()
    paypal_username = Unicode()
    margin_percentage = Int()
    margin_max_dollar = Decimal()
    policy_shipping = Unicode()
    policy_payment = Unicode()
    policy_return = Unicode()
    use_salestax_table = Bool()
    fixed_salestax_percentage = Int()
    item_description_template = Unicode()
    created_at = DateTime()
    updated_at = DateTime()


class zzEbayStorePreferredCategory(object):
    __storm_table__ = 'zz__ebay_store_preferred_categories'

    id = Int(primary=True)
    ebay_store_id = Int()
    category_type = Unicode()
    category_name = Unicode()
    max_items = Int()
    priority = Int()
    created_at = DateTime()
    updated_at = DateTime()

class zzExclBrand(object):
    __storm_table__ = 'zz__excl_brands'

    id = Int(primary=True)
    brand_name = Unicode()
    category = Unicode()
    created_at = DateTime()
    updated_at = DateTime()

class Lookup(object):
    __storm_table__ = 'lookups'

    id = Int(primary=True)
    spider_name = Unicode()
    url = Unicode()
    description = Unicode()


# class LookupOwnership(object):
#     __storm_table__ = 'lookup_ownerships'

#     id = Int(primary=True)
#     ebay_store_id = Int()
#     lookup_id = Int()
#     created_at = DateTime()
#     updated_at = DateTime()


# class LookupAmazonItem(object):
#     __storm_table__ = 'lookup_amazon_items'

#     id = Int(primary=True)
#     lookup_id = Int()
#     amazon_item_id = Int()
#     created_at = DateTime()
#     updated_at = DateTime()


class Transaction(object):
    __storm_table__ = 'transactions'

    id = Int(primary=True)
    ebay_store_id = Int()
    seller_user_id = Unicode()
    transaction_id = Unicode()
    item_id = Unicode()
    order_id = Unicode()
    external_transaction_id = Unicode()
    transaction_price = Decimal()
    sales_tax_percent = Decimal()
    sales_tax_state = Unicode()
    sales_tax_amount = Decimal()
    amount_paid = Decimal()
    buyer_email = Unicode()
    buyer_user_id = Unicode()
    buyer_status = Unicode()
    buyer_shipping_name = Unicode()
    buyer_shipping_street1 = Unicode()
    buyer_shipping_street2 = Unicode()
    buyer_shipping_city_name = Unicode()
    buyer_shipping_state_or_province = Unicode()
    buyer_shipping_country = Unicode()
    buyer_shipping_country_name = Unicode()
    buyer_shipping_phone = Unicode()
    buyer_shipping_postal_code = Unicode()
    order_status = Unicode()
    ebay_payment_status = Unicode()
    checkout_status = Unicode()
    complete_status = Unicode()
    payment_hold_status = Unicode()
    external_transaction_status = Unicode()
    raw_item = Unicode()
    raw_transactionarray = Unicode()
    raw_xml = Unicode()
    created_at = DateTime()
    updated_at = DateTime()

# class Order(object):
#     __storm_table__ = 'orders'

#     id = Int(primary=True)
#     order_id = Unicode()
#     status = Unicode()
#     # raw = Unicode()
#     created_at = DateTime()
#     updated_at = DateTime()

class EbayNotificationError(object):
    __storm_table__ = 'ebay_notification_errors'

    id = Int(primary=True)
    correlation_id = RawStr()
    event_name = Unicode()
    recipient_user_id = Unicode()
    ebay_store_id = Int()
    response = Unicode() # xml
    error_code = Int()
    description = Unicode()
    created_at = DateTime()
    updated_at = DateTime()

class ErrorEbayInvalidCategory(object):
    __storm_table__ = 'error_ebay_invalid_category'

    id = Int(primary=True)
    message_id = RawStr()
    asin = Unicode()
    amazon_category = Unicode()
    ebay_category_id = Unicode()
    request = Unicode() # json object
    created_at = DateTime()
    updated_at = DateTime()



__db = create_database('mysql://'+settings.APP_MYSQL_USERNAME+':'+settings.APP_MYSQL_PASSWORD+'@'+settings.APP_MYSQL_HOST+'/'+settings.APP_MYSQL_DATABASE)
StormStore = Store(__db)
