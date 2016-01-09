import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ao', 'src'))

from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler

from celery import Celery

app = Celery('automations', broker='amqp://guest@localhost//')

@app.task
def ordering_task(transaction_id):
    # ebay_store = EbayStoreModelManager.fetch_one(username=u'redflagitems777')
    # transactions = TransactionModelManager.fetch(ebay_store_id=1)
    # for transaction in transactions:
    #     if transaction:
    #         break
    # asin = u'B003IG8RQW'

    transaction = TransactionModelManager.fetch_one(id=transaction_id)
    ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)
    ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.item_id)

    ordering_handler = AmazonOrderingHandler(ebay_store=ebay_store, ebay_transaction=transaction, asin=ebay_item.asin)
    ordering_handler.run()

