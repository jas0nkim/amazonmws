import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import random
import logging
import time

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

class AutomaticException(Exception):
    pass

class Automatic(object):

    _input_default = {}

    CASPERJS_BIN_PATH = None
    JS_PATH = None

    _proxy = None
    _proxy_type = None
    _user_agent = None

    # error
    error_type = None
    error_message = None

    def __init__(self, **inputdata):

        self.input = self._input_default.copy()
        self.input.update(inputdata)

        self.logger = logger

        self.CASPERJS_BIN_PATH = os.path.join(amazonmws_settings.ROOT_PATH, 'casperjs', 'bin')
        self.JS_PATH = os.path.join(amazonmws_settings.ROOT_PATH, 'ao', 'js')
        
        self._proxy = '{}:{}'.format(amazonmws_settings.TOR_CLIENT_IP, amazonmws_settings.TOR_CLIENT_PORT)
        self._proxy_type = amazonmws_settings.TOR_CLIENT_PORT_TYPE
        self._user_agent = random.choice(amazonmws_settings.USER_AGENT_LIST_MOBILE)

        amazonmws_utils.renew_tor_connection()

    def _log_error(self, error_type=None, error_message='Error during process'):
        if error_type:
            self.error_type = error_type
        if error_message:
            self.error_message = error_message
            self.logger.error('[error] {}'.format(error_message))
