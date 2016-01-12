import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import shlex, subprocess
import json

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from automatic import Automatic, AutomaticException


class AmazonOrdering(Automatic):

    _input_default = {
        'asin': None,
        'ebay_order_id': None,
        'amazon_user': None,
        'amazon_pass': None,
        'billing_addr_zip': None,
        'buyer_fullname': None,
        'buyer_shipping_address1': None,
        'buyer_shipping_address2': None,
        'buyer_shipping_city': None,
        'buyer_shipping_state': None,
        'buyer_shipping_postal': None,
        'buyer_shipping_phone': None,
    }

    # prices
    item_price = None
    shipping_and_handling = None
    tax = None
    total = None

    # order number
    order_number = None

    def __init__(self, **inputdata):
        super(AmazonOrdering, self).__init__(**inputdata)

        # set default value for buyer_shipping_address2
        self.input['buyer_shipping_address2'] = self.input['buyer_shipping_address2'] if self.input['buyer_shipping_address2'] else ' '
        
        # set default value for buyer_shipping_phone
        self.input['buyer_shipping_phone'] = self.input['buyer_shipping_phone'] if self.input['buyer_shipping_phone'] else '3454565678'
        
        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_ordering'))

    def _parse_output(self, output):
        info_str = amazonmws_utils.find_between(output, self.PREFIX_OUTPUT, self.POSTFIX_OUTPUT)

        if info_str != '':
            info = json.loads(info_str.strip())
            if 'order_summary' in info:
                if 'item_price' in info['order_summary']:
                    self.item_price = amazonmws_utils.money_to_float(info['order_summary']['item_price'])
                if 'shipping_and_handling' in info['order_summary']:
                    self.shipping_and_handling = amazonmws_utils.money_to_float(info['order_summary']['shipping_and_handling'])
                if 'tax' in info['order_summary']:
                    self.tax = amazonmws_utils.money_to_float(info['order_summary']['tax'])
                if 'total' in info['order_summary']:
                    self.total = amazonmws_utils.money_to_float(info['order_summary']['total'])

            elif 'order_number' in info:
                self.order_number = info['order_number']

    def run(self):
        try:
            command_line = "{casperjs} {script} {root_path} {proxy} {proxy_type} {user_agent} {asin} {amazon_user} {amazon_pass} {buyer_name} {buyer_addr_1} {buyer_addr_2} {buyer_city} {buyer_state} {buyer_zip} {buyer_phone}".format(
                    casperjs=os.path.join(self.CASPERJS_BIN_PATH, 'casperjs'),
                    script=os.path.join(self.JS_PATH, 'amazon_mobile.js'),
                    root_path="--root_path='{}'".format(amazonmws_settings.ROOT_PATH),
                    proxy="--proxy='{}'".format(self._proxy),
                    proxy_type="--proxy-type='{}'".format(self._proxy_type),
                    user_agent="--user_agent='{}'".format(self._user_agent),
                    asin="--asin='{}'".format(self.input['asin']),
                    amazon_user="--amazon_user='{}'".format(self.input['amazon_user']),
                    amazon_pass="--amazon_pass='{}'".format(self.input['amazon_pass']),
                    buyer_name="--buyer_name='{}'".format(self.input['buyer_fullname']),
                    buyer_addr_1="--buyer_addr_1='{}'".format(self.input['buyer_shipping_address1']),
                    buyer_addr_2="--buyer_addr_2='{}'".format(self.input['buyer_shipping_address2']),
                    buyer_city="--buyer_city='{}'".format(self.input['buyer_shipping_city']),
                    buyer_state="--buyer_state='{}'".format(self.input['buyer_shipping_state']),
                    buyer_zip="--buyer_zip='{}'".format(self.input['buyer_shipping_postal']),
                    buyer_phone="--buyer_phone='{}'".format(self.input['buyer_shipping_phone']),
                )

            args = shlex.split(command_line)

            p = subprocess.Popen(args, stderr=subprocess.PIPE)

            while True:
                out = p.stderr.read(1)
                print out
                self._parse_output(out)
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()
                    print out
                    self._parse_output(out)

        except subprocess.CalledProcessError as e:
            self._log_error(error_message='system error')
            self.logger.exception(str(e))

        finally:
            return True
