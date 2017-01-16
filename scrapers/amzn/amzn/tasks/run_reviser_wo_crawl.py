import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

# __premium_ebay_store_ids = [1, 5, 6, 7]

# __popularity_levels = {
#     'popular': 1,
#     'normal': 2,
#     'slow': 3,
# }

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print('run_reviser_wo_crawl.py -e <1|2|3|4|...ebaystoreid>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_reviser_wo_crawl.py -e <1|2|3|4|...ebaystoreid>')
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)

def run(ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()
    # get distinct parent asins

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    if not ebay_store:
        return False

    handler = ListingHandler(ebay_store=ebay_store)
    ebay_items = EbayItemModelManager.fetch(ebay_store_id=ebay_store_id, status__in=[1, 2, ])
    for ebay_item in ebay_items:
        ebay_item = handler.sync_item(ebay_item=ebay_item)
        if ebay_item:
            success, maxed_out = handler.revise_item(ebay_item=ebay_item)


if __name__ == "__main__":
    main(sys.argv[1:])
