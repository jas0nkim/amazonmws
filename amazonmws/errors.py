import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

import datetime
import json

from django.core.exceptions import MultipleObjectsReturned

from .loggers import GrayLogger as logger

from rfi_errors.models import EbayTradingApiError, EbayNotificationError, ErrorEbayInvalidCategory


class EbayTradingApiErrorRecorder(object):

    message_id = None
    trading_api = None
    request = None
    response = None
    severity_code = None
    error_code = None
    asin = None
    ebid = None

    __exclude_error_code = [
        # 21916790, # To reduce possible issues with picture display quality, eBay recommends that pictures you upload are 1000 pixels or larger on the longest side.
        # 21917091, # The existing price and quantity values are identical to those specified in the request and, therefore, have not been modified.
        # 21917092, # The existing quantity value is identical to the quantity specified in the request and, therefore, is not modified.
    ]

    def __init__(self, message_id, trading_api, request, response, **kwargs):
        self.message_id = message_id
        self.trading_api = trading_api
        self.request = request # json string
        self.response = response # json string
        self.severity_code = self.__retrieve_severity_code()
        self.error_code = self.__retrieve_error_code()
        self.asin = kwargs['asin'] if 'asin' in kwargs else None
        self.ebid = kwargs['ebid'] if 'ebid' in kwargs else None

    def record(self):
        e = self.__record_already_exists()
        if e:
            try:
                _m_ids = json.loads(e.message_ids)
                if not _m_ids:
                    _m_ids = []
            except TypeError as e:
                _m_ids = []
            except ValueError as e:
                _m_ids = []
            _m_ids.append(str(self.message_id))

            # do update
            e.count = e.count + 1
            e.message_ids = json.dumps(_m_ids)
        else:
            # do create
            kw = {
                'trading_api': self.trading_api,
                'request': self.request,
                'response': self.response,
                'severity_code': self.severity_code,
                'error_code': self.error_code,
                'description': self.__retrieve_description(),
                'asin': self.asin,
                'ebid': self.ebid,
                'count': 1,
                'message_ids': json.dumps([ str(self.message_id), ])
            }
            e = EbayTradingApiError(**kw)
        if self.error_code not in self.__exclude_error_code:
            e.save()
        return e

    def __record_already_exists(self):
        try:
            record = EbayTradingApiError.objects.get(trading_api=self.trading_api,
                severity_code=self.severity_code,
                error_code=self.error_code,
                asin=self.asin,
                ebid=self.ebid,)
            return record
        except MultipleObjectsReturned as e:
            logger.error("[ErrorCode:{ec}|ASIN:{a}|EBID:{e}] Multiple error records exist in the system".format(ec=self.error_code, a=self.asin, e=self.ebid))
            return None
        except EbayTradingApiError.DoesNotExist as e:
            logger.warning("[ErrorCode:{ec}|ASIN:{a}|EBID:{e}] Error record not exists in the system. Create one".format(ec=self.error_code, a=self.asin, e=self.ebid))
            return None

    def __retrieve_by_key(self, key):
        response_obj = self.__load_response()
        if isinstance(response_obj['Errors'], list):
            # get last element from the list
            try:
                ret = response_obj['Errors'][len(response_obj['Errors']) - 1][key]
                return ret

            except KeyError:
                logger.exception(self.response)
        else:
            try:
                ret = response_obj['Errors'][key]
                return ret

            except KeyError:
                logger.exception(self.response)
        return None

    def __retrieve_severity_code(self):
        return self.__retrieve_by_key(key='SeverityCode')

    def __retrieve_error_code(self):
        error_code = self.__retrieve_by_key(key='ErrorCode')
        if error_code and not isinstance(error_code, int):
            error_code = int(error_code)
        return error_code

    def __retrieve_description(self):
        return self.__retrieve_by_key(key='LongMessage')

    def __load_response(self):
        return json.loads(self.response)


class EbayNotificationErrorRecorder(object):

    correlation_id = None
    event_name = None
    recipient_user_id = None
    response = None

    def __init__(self, correlation_id, event_name, recipient_user_id, response):
        self.correlation_id = correlation_id
        self.event_name = event_name
        self.recipient_user_id = recipient_user_id
        self.response = response # xml string

    def record(self):
        kw = {
            'correlation_id': self.correlation_id,
            'event_name': self.event_name,
            'recipient_user_id': self.recipient_user_id,
            'ebay_store_id': self.__retrieve_ebay_store().id if self.__retrieve_ebay_store() else None,
            'response': self.response,
            'error_code': self.__retrieve_error_code(),
            'description': self.__retrieve_description(),
        }
        e = EbayNotificationError(**kw)
        e.save()
        return e

    def __retrieve_ebay_store(self):
        ebay_store = None
        try:
            ebay_store = StormStore.find(EbayStore, EbayStore.username == self.recipient_user_id).one()
        except StormError as e:
            logger.exception("[RecipientUserId: " + self.recipient_user_id + "] " + "Failed to fetch ebay user: " +  str(e))
        return ebay_store

    def __retrieve_error_code(self):
        return None

    def __retrieve_description(self):
        return None


class ErrorEbayInvalidCategoryRecorder(object):

    message_id = None
    asin = None
    amazon_category = None
    ebay_category_id = None
    request = None

    def __init__(self, message_id, asin, amazon_category, ebay_category_id, request):
        self.message_id = message_id
        self.asin = asin
        self.amazon_category = amazon_category
        self.ebay_category_id = ebay_category_id
        self.request = request # json string

    def record(self):
        kw = {
            'message_id': self.message_id,
            'asin': self.asin,
            'amazon_category': str(self.amazon_category),
            'ebay_category_id': self.ebay_category_id,
            'status': 0,
        }
        e = ErrorEbayInvalidCategory(**kw)
        e.save()
        return e


def record_trade_api_error(message_id, trading_api, request, response, **kwargs):
    recorder = EbayTradingApiErrorRecorder(message_id, trading_api, request, response, **kwargs)
    return recorder.record()

def record_notification_error(correlation_id, event_name, recipient_user_id, response):
    recorder = EbayNotificationErrorRecorder(correlation_id, event_name, recipient_user_id, response)
    return recorder.record()

def record_ebay_category_error(message_id, asin, amazon_category, ebay_category_id, request):
    recorder = ErrorEbayInvalidCategoryRecorder(message_id, asin, amazon_category, ebay_category_id, request)
    return recorder.record()

class GetOutOfLoop(Exception):
    pass