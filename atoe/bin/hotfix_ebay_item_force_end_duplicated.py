import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import re
import datetime
from decimal import Decimal

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction


def _revise_item_end(ebay_store, ebay_item):
    amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
    if not amazon_item:
        return False

    action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
    succeed = action.end_item()
    if succeed:
        EbayItemModelManager.inactive(ebay_item=ebay_item)
        return True
    return False


if __name__ == "__main__":
    store = EbayStoreModelManager.fetch_one(id=3)

    ebay_items = EbayItemModelManager.fetch_distinct_asin(ebay_store_id=store.id, 
        created_at__gte=datetime.datetime(2016, 1, 28, 0, 0))

    for ebay_item in ebay_items:
        dup_ebay_items = EbayItemModelManager.fetch(ebay_store_id=store.id, asin=ebay_item.asin)
        if dup_ebay_items.count() > 1:
            _revise_item_end(ebay_store=store, ebay_item=dup_ebay_items.any())
