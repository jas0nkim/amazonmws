import sys, os

sys.path.append('%s/../../' % os.path.dirname(__file__))

from flask import Flask
from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


application = Flask(__name__)

@application.route(settings.APP_EBAY_NOTIFICATION_ENDPOINT_URL)
def start():
    return EbayNotificationHandler().run()


class EbayNotificationHandler(object):

    def __init__(self):
    	pass

    def run(self):
    	logger.info('flask run')
    	return "EbayNotificationHandler started"


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080, debug=True)
