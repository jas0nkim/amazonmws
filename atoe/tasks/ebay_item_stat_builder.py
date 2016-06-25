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

from atoe.actions import EbayItemAction

__ebay_stores = [1, 5, 6, ]

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_item_stat_builder.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_item_stat_builder.py'
            sys.exit()
    run()

def run():
    ebay_items = EbayItemModelManager.fetch(status__in=[ 1, 2, ], ebay_store_id__in=__ebay_stores)

    for ebay_item in ebay_items:
        action = EbayItemAction(ebay_store=ebay_item.ebay_store)
        item = action.fetch_one_item(ebay_item_id=ebay_item.id, include_watch_count=True)
        if not item:
            continue
        EbayItemStatModelManager.create(ebid=ebay_item.ebid,
            clicks=item['HitCount'],
            watches=item['WatchCount'],
            solds=item['SellingStatus']['QuantitySold']
        )


if __name__ == "__main__":
    main(sys.argv[1:])
