import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler


if __name__ == "__main__":
    asins = [
        u'B00LDGV15I',
        u'B002M9D4HI',
        u'B00P1HU2WI',
        u'B013WBBJF8',
        u'B00EZTCW94',
        u'B00UAHKCWE',
        u'B00VDVW9YK',
        u'B004Y6BH6W',
        u'B000J09OLM',
        u'B00UW2SP80',
        u'B00GNB3MRI',
        u'B0072H60MG',
        u'B0013JPVN8',
        u'B00D5P846Y',
        u'B00KG6Z972',
        u'B00QCAGVFA',
        u'B00U9RWQMY',
        u'B001W2WKS0',
        u'B00JCW8D38',
        u'B00QPHW63G',
        u'B00GJMYDK6',
        u'B00RQLC7GQ',
        u'B002M782UO',
        u'B00Y2BGFIO',
        u'B00LD6UCCG',
        u'B00KWR2BCQ',
        u'B00MUZVKY8',
    ]

    ebay_store_id = 1
    ebay_store_username = u'redflagitems777'
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)
    handler = ListingHandler(ebay_store)

    for asin in asins:
        amazon_item = AmazonItemModelManager.fetch_one(asin)
        if not amazon_item:
            logger.info("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, asin))
            continue
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=asin)
        succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break
