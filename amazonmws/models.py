from storm.locals import *


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
    amazon_halloween_accessories = 2


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


class UnlistedAmazonItem(object):
    __storm_table__ = 'unlisted_amazon_items'

    # EbayItem.status values
    STATUS_UNLISTED = 1 # still unlisted item
    STATUS_RESOLVED = 2 # resolved

    id = Int(primary=True)
    amazon_item_id = Int()
    asin = Unicode()
    reason = Unicode()
    resolved_howto = Unicode()
    status = Int()
    created_at = DateTime()
    updated_at = DateTime()
    

__db = create_database('mysql://writeuser:123spirit@localhost/amazonmws')
StormStore = Store(__db)
