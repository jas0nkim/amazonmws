from storm.locals import *

class EbayProductCategory(object):
    __storm_table__ = 'ebay_product_categories'

    id = Int(primary=True)
    category_id = Int()
    category_level = Int()
    category_name = Unicode()
    category_parent_id = Int()
    auto_pay_enabled = Bool()
    best_offer_enabled = Bool()
    leaf_category = Bool()


__db = create_database('mysql://writeuser:123spirit@localhost/amazonmws')
StormStore = Store(__db)
