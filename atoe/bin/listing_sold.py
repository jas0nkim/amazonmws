import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import csv

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

if __name__ == "__main__":
    ebay_store_id = 1
    ebay_store_username = u'redflagitems777'
    # ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username, asins_exclude=[u'B00NHPGW8Y', u'B011E1XQ54',])

    handler = ListingHandler(ebay_store)

    _asin_cache = {}

    # trans = TransactionModelManager.fetch(ebay_store_id=ebay_store_id, order_by='created_at', order_desc=True)
    trans = TransactionModelManager.fetch(order_by='created_at', order_desc=True)
    if trans.count() > 0:
        for tran in trans:
            ebay_item = EbayItemModelManager.fetch_one(ebid=tran.item_id)
            if not ebay_item:
                continue
            
            if ebay_item.asin not in _asin_cache:
                _asin_cache[ebay_item.asin] = True
            else:
                continue
            
            amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
            if not amazon_item:
                continue
            succeed, maxed_out = handler.run_each__solditems(amazon_item, ebay_item)
            if maxed_out:
                logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
                break
