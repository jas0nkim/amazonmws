import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler

if __name__ == "__main__":
    _rand_ebay_store = EbayStoreModelManager.fetch_one(random=True)
    handler = CategoryHandler(ebay_store=_rand_ebay_store)
    
    atoe_map = AtoECategoryMapModelManager.fetch()
    for cmap in atoe_map:
        try:
            ebay_category_id, ebay_category_name = handler.find_ebay_category(cmap.amazon_category)
            AtoECategoryMapModelManager.update(cmap=cmap,
                ebay_category_id=ebay_category_id,
                ebay_category_name=ebay_category_name)
            print (cmap.amazon_category + '      >>>>      ' + ebay_category_name)

        except Exception:
            continue

