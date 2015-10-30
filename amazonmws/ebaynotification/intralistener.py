import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import json

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

    logger.debug('GetItem - Timestamp: %s' % Timestamp)
    logger.debug('GetItem - Ack: %s' % Ack)
    logger.debug('GetItem - CorrelationID: %s' % CorrelationID)
    logger.debug('GetItem - Version: %s' % Version)
    logger.debug('GetItem - Build: %s' % Build)
    logger.debug('GetItem - NotificationEventName: %s' % NotificationEventName)
    logger.debug('GetItem - RecipientUserID: %s' % RecipientUserID)
    logger.debug('GetItem - Item: %s' % Item)
    logger.debug('GetItem - raw: %s' % raw)
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

    logger.debug('GetItemTransactions - Timestamp: %s' % Timestamp)
    logger.debug('GetItemTransactions - Ack: %s' % Ack)
    logger.debug('GetItemTransactions - CorrelationID: %s' % CorrelationID)
    logger.debug('GetItemTransactions - Version: %s' % Version)
    logger.debug('GetItemTransactions - Build: %s' % Build)
    logger.debug('GetItemTransactions - NotificationEventName: %s' % NotificationEventName)
    logger.debug('GetItemTransactions - RecipientUserID: %s' % RecipientUserID)
    logger.debug('GetItemTransactions - EIASToken: %s' % EIASToken)
    logger.debug('GetItemTransactions - PaginationResult: %s' % PaginationResult)
    logger.debug('GetItemTransactions - HasMoreTransactions: %s' % HasMoreTransactions)
    logger.debug('GetItemTransactions - TransactionsPerPage: %s' % TransactionsPerPage)
    logger.debug('GetItemTransactions - PageNumber: %s' % PageNumber)
    logger.debug('GetItemTransactions - ReturnedTransactionCountActual: %s' % ReturnedTransactionCountActual)
    logger.debug('GetItemTransactions - Item: %s' % Item)
    logger.debug('GetItemTransactions - TransactionArray: %s' % TransactionArray)
    logger.debug('GetItemTransactions - PayPalPreferred: %s' % PayPalPreferred)
    logger.debug('GetItemTransactions - raw: %s' % raw)
    
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

        try:
            trans = Transaction()
            trans.ebay_store_id = ebay_store.id
            trans.seller_user_id = RecipientUserID
            trans.transaction_id = Transaction_data["TransactionID"]
            trans.item_id = Item_data["ItemID"]
            trans.order_id = Transaction_data["ContainingOrder"]["OrderID"]
            trans.external_transaction_id = Transaction_data["ExternalTransaction"]["ExternalTransactionID"]
            trans.transaction_price = Transaction_data["TransactionPrice"]
            trans.sales_tax_percent = Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxPercent"]
            trans.sales_tax_state = Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxState"]
            trans.sales_tax_amount = Transaction_data["ShippingDetails"]["SalesTax"]["SalesTaxAmount"]
            trans.amount_paid = Transaction_data["AmountPaid"]
            trans.buyer_email = Transaction_data["Buyer"]["Email"]
            trans.buyer_user_id = Transaction_data["Buyer"]["UserID"]
            trans.buyer_status = Transaction_data["Buyer"]["Status"]
            trans.buyer_shipping_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Name"]
            trans.buyer_shipping_street1 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street1"]
            trans.buyer_shipping_street2 = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Street2"]
            trans.buyer_shipping_city_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CityName"]
            trans.buyer_shipping_state_or_province = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["StateOrProvince"]
            trans.buyer_shipping_country = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Country"]
            trans.buyer_shipping_country_name = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["CountryName"]
            trans.buyer_shipping_phone = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["Phone"]
            trans.buyer_shipping_postal_code = Transaction_data["Buyer"]["BuyerInfo"]["ShippingAddress"]["PostalCode"]
            trans.order_status = Transaction_data["ContainingOrder"]["OrderStatus"]
            trans.ebay_payment_status = Transaction_data["Status"]["eBayPaymentStatus"]
            trans.checkout_status = Transaction_data["Status"]["CheckoutStatus"]
            trans.complete_status = Transaction_data["Status"]["CompleteStatus"]
            trans.payment_hold_status = Transaction_data["Status"]["PaymentHoldStatus"]
            trans.external_transaction_status = Transaction_data["Status"]["ExternalTransactionStatus"]
            trans.raw_item = Item_data
            trans.raw_transactionarray = TransactionArray_data
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
        ebay_store = StormStore.find(EbayStore, EbayStore.username == ebay_user_id)
    except StormError, e:
        logger.exception("[ebay username: " + ebay_user_id + "] " + "Failed to fetch ebay user: " +  str(e))
    return ebay_store


if __name__ == "__main__":
    application.run(host=settings.APP_HOST, port=8091, debug=True)
