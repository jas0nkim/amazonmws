import datetime
import json

from storm.exceptions import StormError

from .models import StormStore, EbayStore, EbayTradingApiError, EbayNotificationError, ErrorEbayInvalidCategory
from .loggers import GrayLogger as logger

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
        error_code = self.__retrieve_error_code()
        description = self.__retrieve_description()

        try:
            api_error = EbayTradingApiError()
            api_error.message_id = self.message_id if isinstance(self.message_id, str) else str(self.message_id)
            api_error.trading_api = self.trading_api
            api_error.request = self.request if isinstance(self.request, unicode) else unicode(self.request)
            api_error.response = self.response if isinstance(self.response, unicode) else unicode(self.response)
            if error_code:
                api_error.error_code = error_code
            if description:
                api_error.description = description
            if self.asin:
                api_error.asin = self.asin
            if self.ebid:
                api_error.ebid = self.ebid
            api_error.created_at = datetime.datetime.now()
            api_error.updated_at = datetime.datetime.now()

            StormStore.add(api_error)
            StormStore.commit()

        except StormError:
            logger.exception('EbayTradingApiError db insertion error')
            StormStore.rollback()

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
        ebay_store = self.__retrieve_ebay_store()        
        error_code = self.__retrieve_error_code()
        description = self.__retrieve_description()

        try:
            notif_error = EbayNotificationError()
            notif_error.correlation_id = self.correlation_id if isinstance(self.correlation_id, str) else str(self.correlation_id)
            notif_error.event_name = self.event_name
            notif_error.recipient_user_id = self.recipient_user_id
            notif_error.ebay_store_id = ebay_store.id
            notif_error.response = self.response if isinstance(self.response, unicode) else unicode(self.response)
            if error_code:
                notif_error.error_code = error_code
            if description:
                notif_error.description = description
            notif_error.created_at = datetime.datetime.now()
            notif_error.updated_at = datetime.datetime.now()

            StormStore.add(notif_error)
            StormStore.commit()

        except StormError:
            logger.exception('EbayNotificationError db insertion error')
            StormStore.rollback()

    def __retrieve_ebay_store(self):
        ebay_store = None
        try:
            ebay_store = StormStore.find(EbayStore, EbayStore.username == self.recipient_user_id).one()
        except StormError, e:
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
        try:
            category_error = ErrorEbayInvalidCategory()
            category_error.message_id = self.message_id if isinstance(self.message_id, str) else str(self.message_id)
            category_error.asin = self.asin
            category_error.amazon_category = self.amazon_category if isinstance(self.amazon_category, unicode) else unicode(self.amazon_category)
            category_error.ebay_category_id = self.ebay_category_id if isinstance(self.ebay_category_id, unicode) else unicode(self.ebay_category_id)
            category_error.request = self.request if isinstance(self.request, unicode) else unicode(self.request)
            category_error.status = 0
            category_error.created_at = datetime.datetime.now()
            category_error.updated_at = datetime.datetime.now()
            StormStore.add(category_error)
            StormStore.commit()

        except StormError:
            logger.exception('ErrorEbayInvalidCategory db insertion error')
            StormStore.rollback()


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