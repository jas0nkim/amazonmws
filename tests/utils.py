import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from decimal import Decimal

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *

ebay_store_username = u'wbjworld'
ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)

eb_price = amazonmws_utils.calculate_profitable_price(Decimal('26.99'), ebay_store)
print eb_price