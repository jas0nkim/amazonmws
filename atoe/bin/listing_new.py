import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import datetime
import csv

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *
from amazonmws.errors import GetOutOfLoop

from atoe.helpers import ListingHandler

if __name__ == "__main__":
    ebay_store_id = 3
    ebay_store_username = u'wbjworld'
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)

    asins_exclude = []
    with open(os.path.join(amazonmws_settings.TEMP_PATH, '_asins_exclude.csv'), 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            asins_exclude.append(amazonmws_utils.str_to_unicode(row[0]).strip())


    handler = ListingHandler(ebay_store, asins_exclude=asins_exclude)
    amazon_items = AmazonItemModelManager.fetch(created_at__gte=datetime.datetime(2016, 1, 28, 0, 0))
    for amazon_item in amazon_items:
        succeed, maxed_out = handler.run_each(amazon_item=amazon_item)
        if maxed_out:
            raise GetOutOfLoop("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
    