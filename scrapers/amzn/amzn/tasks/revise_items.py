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

    # get distinct parent asins
    parent_asins = __asins if len(__asins) > 0 else EbayItemModelManager.fetch_distinct_parent_asins(ebay_store_id=ebay_store_id, status__in=[1, 2,])

    parent_apparel_asins = []

    # scrape amazon items (variations)
    if len(parent_asins) > 0:
        _parent_apparel_asins = AmazonItemModelManager.fetch_distinct_parent_asins_apparel_only(parent_asin__in=parent_asins)
        for _p_asin in _parent_apparel_asins:
            if not AmazonItemApparelModelManager.fetch_one(parent_asin=_p_asin):
                parent_apparel_asins.append(_p_asin)

        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin',
            asins=parent_asins,
            dont_parse_pictures=False,
            dont_parse_variations=False,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium)
        process.crawl('amazon_apparel',
            asins=parent_apparel_asins,
            premium=premium)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True

def __do_revise(ebay_store, asin):
    ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store.id, asin=asin)
    if not ebay_item:
        logger.info("[%s|ASIN:%s] Failed to fetch an ebay item with given asin" % (ebay_store.username, asin))
        continue
    handler = ListingHandler(ebay_store)
    success, maxed = handler.revise_item(ebay_item=ebay_item)
    return success


def revise_ebay_items(task_id, ebay_store_id):
    # list to ebay store
    # get distinct parent asins
    _cache_asins = {}

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id, ebay_store_id=ebay_store_id))
        if t.parent_asin not in _cache_asins:
            __do_revise(ebay_store=ebay_store, asin=t.parent_asin)
            _cache_asins[t.parent_asin] = True
        if t.asin not in _cache_asins:
            __do_revise(ebay_store=ebay_store, asin=t.asin)
            _cache_asins[t.asin] = True

if __name__ == "__main__":
    main(sys.argv[1:])
