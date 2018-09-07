import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime
import getopt
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


__premium_ebay_store_ids = [1, 8]

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'run_reviser_sold.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'run_reviser_sold.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)

def __get_ordered_asins(ebay_store_id):
    """
        ## NEW - pass parent asins of sold items - follow run_reviser.py

        ## OLD
        _asins format:
        i.e.
        _asins = [
            {
                'asin': 'ABEASDF381',
                'is_variation': False,
            },
            {
                'asin': 'ABEEBSDF38',
                'is_variation': True,
            },
            ...
        ]
    """
    asins = []

    # get all orders in 6 hours
    orders = EbayOrderModelManager.fetch(created_at__gte=(datetime.datetime.now(tz=amazonmws_utils.get_utc()) - datetime.timedelta(hours=6)), ebay_store_id=ebay_store_id)
    
    if len(orders) < 1:
        return asins

    for order in orders:
        ordered_items = EbayOrderItemModelManager.fetch(ebay_order=order)
        if len(ordered_items) < 1:
            continue
        for ordered_item in ordered_items:
            if not ordered_item.sku:
                continue
            if not ordered_item.sku or ordered_item.sku in asins:
                continue
            parent_asin = AmazonItemModelManager.find_parent_asin(asin=ordered_item.sku)
            if not parent_asin:
                parent_asin = ordered_item.sku
            asins.append(parent_asin)
    return asins

def run(ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    task_id = uuid.uuid4()

    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True

    asins = __get_ordered_asins(ebay_store_id=ebay_store_id)

    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_pricewatch',
            asins=asins,
            sync_ebay_item_first=True,
            premium=premium,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            revise_inventory_only=True,
            force_crawl=True)
        process.start()
    else:
        logger.error('No amazon items found')


if __name__ == "__main__":
    main(sys.argv[1:])
