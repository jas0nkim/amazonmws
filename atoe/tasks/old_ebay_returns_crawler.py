import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from atoe.helpers import PostOrderHandler

__ebay_store_id = 1

def main(argv):
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'old_ebay_returns_crawler'))
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'old_ebay_returns_crawler.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'old_ebay_returns_crawler.py'
            sys.exit()
    run()

def run():
    ebay_store = EbayStoreModelManager.fetch_one(id=__ebay_store_id)
    if not ebay_store:
        return False
    helper = PostOrderHandler(ebay_store)
    helper.fetch_returns(date_from='2015-09-01T00:00:00.000Z')

if __name__ == "__main__":
    main(sys.argv[1:])
