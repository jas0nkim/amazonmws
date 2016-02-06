import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ao', 'src'))

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler, AmazonOrderTrackingHandler

from atoe.helpers import ListingHandler

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

@app.task
def listing_single_item_task(transaction_id, ebay_item_id):
    transaction = TransactionModelManager.fetch_one(id=transaction_id)
    if not transaction:
        logger.error("[TRANSID:%s] No ebay transaction found from system. Terminating..." % transaction_id)
        return False

    ebay_store = EbayStoreModelManager.fetch_one(username=transaction.seller_user_id)
    if not ebay_store:
        logger.error("[%s] No ebay store found from system." % transaction.seller_user_id)
        return False

    ebay_item = EbayItemModelManager.fetch_one(ebid=ebay_item_id)
    if not ebay_item:
        logger.error("[%s|EBID:%s] No ebay item found from system." % (ebay_store.username, ebay_item_id))
        return False

    amazon_item = AmazonItemModelManager.fetch_one(ebay_item.asin)
    if not amazon_item:
        logger.error("[%s|ASIN:%s] Failed to fetch an amazon item with given asin" % (ebay_store.username, ebay_item.asin))
        return False
    
    handler = ListingHandler(ebay_store)
    succeed, maxed_out = handler.run_each(amazon_item, ebay_item)
    if not succeed:
        logger.info("[%s|EBID:%s] Failed to listing ebay" % (ebay_store.username, ebay_item_id))
        return False

    return True
