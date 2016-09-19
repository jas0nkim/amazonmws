import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


def __fetch_and_save_cat_features(ebay_store):
    action = EbayItemAction(ebay_store=ebay_store)

    maps = AtoECategoryMapModelManager.fetch()
    for each in maps:
        try:
            data = action.get_category_features(category_id=each.ebay_category_id)
            if not data:
                continue
            EbayCategoryFeaturesModelManager.create(ebay_category_id=each.ebay_category_id,
                ebay_category_name=each.ebay_category_name,
                upc_enabled=data.UPCEnabled,
                variations_enabled=data.VariationsEnabled
            )
        except Exception as e:
            logger.exception("Failed to save ebay category features - {}".format(str(e)))
            continue
    

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_cat_features_fetcher.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_cat_features_fetcher.py'
            sys.exit()
    run()

def run():
    ebay_store = EbayStoreModelManager.fetch_one(id=1)
    __fetch_and_save_cat_features(ebay_store)


if __name__ == "__main__":
    main(sys.argv[1:])
