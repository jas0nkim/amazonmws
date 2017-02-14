import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.helpers import PostOrderHandler


__ebay_stores = [1, ]

def main(argv):
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'ebay_order_returns_fetcher'))
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_order_returns_fetcher.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_order_returns_fetcher.py'
            sys.exit()
    run()

def run():
    for ebay_store_id in __ebay_stores:
        ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
        if not ebay_store:
            continue
        helper = PostOrderHandler(ebay_store)
        helper.fetch_returns()


if __name__ == "__main__":
    main(sys.argv[1:])
