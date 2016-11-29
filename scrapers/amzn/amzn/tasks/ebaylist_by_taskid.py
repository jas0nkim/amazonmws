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


def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:t:", ["ebaystoreid=", "taskid="])
    except getopt.GetoptError:
        print 'ebaylist_by_taskid.py -e <1|2|3|4|...ebaystoreid> -t <taskid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'ebaylist_by_taskid.py -e <1|2|3|4|...ebaystoreid> -t <taskid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
        elif opt in ("-t", "--taskid"):
            task_id = arg
    run(ebay_store_id=ebay_store_id, task_id=task_id)


def run(ebay_store_id, task_id):
    list_ebay(ebay_store_id=ebay_store_id, task_id=task_id)

__maxed_out = False

def __do_list(handler, ebay_store, parent_asin):
    amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin)
    ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store.id, asin=parent_asin)
    succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
    if maxed_out:
        __maxed_out = maxed_out
    return succeed

def list_ebay(ebay_store_id, task_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    __cached_asins = {}

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not ebay_store:
        print("No ebay store found. Ending process...")
        return False

    handler = ListingHandler(ebay_store=ebay_store)
    
    for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id, ebay_store_id=ebay_store_id)):
        if t.parent_asin not in __cached_asins:
            __do_list(handler=handler, ebay_store=ebay_store, parent_asin=t.parent_asin)
            __cached_asins[t.parent_asin] = True

        if __maxed_out:
            print("[{}] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION".format(ebay_store.username))
            break
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
