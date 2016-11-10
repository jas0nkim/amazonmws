import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import CategoryHandler


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_item_categories_builder.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_item_categories_builder.py'
            sys.exit()
    run()

def run():
    ebay_store = EbayStoreModelManager.fetch_one(id=1)
    
    handler = CategoryHandler(ebay_store=ebay_store)
    handler.store_full_categories()

if __name__ == "__main__":
    main(sys.argv[1:])
