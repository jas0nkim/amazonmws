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

__ebay_stores = [1, 8]

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

def _is_active_ebay_item(ebay_item, _i):
    is_active = False
    try:
        if not _i:
            EbayItemModelManager.inactive(ebay_item=ebay_item)
            is_active = False
        elif _i.SellingStatus.ListingStatus in ['Ended', 'Completed', ]:
            EbayItemModelManager.inactive(ebay_item=ebay_item)
            is_active = False
        elif _i.SellingStatus.ListingStatus in ['Active', ]:
            EbayItemModelManager.reactive(ebay_item=ebay_item)
            is_active = True
        else:
            is_active = False
    except Exception as e:
        logger.exception("[EBID:" + ebay_item.ebid + "] " + str(e))
        print("ERROR [EBID:" + ebay_item.ebid + "] " + str(e))
        is_active = False
    return is_active

def run():

    for ebay_item in amazonmws_utils.queryset_iterator(EbayItemModelManager.fetch(ebay_store_id__in=__ebay_stores)):
    # ebay_items = EbayItemModelManager.fetch(status__in=[ 1, 2, ], ebay_store_id__in=__ebay_stores)

    # for ebay_item in ebay_items:
        action = EbayItemAction(ebay_store=ebay_item.ebay_store)
        item = action.fetch_one_item(ebid=ebay_item.ebid, include_watch_count=True)
        if not _is_active_ebay_item(ebay_item=ebay_item, _i=item):
            continue

        try:
            clicks = item.HitCount
        except AttributeError as e:
            logger.exception("[EBID:" + ebay_item.ebid + "] no HitCount: " + str(e))
            clicks = None

        try:
            watches = item.WatchCount
        except AttributeError as e:
            logger.exception("[EBID:" + ebay_item.ebid + "] no WatchCount: " + str(e))
            watches = None

        try:
            solds = item.SellingStatus.QuantitySold
        except AttributeError as e:
            logger.exception("[EBID:" + ebay_item.ebid + "] no SellingStatus.QuantitySold: " + str(e))
            solds = None

        try:
            EbayItemStatModelManager.create(ebay_store=ebay_item.ebay_store,
                ebid=ebay_item.ebid,
                clicks=clicks,
                watches=watches,
                solds=solds)
        except Exception as e:
            logger.exception("[EBID:" + ebay_item.ebid + "] " + str(e))
            continue


if __name__ == "__main__":
    main(sys.argv[1:])
