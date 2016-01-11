import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import shlex, subprocess

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
        self.input['buyer_shipping_address2'] = self.input['buyer_shipping_address2'] if self.input['buyer_shipping_address2'] else ''
        
        # set default value for buyer_shipping_phone
        self.input['buyer_shipping_phone'] = self.input['buyer_shipping_phone'] if self.input['buyer_shipping_phone'] else '3454565678'
        
        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_ordering'))

    def run(self):
        try:
            args = [
                os.path.join(self.CASPERJS_BIN_PATH, 'casperjs'), 
                os.path.join(self.JS_PATH, 'amazon_mobile.js'),
                '--root_path', amazonmws_settings.ROOT_PATH,
                '--proxy', self._proxy, 
                '--proxy-type', self._proxy_type,
                '--user_agent', self._user_agent,
                '--asin', self.input['asin'],
                '--amazon_user', self.input['amazon_user'],
                '--amazon_pass', self.input['amazon_pass'],
                '--buyer_name', self.input['buyer_fullname'],
                '--buyer_addr_1', self.input['buyer_shipping_address1'],
                '--buyer_addr_2', self.input['buyer_shipping_address2'],
                '--buyer_city', self.input['buyer_shipping_city'],
                '--buyer_state', self.input['buyer_shipping_state'],
                '--buyer_zip', self.input['buyer_shipping_postal'],
                '--buyer_phone', self.input['buyer_shipping_phone'],
            ]
            p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            p.wait()
            
            for line in p.stdout:
                print line

        except subprocess.CalledProcessError as e:
            self._log_error(error_message='system error')
            self.logger.exception(str(e))

        finally:
            return True
