import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws.model_managers import *

from atoe.actions import EbayOrderAction


if __name__ == "__main__":

    store = EbayStoreModelManager.fetch_one(id=1)
    action = EbayOrderAction(ebay_store=store)
    orders = action.get_orders()

    print(orders)
