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
    revise_ebay_items()

def revise_ebay_items():
    # list to ebay store
    ebay_store_id = __ebay_store_id
    
    # get distinct parent asins
    parent_asins = __asins if len(__asins) > 0 else AmazonItemModelManager.fetch_distinct_parent_asins_apparel_only()

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    for parent_asin in parent_asins:
        size_chart = AmazonItemApparelModelManager.get_size_chart(parent_asin=parent_asin)
        if not size_chart:
            continue
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=parent_asin)
        if not ebay_item:
            logger.info("[%s|ASIN:%s] Failed to fetch an ebay item with given asin" % (ebay_store.username, parent_asin))
            continue
        handler.revise_item_description(ebay_item=ebay_item)


if __name__ == "__main__":
    main(sys.argv[1:])
