import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask import request
from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


application = Flask(__name__)

@application.route(settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL, methods=['POST'])
def test_start():
    # print "here"
    # print request.form['Timestamp']
    # print 'FLASK - Timestamp: %s' % request.form['Timestamp']
    # print 'FLASK - Ack: %s' % request.form['Ack']
    # print 'FLASK - CorrelationID: %s' % request.form['CorrelationID']
    # print 'FLASK - Version: %s' % request.form['Version']
    # print 'FLASK - Build: %s' % request.form['Build']
    # print 'FLASK - NotificationEventName: %s' % request.form['NotificationEventName']
    # print 'FLASK - RecipientUserID: %s' % request.form['RecipientUserID']
    # print 'FLASK - Item: %s' % request.form['Item']

    logger.info('FLASK - Timestamp: %s' % request.form['Timestamp'])
    logger.info('FLASK - Ack: %s' % request.form['Ack'])
    logger.info('FLASK - CorrelationID: %s' % request.form['CorrelationID'])
    logger.info('FLASK - Version: %s' % request.form['Version'])
    logger.info('FLASK - Build: %s' % request.form['Build'])
    logger.info('FLASK - NotificationEventName: %s' % request.form['NotificationEventName'])
    logger.info('FLASK - RecipientUserID: %s' % request.form['RecipientUserID'])
    logger.info('FLASK - Item: %s' % utils.dict_to_unicode(request.form['Item']))
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
    application.run(host="localhost", port=8090, debug=True)
