import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

import datetime
import json

from .loggers import GrayLogger as logger

from rfi_errors.models import EbayTradingApiError, EbayNotificationError, ErrorEbayInvalidCategory


class EbayTradingApiErrorRecorder(object):

    message_id = None
    trading_api = None
    request = None
    response = None
    asin = None
    ebid = None

    def __init__(self, message_id, trading_api, request, response, **kwargs):
        self.message_id = message_id
        self.trading_api = trading_api
        self.request = request # json string
        self.response = response # json string
        self.asin = kwargs['asin'] if 'asin' in kwargs else None
        self.ebid = kwargs['ebid'] if 'ebid' in kwargs else None

    def record(self):
        kw = {
            'message_id': self.message_id,
            'trading_api': self.trading_api,
            'request': self.request,
            'response': self.response,
            'error_code': self.__retrieve_error_code(),
            'description': self.__retrieve_description(),
            'asin': self.asin,
            'ebid': self.ebid,
        }

        obj, created = EbayTradingApiError.objects.update_or_create(**kw)
        return created

    def __retrieve_error_code(self):
        response_obj = self.__load_response()
        
        if isinstance(response_obj['Errors'], list):
            # get last error code from the list
            try:
                error_code = response_obj['Errors'][len(response_obj['Errors']) - 1]['ErrorCode']
                if not isinstance(error_code, int):
                    error_code = int(error_code)
                return error_code

            except KeyError:
                logger.exception(self.response)
        else:
            try:
                error_code = response_obj['Errors']['ErrorCode']
                if not isinstance(error_code, int):
                    error_code = int(error_code)
                return error_code

            except KeyError:
                logger.exception(self.response)

        return None

    def __retrieve_description(self):
        response_obj = self.__load_response()

        if isinstance(response_obj['Errors'], list):
            # get last error code from the list
            try:
                return response_obj['Errors'][len(response_obj['Errors']) - 1]['LongMessage']
            except KeyError:
                logger.exception(self.response)
        else:
            try:
                return response_obj['Errors']['LongMessage']
            except KeyError:
                logger.exception(self.response)
                
        return None

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

        obj, created = EbayNotificationError.objects.update_or_create(**kw)
        return created

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
            'amazon_category': self.amazon_category,
            'ebay_category_id': self.ebay_category_id,
            'status': 0,
        }

        obj, created = ErrorEbayInvalidCategory.objects.update_or_create(**kw)
        return created

def record_trade_api_error(message_id, trading_api, request, response, **kwargs):
    recorder = EbayTradingApiErrorRecorder(message_id, trading_api, request, response, **kwargs)
    recorder.record()

def record_notification_error(correlation_id, event_name, recipient_user_id, response):
    recorder = EbayNotificationErrorRecorder(correlation_id, event_name, recipient_user_id, response)
    recorder.record()

def record_ebay_category_error(message_id, asin, amazon_category, ebay_category_id, request):
    recorder = ErrorEbayInvalidCategoryRecorder(message_id, asin, amazon_category, ebay_category_id, request)
    recorder.record()

class GetOutOfLoop(Exception):
    pass