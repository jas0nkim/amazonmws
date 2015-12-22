import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ao', 'src'))

import json
from decimal import Decimal
import datetime

from flask import Flask
from flask import request

from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.models import StormStore, EbayStore, Transaction
from amazonmws.errors import record_notification_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from automatic.amazon.helpers import AmazonOrderingHandler


application = Flask(__name__)

@application.route("%s%s" % (settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, "/GetItem"), methods=['POST'])
def get_item_handler():
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'python_restful_test'))

    # post values
    Timestamp = request.form['Timestamp']
    Ack = request.form['Ack']
    CorrelationID = request.form['CorrelationID']
    Version = request.form['Version']
    Build = request.form['Build']
    NotificationEventName = request.form['NotificationEventName']
    RecipientUserID = request.form['RecipientUserID']
    Item = request.form['Item']
    raw = request.form['raw']

    logger.debug('%s [GetItem] - raw: %s' % (NotificationEventName, raw))

    if Ack != "Success":
        record_notification_error(
            CorrelationID,
            NotificationEventName,
            RecipientUserID,
            raw
        )

    return Ack

@application.route("%s%s" % (settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, "/GetItemTransactions"), methods=['POST'])
def get_item_transactions_handler():
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'python_restful_test'))

    # post values
    Timestamp = request.form['Timestamp']
    Ack = request.form['Ack']
    CorrelationID = request.form['CorrelationID']
    Version = request.form['Version']
    Build = request.form['Build']
    NotificationEventName = request.form['NotificationEventName']
    RecipientUserID = request.form['RecipientUserID']
    EIASToken = request.form['EIASToken']
    PaginationResult = request.form['PaginationResult']
    HasMoreTransactions = request.form['HasMoreTransactions']
    TransactionsPerPage = request.form['TransactionsPerPage']
    PageNumber = request.form['PageNumber']
    ReturnedTransactionCountActual = request.form['ReturnedTransactionCountActual']
    Item = request.form['Item']
    TransactionArray = request.form['TransactionArray']
    PayPalPreferred = request.form['PayPalPreferred']
    raw = request.form['raw']

    logger.debug('%s [GetItemTransactions] - raw: %s' % (NotificationEventName, raw))
    
    if Ack != "Success":
        record_notification_error(
            CorrelationID,
            NotificationEventName,
            RecipientUserID,
            raw
        )

    if NotificationEventName == 'AuctionCheckoutComplete':
        # store in database
        try:
            Item_data = json.loads(Item)
        except ValueError:
            logger.exception("Failed to load Item json - %s" % Item)
        try:
            TransactionArray_data = json.loads(TransactionArray)
            Transaction_data = TransactionArray_data["Transaction"]
        except ValueError:
            logger.exception("Failed to load TransactionArray json - %s" % TransactionArray)
        
        ebay_store = EbayStoreModelManager.fetch_one(username=RecipientUserID)
        if not ebay_store:
            logger.error("No ebay store found from system. Terminating...")
            return Ack
        # create transaction entry
        transaction = TransactionModelManager.create(ebay_store.id, RecipientUserID, 
            Item_data["ItemID"], Transaction_data, Item, TransactionArray, raw)

        ebay_item = EbayItemModelManager.fetch_one(ebid=Item_data["ItemID"])
        if not ebay_item:
            logger.error("No ebay item found from system. Terminating...")
            return Ack
        # reduce ebay item quantity in db only - make oos if necessary
        EbayItemModelManager.reduce_quantity(ebay_item)

        #
        # temp - testing purpose...
        # 
        if ebay_store.id == 1:

            # make order to amazon
            ordering_handler = AmazonOrderingHandler(ebay_store, transaction, ebay_item.asin)
            ordering_handler.run()

    return Ack


if __name__ == "__main__":
    application.run(host=settings.APP_HOST, port=8091, debug=True)
