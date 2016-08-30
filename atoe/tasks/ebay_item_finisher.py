import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayItemAction

__ebids = [
    '281840466843',
    '281840465635',
    '281876584135',
    '281876584009',
]

__ebay_store = 1

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

    for ebay_item in ebay_items:
        ebay_action = EbayItemAction(ebay_store=ebay_item.ebay_store, ebay_item=ebay_item)
        succeed = ebay_action.end_item()

        if succeed:
            EbayItemModelManager.inactive(ebay_item=ebay_item)


if __name__ == "__main__":
    main(sys.argv[1:])
