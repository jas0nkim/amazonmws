import datetime
import json

from storm.exceptions import StormError

from .models import StormStore, EbayTradingApiError
from .loggers import GrayLogger as logger

class EbayTradingApiErrorRecorder(object):

    message_id = None
    trading_api = None
    request = None
    response = None
    amazon_item_id = None
    asin = None
    ebay_item_id = None
    ebid = None

    def __init__(self, message_id, trading_api, request, response, **kwargs):
        self.message_id = message_id
        self.trading_api = trading_api
        self.request = request # json string
        self.response = response # json string
        self.amazon_item_id = kwargs['amazon_item_id'] if 'amazon_item_id' in kwargs else None
        self.asin = kwargs['asin'] if 'asin' in kwargs else None
        self.ebay_item_id = kwargs['ebay_item_id'] if 'ebay_item_id' in kwargs else None
        self.ebid = kwargs['ebid'] if 'ebid' in kwargs else None

    def record(self):
        error_code = self.__retrieve_error_code()
        description = self.__retrieve_description()

        try:
            api_error = EbayTradingApiError()
            api_error.message_id = self.message_id
            api_error.trading_api = self.trading_api
            api_error.request = self.request
            api_error.response = self.response
            if self.error_code:
                api_error.error_code = self.error_code
            if self.description:
                api_error.description = self.description
            if self.amazon_item_id:
                api_error.amazon_item_id = self.amazon_item_id
            if self.asin:
                api_error.asin = self.asin
            if self.ebay_item_id:
                api_error.ebay_item_id = self.ebay_item_id
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

        try:
            return response_obj['Errors']['LongMessage']

        except KeyError:
            logger.exception(self.response)

        return None

    def __load_response(self):
        return json.loads(self.response)


def record_trade_api_error(message_id, trading_api, request, response, **kwargs):
    recorder = EbayTradingApiErrorRecorder(message_id, trading_api, request, response, **kwargs)
    recorder.record()
