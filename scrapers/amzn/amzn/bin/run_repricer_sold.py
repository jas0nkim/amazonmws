import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import datetime
import getopt

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'run_repricer_sold.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'run_repricer_sold.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)

def __get_ordered_asins(premium=False):
    """ pass parent asin if exists
    """
    asins = []

    # get all orders in 6 hours
    orders = []
    if premium:
        orders = EbayOrderModelManager.fetch(created_at__gte=(datetime.datetime.now() - datetime.timedelta(hours=6)), ebay_store_id__in=[1, 5, 6, 7])
    else:
        orders = EbayOrderModelManager.fetch(created_at__gte=(datetime.datetime.now() - datetime.timedelta(hours=6)))
    
    if len(orders) < 1:
        return asins

    for order in orders:
        ordered_items = EbayOrderItemModelManager.fetch(ebay_order=order)
        if len(ordered_items) < 1:
            continue
        for ordered_item in ordered_items:
            parent_asin = AmazonItemModelManager.find_parent_asin(asin=ordered_item.sku)
            if parent_asin and not parent_asin in asins:
                asins.append(parent_asin)
    return asins

def run(premium):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = __get_ordered_asins(premium=premium)

    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_pricewatch', asins=asins, premium=premium)
        process.start()
    else:
        logger.error('No amazon items found')


if __name__ == "__main__":
    main(sys.argv[1:])
