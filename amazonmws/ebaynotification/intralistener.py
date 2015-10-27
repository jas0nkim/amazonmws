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

    logger.info('GetItem - Timestamp: %s' % request.form['Timestamp'])
    logger.info('GetItem - Ack: %s' % request.form['Ack'])
    logger.info('GetItem - CorrelationID: %s' % request.form['CorrelationID'])
    logger.info('GetItem - Version: %s' % request.form['Version'])
    logger.info('GetItem - Build: %s' % request.form['Build'])
    logger.info('GetItem - NotificationEventName: %s' % request.form['NotificationEventName'])
    logger.info('GetItem - RecipientUserID: %s' % request.form['RecipientUserID'])
    logger.info('GetItem - Item: %s' % utils.dict_to_unicode(request.form['Item']))
    return "Success"

@application.route("%s%s" % (settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, "/GetItemTransactions"), methods=['POST'])
def test_get_item_transactions():
    logger.addFilter(StaticFieldFilter(get_logger_name(), 'python_restful_test'))

    logger.info('GetItemTransactions - Timestamp: %s' % request.form['Timestamp'])
    logger.info('GetItemTransactions - Ack: %s' % request.form['Ack'])
    logger.info('GetItemTransactions - CorrelationID: %s' % request.form['CorrelationID'])
    logger.info('GetItemTransactions - Version: %s' % request.form['Version'])
    logger.info('GetItemTransactions - Build: %s' % request.form['Build'])
    logger.info('GetItemTransactions - NotificationEventName: %s' % request.form['NotificationEventName'])
    logger.info('GetItemTransactions - PaginationResult: %s' % utils.dict_to_unicode(request.form['PaginationResult']))
    logger.info('GetItemTransactions - HasMoreTransactions: %s' % request.form['HasMoreTransactions'])
    logger.info('GetItemTransactions - TransactionsPerPage: %s' % request.form['TransactionsPerPage'])
    logger.info('GetItemTransactions - PageNumber: %s' % request.form['PageNumber'])
    logger.info('GetItemTransactions - ReturnedTransactionCountActual: %s' % request.form['ReturnedTransactionCountActual'])
    logger.info('GetItemTransactions - Item: %s' % utils.dict_to_unicode(request.form['Item']))
    logger.info('GetItemTransactions - TransactionArray: %s' % utils.dict_to_unicode(request.form['TransactionArray']))
    logger.info('GetItemTransactions - PayPalPreferred: %s' % request.form['PayPalPreferred'])
    return "Success"

# class EbayNotificationHandler(object):

#     def __init__(self):
#         pass

#     def run(self):
#         logger.info('FLASK - Timestamp: %s' % request.form['Timestamp'])
#         logger.info('FLASK - Ack: %s' % request.form['Ack'])
#         logger.info('FLASK - CorrelationID: %s' % request.form['CorrelationID'])
#         logger.info('FLASK - Version: %s' % request.form['Version'])
#         logger.info('FLASK - Build: %s' % request.form['Build'])
#         logger.info('FLASK - NotificationEventName: %s' % request.form['NotificationEventName'])
#         logger.info('FLASK - RecipientUserID: %s' % request.form['RecipientUserID'])
#         logger.info('FLASK - Item: %s' % utils.dict_to_unicode(request.form['Item']))
#         return "EbayNotificationHandler started"


if __name__ == "__main__":
    application.run(host=settings.APP_HOST, port=8091, debug=True)
