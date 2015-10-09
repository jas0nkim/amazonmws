import sys, os, traceback

sys.path.append('%s/../../' % os.path.dirname(__file__))

from os.path import basename
import json
import uuid
import datetime
import operator

from decimal import Decimal

from storm.exceptions import StormError
from storm.expr import Desc

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from amazonmws import utils
from amazonmws import settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, Task
from amazonmws.errors import record_trade_api_error
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class UserSetter(object):

    def __init__(self):
        pass

    def run(self):
        user_obj = settings.EBAY_USER_PREFERENCE_TEMPLATE
        user_obj['MessageID'] = uuid.uuid4()
        
        self.__set_user(user_obj)
        return True

    def __set_user(self, user_obj):
        ret = False

        try:
            api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN)
            api.execute('SetUserPreferences', user_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    
                    ret = True

                else:
                    logger.error(api.response.json())
                    record_trade_api_error(
                        user_obj['MessageID'], 
                        u'SetUserPreferences', 
                        utils.dict_to_json_string(user_obj),
                        api.response.json()
                    )

        except ConnectionError, e:
            logger.exception(e)

        return ret


if __name__ == "__main__":
    handler = UserSetter()
    handler.run()
