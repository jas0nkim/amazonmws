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
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)

    handler = ListingHandler(ebay_store)

    trans = TransactionModelManager.fetch(ebay_store_id=ebay_store_id)
    if trans.count() > 0:
        for tran in trans:
            ebay_item = EbayItemModelManager.fetch_one(ebid=tran.item_id)
            if not ebay_item:
                continue
            amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
            if not amazon_item:
                continue
            succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
            if maxed_out:
                logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
                break
