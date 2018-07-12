import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws.model_managers import *
from atoe.helpers import InventoryListingHandler


def _create_inventory_items(ebay_store, parent_asin):
    helper = InventoryListingHandler(ebay_store=ebay_store)
    amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin)
    result = helper.list(amazon_items=amazon_items)


if __name__ == "__main__":
    ebay_store = EbayStoreModelManager.fetch_one(id=1)
    parent_asin = 'B071WPN11C'
    _create_inventory_items(ebay_store=ebay_store, parent_asin=parent_asin)
