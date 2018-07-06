import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws.model_managers import *
from atoe.helpers import InventoryLocationHandler


def _create_inventory_location(ebay_store):
    helper = InventoryLocationHandler(ebay_store=ebay_store)
    result = helper.create_inventory_location()


if __name__ == "__main__":
    ebay_store = EbayStoreModelManager.fetch_one(id=1)
    _create_inventory_location(ebay_store=ebay_store)
