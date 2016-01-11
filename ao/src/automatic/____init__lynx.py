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

    _lynxlog_filename = None

    _print_filenames = []

    _proxy = None
    _user_agent = None

    NEW_LINE = '\n'

    # error
    error_type = None
    error_message = None

    def __init__(self, **inputdata):
        self._ts = str(time.time())
        
        self.input = self._input_default.copy()
        self.input.update(inputdata)

        self.logger = logger

        amazonmws_utils.renew_tor_connection()
        self._proxy = 'http://{}:{}'.format(amazonmws_settings.APP_HOST_ORDERING, amazonmws_settings.PRIVOXY_LISTENER_PORT)

        self._user_agent = random.choice(amazonmws_settings.USER_AGENT_LIST)

    def _remove_lynxlog(self):
        if self._lynxlog_filename and os.path.isfile(self._lynxlog_filename):
            os.remove(self._lynxlog_filename)

    def _remove_print_files(self):
        if len(self._print_filenames) > 0:
            for fn in self._print_filenames:
                if os.path.isfile(fn):
                    os.remove(fn)

    def _lynxlog_line(self, content):
        return content + self.NEW_LINE

    def _convert_to_lynxlog_char(self, char):
        if char == ' ':
            return '<space>'
        else:
            return char

    def _build_lynxlog(self):
    	pass

    def _build_lynxlog__print_screen(self, filename):

        buf = ''

        buf += self._lynxlog_line('################')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('# print page')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('key p')
        buf += self._lynxlog_line('key ^J')

        for i in range(300): # 300 <delete> key
            buf += self._lynxlog_line('key <delete>')

        for filename_char in list(filename):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(filename_char))

        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('################')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _log_error(self, error_type=None, error_message='Error during process'):
        if error_type:
            self.error_type = error_type
        if error_message:
            self.error_message = error_message
            self.logger.error('[error] {}'.format(error_message))
