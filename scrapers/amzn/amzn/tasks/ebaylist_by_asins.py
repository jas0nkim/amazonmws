import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt
import uuid

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

__asins = [
    'B011AXTQSW',
]

def main(argv):
    ebay_store_id = 1
    task_id = None
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid="])
    except getopt.GetoptError:
        print 'ebaylist_by_asins.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'ebaylist_by_asins.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)


def run(ebay_store_id):
    list_ebay(ebay_store_id=ebay_store_id)

__maxed_out = False

def __do_list(handler, ebay_store, parent_asin):
    amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin)
    ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store.id, asin=parent_asin)
    succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
    if maxed_out:
        __maxed_out = maxed_out
    return not ebay_item and succeed

def list_ebay(ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    __cached_asins = {}

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not ebay_store:
        print("No ebay store found. Ending process...")
        return False

    counter = 0
    handler = ListingHandler(ebay_store=ebay_store)
    for asin in __asins:
        a = AmazonItemModelManager.fetch_one(asin=asin)
        if a.parent_asin not in __cached_asins:
            if __do_list(handler=handler, ebay_store=ebay_store, parent_asin=a.parent_asin):
                print("[{}] CURRENT LISTED COUNT - {}".format(ebay_store.username, counter))
                counter += 1
            __cached_asins[a.parent_asin] = True

        if __maxed_out:
            print("[{}] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION".format(ebay_store.username))
            break
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
