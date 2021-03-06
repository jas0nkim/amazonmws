import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import csv
import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

def main(argv):
    order = 'most'
    restockonly = False
    try:
        opts, args = getopt.getopt(argv, "hro:", ["order=", "restockonly="])
    except getopt.GetoptError:
        print 'listing_sold.py -r -o <most|recent>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'listing_sold.py -r -o <most|recent>'
            sys.exit()
        elif opt in ("-r", "--restockonly"):
            restockonly = True
        elif opt in ("-o", "--order"):
            order = arg
    run(order, restockonly)

def run(order, restockonly):
    max_items = None
    ebay_stores = EbayStoreModelManager.fetch()

    for ebay_store in ebay_stores:
        if ebay_store.id not in [1,]:
            continue
        # handler = ListingHandler(ebay_store, asins_exclude=[u'B00NHPGW8Y', u'B011E1XQ54', u'B00NW2Q6ZG', u'B00WI0G7GG', u'B00CMNX5YG', u'B00K2XX4OY', u'B00VMB5VB4', ])
        handler = ListingHandler(ebay_store)
        handler.run_sold(order, restockonly, max_items)


if __name__ == "__main__":
    main(sys.argv[1:])
