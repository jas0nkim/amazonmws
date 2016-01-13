import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import shlex, subprocess
import json

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from automatic import Automatic, AutomaticException


class AmazonOrderTracking(Automatic):

    _input_default = {
        'order_id': None,
        'amazon_user': None,
        'amazon_pass': None,
    }

    # _input_default = {
    #     'order_id': '108-5490206-2993824',
    #     'amazon_user': 'redflagitems.0020@gmail.com',
    #     'amazon_pass': '12ReDF002AZIt!em!s',
    #     'billing_addr_zip': 'M5B0A5',
    # }

    is_delivered = False

    carrier = None
    tracking_number = None

    def __init__(self, **inputdata):
        super(AmazonOrdering, self).__init__(**inputdata)
        
        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_order_tracking'))

    def _parse_output(self, output):
        info_str = amazonmws_utils.find_between(output, self.PREFIX_OUTPUT, self.POSTFIX_OUTPUT)

        if info_str != '':
            info = json.loads(info_str.strip())
            if 'tracking_info' in info:
                if 'carrier' in info['tracking_info']:
                    self.carrier = amazonmws_utils.str_to_unicode(info['tracking_info']['carrier'])
                if 'tracking_number' in info['tracking_info']:
                    self.tracking_number = amazonmws_utils.str_to_unicode(info['tracking_info']['tracking_number'])

    def run(self):
        try:
            command_line = "{casperjs} {script} {root_path} {proxy} {proxy_type} {user_agent} {order_id} {amazon_user} {amazon_pass}".format(
                    casperjs=os.path.join(self.CASPERJS_BIN_PATH, 'casperjs'),
                    script=os.path.join(self.JS_PATH, 'amazon_mobile.js'),
                    root_path="--root_path='{}'".format(amazonmws_settings.ROOT_PATH),
                    proxy="--proxy='{}'".format(self._proxy),
                    proxy_type="--proxy-type='{}'".format(self._proxy_type),
                    user_agent="--user_agent='{}'".format(self._user_agent),
                    order_id="--order_id='{}'".format(self.input['order_id']),
                    amazon_user="--amazon_user='{}'".format(self.input['amazon_user']),
                    amazon_pass="--amazon_pass='{}'".format(self.input['amazon_pass']),
                )

            args = shlex.split(command_line)

            p = subprocess.Popen(args, stdout=subprocess.PIPE)

            while True:
                out = p.stdout.readline()
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    # print out
                    self._parse_output(out)

        except subprocess.CalledProcessError as e:
            self._log_error(error_message='system error')
            self.logger.exception(str(e))

        finally:
            return True
