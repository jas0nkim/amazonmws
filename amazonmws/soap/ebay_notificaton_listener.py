import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import binascii, hashlib

from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.decorator import rpc, srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable, ComplexModel, XmlAttribute, ComplexModelBase, ComplexModelMeta
from spyne.model.primitive import Unicode, Integer
from spyne.util.six import add_metaclass

from amazonmws import settings
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class RequesterCredentials(ComplexModel):
    NotificationSignature = Unicode


# class NotificationService(ServiceBase):
#     __tns__ = 'urn:ebay:apis:eBLBaseComponents'
#     __in_header__ = RequesterCredentials

#     def __getattr__(self, method_name):
#         def function(*args, **kwargs):
#             print "*"*10 + "__getattr__" + "*"*10
#             print method_name
#             print args
#             print kwargs
#             print "*"*10

#             self.__validate_signature(args[0])

#         return function

#     def __validate_signature(self, Timestamp):
#         calculated_signature = self.__calculate_signature(Timestamp)

#     def __calculate_signature(self, Timestamp):
#         hash_str = "%(timestamp)s%(devid)s%(appid)s%(certid)s" % {
#             "timestamp": Timestamp,
#             "devid": settings.EBAY_API_DEVID,
#             "appid": settings.EBAY_API_APPID,
#             "certid": settings.EBAY_API_CERTID,
#         };

#         print hash_str

#         # "base 64" of "binary hax string" of "md5" of hash string...
#         return base64.b64encode(binascii.unhexlify(hashlib.md5(hash_str).digest()))

#     @rpc(Unicode, Unicode, Integer, Integer, Unicode, Unicode, Unicode, ComplexModel, _returns=Iterable(Unicode, _body_style="bare"))
#     def GetItem(self, Timestamp, Ack, CorrelationID, Version, Build, NotificationEventName, RecipientUserID, Item):

#         # self.in_header.NotificationSignature

#         print "Timestamp: " + Timestamp
#         print "Ack: " + Ack
#         print "CorrelationID: " + CorrelationID
#         print "Version: " + Version
#         print "Build: " + Build
#         print "NotificationEventName: " + NotificationEventName
#         print "RecipientUserID: " + RecipientUserID

#         self.transport.resp_headers = {
#             "status": "200 OK",
#         }

#         return [ "Success" ]
@add_metaclass(ComplexModelMeta)
class GetItemResponse(ComplexModelBase):
    __namespace__ = 'urn:ebay:apis:eBLBaseComponents'
    Timestamp = Unicode()
    Ack = Unicode
    # CorrelationID = Integer
    # Version = Integer
    # Build = Unicode
    # NotificationEventName = Unicode
    # RecipientUserID = Unicode
    # Item = ComplexModel

class TestService(ServiceBase):
    __tns__ = 'urn:ebay:apis:eBLBaseComponents'

    @srpc(GetItemResponse, _returns=Unicode, _body_style='bare')
    def GetItem(request):
        return "Success"


application = Application([TestService],
    tns='urn:ebay:apis:eBLBaseComponents',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    wsgi_application = WsgiApplication(application)
    server = make_server('127.0.0.1', 8080, wsgi_application)
    server.serve_forever()
