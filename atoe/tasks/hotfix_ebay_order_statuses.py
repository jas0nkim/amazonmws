import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *

from atoe.actions import EbayOrderAction


__ebay_stores = [1, ]

def __update_order_status_if_exists(ebay_store, since_hours_ago=4):
    action = EbayOrderAction(ebay_store=ebay_store)
    orders = action.get_orders(modified=True, since_hours_ago=since_hours_ago)
    
    for moded_order in orders:
        try:
            # check order already stored in db
            _existed_order = EbayOrderModelManager.fetch_one(order_id=moded_order.OrderID)
            if _existed_order.order_status == moded_order.OrderStatus:
                continue

            ebay_order = EbayOrderModelManager.update(order=_existed_order, 
                order_status=moded_order.OrderStatus)

        except Exception as e:
            logger.exception("Failed to save ebay order - {}".format(str(e)))
            continue

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'ebay_orders_fetcher.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'ebay_orders_fetcher.py'
            sys.exit()
    run()

def run():
    for ebay_store_id in __ebay_stores:
        ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
        if not ebay_store:
            continue
        since_hours_ago = 720
        __update_order_status_if_exists(ebay_store, since_hours_ago)


if __name__ == "__main__":
    main(sys.argv[1:])
