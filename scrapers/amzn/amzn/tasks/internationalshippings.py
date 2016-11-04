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
    # Clothing, Shoes & Jewelry : Women : Clothing : Sweaters : AmazonGlobal Eligible : Exclude Add-on
    'https://www.amazon.com/s/ref=sr_st_review-rank?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044456%2Cp_n_shipping_option-bin%3A3242350011%2Cp_n_is-min-purchase-required%3A5016683011&qid=1478272653&bbn=1040660&sort=review-rank',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__max_amazon_price = None
__min_amazon_price = None
__max_page = 10

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'internationalshippings.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'internationalshippings.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)


def run(ebay_store_id):
    task_id = uuid.uuid4()
    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True
    scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id)

def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls = __start_urls
    max_amazon_price = __max_amazon_price
    min_amazon_price = __min_amazon_price
    max_page = __max_page

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_global',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            list_new=True,
            max_amazon_price=max_amazon_price,
            min_amazon_price=min_amazon_price,
            max_page=max_page,
            international_shipping=True)
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
        amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=p_asin)
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=p_asin)
        succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
