import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

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

    logger.debug('%s [GetItem] - Timestamp: %s' % (NotificationEventName, Timestamp))
    logger.debug('%s [GetItem] - Ack: %s' % (NotificationEventName, Ack))
    logger.debug('%s [GetItem] - CorrelationID: %s' % (NotificationEventName, CorrelationID))
    logger.debug('%s [GetItem] - Version: %s' % (NotificationEventName, Version))
    logger.debug('%s [GetItem] - Build: %s' % (NotificationEventName, Build))
    logger.debug('%s [GetItem] - NotificationEventName: %s' % (NotificationEventName, NotificationEventName))
    logger.debug('%s [GetItem] - RecipientUserID: %s' % (NotificationEventName, RecipientUserID))
    logger.debug('%s [GetItem] - Item: %s' % (NotificationEventName, Item))
    logger.debug('%s [GetItem] - raw: %s' % (NotificationEventName, raw))
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

    logger.debug('%s [GetItemTransactions] - Timestamp: %s' % (NotificationEventName, Timestamp))
    logger.debug('%s [GetItemTransactions] - Ack: %s' % (NotificationEventName, Ack))
    logger.debug('%s [GetItemTransactions] - CorrelationID: %s' % (NotificationEventName, CorrelationID))
    logger.debug('%s [GetItemTransactions] - Version: %s' % (NotificationEventName, Version))
    logger.debug('%s [GetItemTransactions] - Build: %s' % (NotificationEventName, Build))
    logger.debug('%s [GetItemTransactions] - NotificationEventName: %s' % (NotificationEventName, NotificationEventName))
    logger.debug('%s [GetItemTransactions] - RecipientUserID: %s' % (NotificationEventName, RecipientUserID))
    logger.debug('%s [GetItemTransactions] - EIASToken: %s' % (NotificationEventName, EIASToken))
    logger.debug('%s [GetItemTransactions] - PaginationResult: %s' % (NotificationEventName, PaginationResult))
    logger.debug('%s [GetItemTransactions] - HasMoreTransactions: %s' % (NotificationEventName, HasMoreTransactions))
    logger.debug('%s [GetItemTransactions] - TransactionsPerPage: %s' % (NotificationEventName, TransactionsPerPage))
    logger.debug('%s [GetItemTransactions] - PageNumber: %s' % (NotificationEventName, PageNumber))
    logger.debug('%s [GetItemTransactions] - ReturnedTransactionCountActual: %s' % (NotificationEventName, ReturnedTransactionCountActual))
    logger.debug('%s [GetItemTransactions] - Item: %s' % (NotificationEventName, Item))
    logger.debug('%s [GetItemTransactions] - TransactionArray: %s' % (NotificationEventName, TransactionArray))
    logger.debug('%s [GetItemTransactions] - PayPalPreferred: %s' % (NotificationEventName, PayPalPreferred))
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
        
        ebay_store = get_ebay_store(RecipientUserID)

        if not ebay_store:
            logger.error("No ebay store found from system. Terminating...")
            return Ack

        try:
            trans = Transaction()
            trans.ebay_store_id = ebay_store.id
            trans.seller_user_id = RecipientUserID
            trans.transaction_id = Transaction_data["TransactionID"]
            trans.item_id = Item_data["ItemID"]
            trans.order_id = Transaction_data["ContainingOrder"]["OrderID"]
            trans.external_transaction_id = Transaction_data["ExternalTransaction"]["ExternalTransactionID"] if "ExternalTransactionID" in Transaction_data["ExternalTransaction"] else None
            trans.transaction_price = Decimal(Transaction_data["TransactionPrice"])
            trans.sales_tax_percent = Decimal(Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxPercent"]) if "SalesTaxPercent" in Transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_state = Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxState"] if "SalesTaxState" in Transaction_data["ShippingDetails"]["SalesTax"] else None
            trans.sales_tax_amount = trans.transaction_price * trans.transaction_price # because given number is CAD... don't know why...
            trans.amount_paid = Decimal(Transaction_data["AmountPaid"])
            trans.buyer_email = Transaction_data["Buyer"]["Email"] if "Email" in Transaction_data["Buyer"] else None
            trans.buyer_user_id = Transaction_data["Buyer"]["UserID"]
            trans.buyer_status = Transaction_data["Buyer"]["Status"]
            trans.buyer_shipping_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Name"]
            trans.buyer_shipping_street1 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street1"] if "Street1" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_street2 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street2"] if "Street2" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_city_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CityName"] if "CityName" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_state_or_province = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["StateOrProvince"] if "StateOrProvince" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Country"] if "Country" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_country_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CountryName"] if "CountryName" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_phone = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Phone"] if "Phone" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.buyer_shipping_postal_code = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["PostalCode"] if "PostalCode" in Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"] else None
            trans.order_status = Transaction_data["ContainingOrder"]["OrderStatus"]
            trans.ebay_payment_status = Transaction_data["Status"]["eBayPaymentStatus"] if "eBayPaymentStatus" in Transaction_data["Status"] else None
            trans.checkout_status = Transaction_data["Status"]["CheckoutStatus"] if "CheckoutStatus" in Transaction_data["Status"] else None
            trans.complete_status = Transaction_data["Status"]["CompleteStatus"] if "CompleteStatus" in Transaction_data["Status"] else None
            trans.payment_hold_status = Transaction_data["Status"]["PaymentHoldStatus"] if "PaymentHoldStatus" in Transaction_data["Status"] else None
            trans.external_transaction_status = Transaction_data["Status"]["ExternalTransactionStatus"] if "ExternalTransactionStatus" in Transaction_data["Status"] else None
            trans.raw_item = Item
            trans.raw_transactionarray = TransactionArray
            trans.raw_xml = raw
            trans.created_at = datetime.datetime.now()
            trans.updated_at = datetime.datetime.now()
            
            StormStore.add(trans)
            StormStore.commit()

        except StormError:
            logger.exception("Failed to store data")
            StormStore.rollback()
        except Exception, e:
            logger.exception(e)
            StormStore.rollback()

    return Ack

def get_ebay_store(ebay_user_id):
    ebay_store = None
    try:
        ebay_store = StormStore.find(EbayStore, EbayStore.username == ebay_user_id).one()
    except StormError, e:
        logger.exception("[ebay username: " + ebay_user_id + "] " + "Failed to fetch ebay store: " +  str(e))
    return ebay_store


if __name__ == "__main__":
    application.run(host=settings.APP_HOST, port=8091, debug=True)
