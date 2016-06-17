import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

from decimal import Decimal

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

ebay_store_id = 1
ebay_store = EbayStoreModelManager.fetch_one(id=1)

eb_price = amazonmws_utils.calculate_profitable_price(Decimal('10.80'), ebay_store)
print eb_price