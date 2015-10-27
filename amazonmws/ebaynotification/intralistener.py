import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask import request
from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


application = Flask(__name__)

@application.route("%s%s" % (settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, "/GetItem"), methods=['POST'])
def test_get_item():
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'python_restful_test'))

    logger.debug('GetItem - Timestamp: %s' % request.form['Timestamp'])
    logger.debug('GetItem - Ack: %s' % request.form['Ack'])
    logger.debug('GetItem - CorrelationID: %s' % request.form['CorrelationID'])
    logger.debug('GetItem - Version: %s' % request.form['Version'])
    logger.debug('GetItem - Build: %s' % request.form['Build'])
    logger.debug('GetItem - NotificationEventName: %s' % request.form['NotificationEventName'])
    logger.debug('GetItem - RecipientUserID: %s' % request.form['RecipientUserID'])
    logger.debug('GetItem - Item: %s' % request.form['Item'])
    return "Success"

@application.route("%s%s" % (settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, "/GetItemTransactions"), methods=['POST'])
def test_get_item_transactions():
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'python_restful_test'))

    logger.debug('GetItemTransactions - Timestamp: %s' % request.form['Timestamp'])
    logger.debug('GetItemTransactions - Ack: %s' % request.form['Ack'])
    logger.debug('GetItemTransactions - CorrelationID: %s' % request.form['CorrelationID'])
    logger.debug('GetItemTransactions - Version: %s' % request.form['Version'])
    logger.debug('GetItemTransactions - Build: %s' % request.form['Build'])
    logger.debug('GetItemTransactions - NotificationEventName: %s' % request.form['NotificationEventName'])
    logger.debug('GetItemTransactions - PaginationResult: %s' % request.form['PaginationResult'])
    logger.debug('GetItemTransactions - HasMoreTransactions: %s' % request.form['HasMoreTransactions'])
    logger.debug('GetItemTransactions - TransactionsPerPage: %s' % request.form['TransactionsPerPage'])
    logger.debug('GetItemTransactions - PageNumber: %s' % request.form['PageNumber'])
    logger.debug('GetItemTransactions - ReturnedTransactionCountActual: %s' % request.form['ReturnedTransactionCountActual'])
    logger.debug('GetItemTransactions - Item: %s' % request.form['Item'])
    logger.debug('GetItemTransactions - TransactionArray: %s' % request.form['TransactionArray'])
    logger.debug('GetItemTransactions - PayPalPreferred: %s' % request.form['PayPalPreferred'])
    return "Success"

# class EbayNotificationHandler(object):

#     def __init__(self):
#         pass

#     def run(self):
#         logger.debug('FLASK - Timestamp: %s' % request.form['Timestamp'])
#         logger.debug('FLASK - Ack: %s' % request.form['Ack'])
#         logger.debug('FLASK - CorrelationID: %s' % request.form['CorrelationID'])
#         logger.debug('FLASK - Version: %s' % request.form['Version'])
#         logger.debug('FLASK - Build: %s' % request.form['Build'])
#         logger.debug('FLASK - NotificationEventName: %s' % request.form['NotificationEventName'])
#         logger.debug('FLASK - RecipientUserID: %s' % request.form['RecipientUserID'])
#         logger.debug('FLASK - Item: %s' % utils.dict_to_unicode(request.form['Item']))
#         return "EbayNotificationHandler started"


if __name__ == "__main__":
    application.run(host=settings.APP_HOST, port=8091, debug=True)
