import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import csv

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

if __name__ == "__main__":
    ebay_store_id = 2
    ebay_store_username = u'kat.burr'
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)

    handler = ListingHandler(ebay_store)

    with open(os.path.join(amazonmws_settings.TEMP_PATH, '_new_listing.csv'), 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            asin = amazonmws_utils.str_to_unicode(row[0]).strip()
            amazon_item = AmazonItemModelManager.fetch_one(asin)
            if not amazon_item:
                logger.info("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, asin))
                continue
            ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=asin)
            succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
            if maxed_out:
                logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
                break