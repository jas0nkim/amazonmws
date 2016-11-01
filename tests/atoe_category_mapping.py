import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler

if __name__ == "__main__":

    _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
    # atoe_map = AtoECategoryMapModelManager.fetch(created_at__gt='2016-04-16 00:00:00')

    # for a in atoe_map:
    amazon_category = 'Clothing, Shoes & Jewelry : Women : Clothing : Fashion Hoodies & Sweatshirts'
    handler = CategoryHandler(ebay_store=_rand_ebay_store)
    ebay_category_id, ebay_category_name = handler.find_ebay_category(amazon_category)
    print (amazon_category + '      >>>>      ' + ebay_category_name)