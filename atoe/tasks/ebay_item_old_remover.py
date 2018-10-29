import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt
import datetime

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

__cache_parent_asin = {}

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'ebay_item_old_remover.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_item_old_remover.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)

def run(ebay_store_id):
    old_ebay_items = EbayItemModelManager.fetch(ebay_store_id=ebay_store_id, status=1, created_at__lt=datetime.datetime.now() - datetime.timedelta(days=540))
    counter = 0

    print("total number of ebay items to remove: {}".format(old_ebay_items.count()))

    # amazon_items = AmazonItemModelManager.fetch(title__icontains='halloween')
    # print("num of custume amazon items - " + str(amazon_items.count()))

    for ebay_item in old_ebay_items:

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
    print("{} number of ebay items have been ended.".format(counter))


if __name__ == "__main__":
    main(sys.argv[1:])
