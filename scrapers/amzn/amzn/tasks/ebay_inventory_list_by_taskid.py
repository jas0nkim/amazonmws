import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt
import uuid

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import InventoryListingHandler


def main(argv):
    ebay_store_id = 1
    task_id = None
    max_num = -1
    try:
        opts, args = getopt.getopt(argv, "he:t:m:", ["ebaystoreid=", "taskid=", "maxnum="])
    except getopt.GetoptError:
        print 'ebay_inventory_list_by_taskid.py -e <1|2|3|4|...ebaystoreid> -t <taskid> -m <maxnum>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_inventory_list_by_taskid.py -e <1|2|3|4|...ebaystoreid> -t <taskid> -m <maxnum>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
        elif opt in ("-t", "--taskid"):
            task_id = arg
        elif opt in ("-m", "--maxnum"):
            max_num = int(arg)
    run(ebay_store_id=ebay_store_id, task_id=task_id, max_num=max_num)

def run(ebay_store_id, task_id, max_num):
    list_to_ebay(ebay_store_id=ebay_store_id, task_id=task_id, max_num=max_num)

__maxed_out = False

def __do_list(handler, ebay_store, parent_asin):
    already_listed = False
    amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=parent_asin)
    for amazon_item in amazon_items:
        if EbayOfferModelManager.is_published(sku=amazonmws_settings.EBAY_SKU_AMAZON_PREFIX + amazon_item.asin, marketplace_id=amazonmws_settings.EBAY_MARKETPLACE_US):
            already_listed = True
            continue
    if already_listed:
        return False
    succeed, maxed_out = handler.list(amazon_items=amazon_items)
    if maxed_out:
        __maxed_out = maxed_out
    return succeed



    # ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store.id, asin=parent_asin)
    # succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
    # if maxed_out:
    #     __maxed_out = maxed_out
    # return not ebay_item and succeed

def list_to_ebay(ebay_store_id, task_id, max_num=-1):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    __cached_asins = {}

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not ebay_store:
        print("No ebay store found. Ending process...")
        return False

    counter = 0
    handler = InventoryListingHandler(ebay_store=ebay_store)
    for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id)):
        if t.parent_asin not in __cached_asins:
            if __do_list(handler=handler, ebay_store=ebay_store, parent_asin=t.parent_asin):
                print("[{}] CURRENT LISTED COUNT - {}".format(ebay_store.username, counter))
                counter += 1
            __cached_asins[t.parent_asin] = True

        if max_num > 0 and max_num < counter:
            print("[{}] STOP LISTING - REACHED MAX NUMBER LISTING - {}".format(ebay_store.username, max_num))
            break

        if __maxed_out:
            print("[{}] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION".format(ebay_store.username))
            break
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
