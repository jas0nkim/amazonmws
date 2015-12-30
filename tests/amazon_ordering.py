import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ao', 'src'))

from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler


if __name__ == "__main__":

    # ebay_store = EbayStoreModelManager.fetch_one(username=u'redflagitems777')
    # transactions = TransactionModelManager.fetch(ebay_store_id=1)
    # for transaction in transactions:
    #     if transaction:
    #         break
    # asin = u'B003IG8RQW'

    ebay_store = EbayStoreModelManager.fetch_one(username=u'redflagitems777')
    transaction = TransactionModelManager.fetch_one(id=2259)
    ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.item_id)

    ordering_handler = AmazonOrderingHandler(ebay_store=ebay_store, ebay_transaction=transaction, asin=ebay_item.asin)
    ordering_handler.run()
