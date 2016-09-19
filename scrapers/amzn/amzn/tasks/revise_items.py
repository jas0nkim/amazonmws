import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

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

from atoe.helpers import ListingHandler

__asins = []

__ebay_store_id = 1


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'revise_items.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'revise_items.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)


def run(premium):

    task_id = uuid.uuid4()
    ebay_store_id = __ebay_store_id

    if scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id):
        revise_ebay_items(task_id=task_id, ebay_store_id=ebay_store_id)


def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = __asins if len(__asins) > 0 else EbayItemModelManager.fetch_distinct_asin(ebay_store_id=ebay_store_id, status__in=[1, 2,])

    # scrape amazon items (variations)
    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin',
            asins=asins,
            dont_parse_pictures=True,
            dont_parse_variations=True,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True


def revise_ebay_items(task_id, ebay_store_id):
    # list to ebay store

    asins = [ t.asin for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id, ebay_store_id=ebay_store_id)) ]

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    for asin in asins:
        amazon_item = AmazonItemModelManager.fetch_one(asin)
        if not amazon_item:
            logger.info("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, asin))
            continue
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=asin)
        handler.revise_item(ebay_item=ebay_item)


if __name__ == "__main__":
    main(sys.argv[1:])
