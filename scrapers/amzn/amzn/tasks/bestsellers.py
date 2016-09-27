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

__start_urls = [

    # Best Sellers in Toys & Games
    'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0',
]

__ebay_store_id = 1

__min_amazon_rating = 4.0

def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'bestsellers.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'bestsellers.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)


def run(premium):

    task_id = uuid.uuid4()
    ebay_store_id = __ebay_store_id

    if scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id):
        list_to_ebay(task_id=task_id, ebay_store_id=ebay_store_id)

def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls = __start_urls
    min_amazon_rating = __min_amazon_rating

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_bestseller',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            min_amazon_rating=min_amazon_rating)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True


def list_to_ebay(task_id, ebay_store_id):
    # list to ebay store
    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    # get distinct parent_asin
    parent_asins = list(set([ t.parent_asin for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id, ebay_store_id=ebay_store_id)) ]))

    # find all amazon items (asin) have same parent_asin
    for p_asin in parent_asins:
        amazon_items = AmazonItemModelManager.fetch(parent_asin=p_asin)
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=p_asin)
        succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
