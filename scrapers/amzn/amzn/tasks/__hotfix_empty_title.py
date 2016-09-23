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


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'hotfix_empty_title.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'hotfix_empty_title.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)


def run(premium):

    task_id = uuid.uuid4()
    ebay_store_id = 1

    if scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id):
        list_to_ebay(task_id=task_id, ebay_store_id=ebay_store_id)


def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = [ a.asin for a in amazonmws_utils.queryset_iterator(AmazonItemModelManager.fetch(title='')) ]

    # scrape amazon items
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


def list_to_ebay(task_id, ebay_store_id):
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
        if not ebay_item:
            continue # no new listing allowed
        succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
