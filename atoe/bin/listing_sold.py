import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import csv
import getopt

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

def main(argv):
    order = 'most'
    try:
        opts, args = getopt.getopt(argv, "ho:", ["order=",])
    except getopt.GetoptError:
        print 'listing_sold.py -o <most|recent>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'listing_sold.py -o <most|recent>'
            sys.exit()
        elif opt in ("-o", "--order"):
            order = arg
    run(order)

def run(order):
    max_items = 100

    ebay_store_id = 1
    ebay_store_username = u'redflagitems777'
    ebay_store = EbayStoreModelManager.fetch_one(username=ebay_store_username)

    # handler = ListigHandler(ebay_store)
    handler = ListingHandler(ebay_store, asins_exclude=[u'B00NHPGW8Y', u'B011E1XQ54', u'B00NW2Q6ZG', u'B00WI0G7GG',])
    handler.run_sold(order, max_items)


if __name__ == "__main__":
    main(sys.argv[1:])
