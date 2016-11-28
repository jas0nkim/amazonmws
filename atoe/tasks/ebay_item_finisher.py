import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

__ebids = [
    '282193558580',
]

__ebay_store = 1

__cache_parent_asin = {}

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_item_finisher.py'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_item_finisher.py'
            sys.exit()
    run()

def run():
    ebay_items = EbayItemModelManager.fetch(ebid__in=__ebids, ebay_store_id=__ebay_store)
    counter = 0

    # amazon_items = AmazonItemModelManager.fetch(title__icontains='halloween')
    # print("num of custume amazon items - " + str(amazon_items.count()))

    for ebay_item in ebay_items:

    # for amazon_item in amazon_items:
        # if counter > 3:
        #     break
        # if amazon_item.parent_asin in __cache_parent_asin:
        #     continue
        # __cache_parent_asin[amazon_item.parent_asin] = True
        # ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=__ebay_store, asin=amazon_item.parent_asin)
        # if not ebay_item:
        #     continue
        handler = ListingHandler(ebay_store=ebay_item.ebay_store)
        if handler.end_item(ebay_item=ebay_item, delete=True):
            counter += 1
    print("{} number of items have been ended or oos.".format(counter))


if __name__ == "__main__":
    main(sys.argv[1:])
