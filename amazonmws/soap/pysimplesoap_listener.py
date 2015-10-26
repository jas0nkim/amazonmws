import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import logging
import io
import datetime
from decimal import Decimal

from pysimplesoap.server import SoapDispatcher, SOAPHandler, WSGISOAPHandler
from BaseHTTPServer import HTTPServer

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.soap.payloads import Item as ItemPayload

def get_item_response(Timestamp, Ack, CorrelationID, Version, Build, NotificationEventName, RecipientUserID, Item):
    print 'Ack: ' + Ack
    return Ack

def test_function(NotificationSignature):
    print 'NotificationSignature: ' + NotificationSignature
    pass

dispatcher = SoapDispatcher(
    'ebay_test_dispatcher',
    location="http://localhost:8008/wsdl/",
    action='https://developer.ebay.com/notification/', # SOAPAction
    namespace="urn:ebay:apis:eBLBaseComponents",
    prefix=False,
    soap_ns="soapenv",
    trace=True,
    debug=True,
    ns=True)

# register GetItemResponse function
dispatcher.register_function('GetItemResponse', get_item_response,
    returns={'GetItemResponse': unicode}, 
    args={
        'Timestamp': datetime.datetime,
        'Ack': unicode,
        'CorrelationID': int,
        'Version': int,
        'Build': unicode,
        'NotificationEventName': unicode,
        'RecipientUserID': unicode,
        'Item': ItemPayload
    })

# register GetItemResponse function
dispatcher.register_function('RequesterCredentials', test_function,
    returns={}, 
    args={ 'NotificationSignature': unicode })

log_capture_string = io.StringIO()
logger.addHandler(logging.StreamHandler(log_capture_string))

application = WSGISOAPHandler(dispatcher)


# if __name__=="__main__":
#     print "Starting server..."
#     from wsgiref.simple_server import make_server
#     httpd = make_server('', 8008, application)
#     httpd.serve_forever()

if __name__=="__main__":
    print "Starting server..."
    httpd = HTTPServer(("localhost", 8008), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()