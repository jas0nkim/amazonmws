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


def _revise_item_oos(ebay_store, ebay_item):
    amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
    if not amazon_item:
        return False

    action = EbayItemAction(ebay_store=ebay_store, ebay_item=ebay_item, amazon_item=amazon_item)
    succeed = action.revise_item(eb_price=None, quantity=0)
    if succeed:
        EbayItemModelManager.oos(ebay_item)
        return True
    return False


if __name__ == "__main__":
    store = EbayStoreModelManager.fetch_one(id=3)
    ebay_items_1 = EbayItemModelManager.fetch(ebay_store_id=store.id, 
        created_at__gte=datetime.datetime(2016, 1, 28, 0, 0),
        eb_price__lt=Decimal(store.listing_min_dollar) if store.listing_min_dollar else Decimal("0.00"))

    for ebay_item in ebay_items_1:
        _revise_item_oos(ebay_store=store, ebay_item=ebay_item)


    ebay_items_2 = EbayItemModelManager.fetch(ebay_store_id=store.id, 
        created_at__gte=datetime.datetime(2016, 1, 28, 0, 0),
        eb_price__gt=Decimal(store.listing_max_dollar) if store.listing_max_dollar else Decimal("999999999.99"))

    for ebay_item in ebay_items_2:
        _revise_item_oos(ebay_store=store, ebay_item=ebay_item)
