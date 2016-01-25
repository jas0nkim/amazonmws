import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler

if __name__ == "__main__":

    ebay_store = EbayStoreModelManager.fetch_one(username=u'redflagitems777')
    
    handler = CategoryHandler(ebay_store=ebay_store)
    handler.store_full_categories()