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

# __ebids = [
#     '281840466843',
#     '281840465635',
#     '281876584135',
#     '281876584009',
# ]

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
    # ebay_items = EbayItemModelManager.fetch(ebid__in=__ebids, ebay_store_id=__ebay_store)
    counter = 0
    amazon_items = AmazonItemModelManager.fetch(title__icontains='halloween')
    print("num of custume amazon items - " + str(amazon_items.count()))
    for amazon_item in amazon_items:
        # if counter > 3:
        #     break
        if amazon_item.parent_asin in __cache_parent_asin:
            continue
        __cache_parent_asin[amazon_item.parent_asin] = True
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=__ebay_store, asin=amazon_item.parent_asin)
        if not ebay_item:
            continue
        ebay_action = EbayItemAction(ebay_store=ebay_item.ebay_store, ebay_item=ebay_item)
        succeed = ebay_action.end_item()
        if succeed:
            print("[{}] Ended at ebay.com".format(ebay_item.ebid))
            EbayItemModelManager.inactive(ebay_item=ebay_item)
            print("[{}] Inactived on DB".format(ebay_item.ebid))
        else:
            # fallback to oos
            # check the ebay item has variations
            variations = EbayItemModelManager.fetch_variations(ebay_item=ebay_item)
            if not variations or variations.count() < 1:
                success = ebay_action.oos_item(asin=ebay_item.asin)
                if success:
                    print("[{}] OOS at ebay.com".format(ebay_item.ebid))
                    EbayItemModelManager.oos(ebay_item=ebay_item)
                    print("[{}] OOS on DB".format(ebay_item.ebid))
            else:
                for variation in variations:
                    _s = ebay_action.oos_item(asin=variation.asin)
                    if _s:
                        print("[{}|{}] OOS variation at ebay.com".format(ebay_item.ebid, variation.asin))
                        EbayItemVariationModelManager.oos(variation=variation)
                        print("[{}|{}] OOS variation on db".format(ebay_item.ebid, variation.asin))
        counter += 1
    print("{} number of items have been ended or oos.".format(counter))


if __name__ == "__main__":
    main(sys.argv[1:])
