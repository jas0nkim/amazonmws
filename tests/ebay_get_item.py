import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


if __name__ == "__main__":

    store = EbayStoreModelManager.fetch_one(id=1)
    action = EbayItemAction(ebay_store=store)
    item = action.fetch_one_item('281898851548')

    print(item)
