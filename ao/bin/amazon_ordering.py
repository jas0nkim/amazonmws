import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import time

from storm.exceptions import StormError

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler


if __name__ == "__main__":
    lock_filename = 'ordering.lock'
    amazonmws_utils.check_lock(lock_filename)

    try:
        today = time.strftime("%Y-%m-%d 00:00:00")
        transactions = TransactionModelManager.fetch_not_ordered(since=today)

        for transaction in transactions:
            try:
                ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)
                ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.item_id)

                if ebay_store and ebay_item:
                    if ebay_store.id != 1:
                        continue
                    ordering_handler = AmazonOrderingHandler(ebay_store, transaction, ebay_item.asin)
                    ordering_handler.run()
                else:
                    continue
            
            except StormError:
                continue
    finally:
        amazonmws_utils.release_lock(lock_filename)
