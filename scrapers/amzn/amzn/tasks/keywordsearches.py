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
    #  Electronics : Computers & Accessories : Laptop Accessories : Batteries : Prime Eligible : Exclude Add-on : Dell or HP : "laptop battery"
    'https://www.amazon.com/gp/search/ref=sr_nr_p_89_0?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A720576%2Ck%3Alaptop+battery%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_89%3ADell%7CHP&keywords=laptop+battery&ie=UTF8&qid=1472678826&rnid=2528832011',
]

__ebay_store_id = 1


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'keywordsearches.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'keywordsearches.py -s <basic|premium>'
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

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_keyword_search',
            start_urls=start_urls,
            # dont_parse_variations=False,
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

    asins = [ t.asin for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id)) ]

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    excl_brands = ExclBrandModelManager.fetch()

    for asin in asins:
        amazon_item = AmazonItemModelManager.fetch_one(asin)
        if not amazon_item:
            logger.info("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, asin))
            continue
        if not amazon_item.is_listable(ebay_store=ebay_store, excl_brands=excl_brands):
            logger.info("[%s|ASIN:%s] not listable amazon item" % (ebay_store.username, asin))
            continue

        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=asin)
        succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
