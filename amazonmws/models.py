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

    id = Int(primary=True)
    url = Unicode()
    asin = Unicode()
    category = Unicode()
    subcategory = Unicode()
    title = Unicode()
    price = Decimal()
    description = Unicode()
    status = Int() # 0 - inactive, 1 - active, 2 - temporarily out of stock, 3 - not FBA
    created_at = DateTime()
    updated_at = DateTime()


__db = create_database('mysql://writeuser:123spirit@localhost/amazonmws')
StormStore = Store(__db)
