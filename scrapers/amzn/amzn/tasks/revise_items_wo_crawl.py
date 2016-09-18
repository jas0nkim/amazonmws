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
    asins = __asins if len(__asins) > 0 else EbayItemModelManager.fetch_distinct_asin(ebay_store_id=ebay_store_id, status__in=[1, 2,])

    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    for asin in asins:
        amazon_item = AmazonItemModelManager.fetch_one(asin)
        if not amazon_item:
            logger.info("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, asin))
            continue
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=asin)
        handler.revise_item(ebay_item=ebay_item)
        handler.revise_item(ebay_item=ebay_item, pictures=AmazonItemPictureModelManager.fetch(asin=asin))


if __name__ == "__main__":
    main(sys.argv[1:])
