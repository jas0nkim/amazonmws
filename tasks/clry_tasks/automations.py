import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ao', 'src'))

from storm.exceptions import StormError

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler, AmazonOrderTrackingHandler

from celery import Celery

app = Celery('automations', broker='amqp://{}:{}@{}:{}/{}'.format(
        amazonmws_settings.APP_RABBITMQ_USERNAME, 
        amazonmws_settings.APP_RABBITMQ_PASSWORD, 
        amazonmws_settings.APP_RABBITMQ_HOST, 
        amazonmws_settings.APP_RABBITMQ_PORT, 
        amazonmws_settings.APP_RABBITMQ_VHOST))

@app.task
def ordering_task(transaction_id):

    transaction = TransactionModelManager.fetch_one(id=transaction_id)
    ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)
    ebay_item = EbayItemModelManager.fetch_one(ebid=transaction.item_id)

    ordering_handler = AmazonOrderingHandler(ebay_store=ebay_store, ebay_transaction=transaction, asin=ebay_item.asin)
    ordering_handler.run()

@app.task
def order_tracking_task(transaction_id):

    transaction = TransactionModelManager.fetch_one(id=transaction_id)
    ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)

    ordering_handler = AmazonOrderTrackingHandler(ebay_store=ebay_store, ebay_transaction=transaction)
    ordering_handler.run()

