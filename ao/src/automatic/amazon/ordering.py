import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import time
import shlex, subprocess

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class AmazonOrdering(object):

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

    _lynxlog_filename = None

    NEW_LINE = '\n'

    _print_1_filename = None
    _print_2_filename = None

    # error
    error_type = None
    error_message = None

    # prices
    item_price = None
    shipping_and_handling = None
    tax = None
    total = None

    # order number
    order_number = None

    def __init__(self, **inputdata):
        self.input = self._input_default.copy()
        self.input.update(inputdata)

        # set default value for buyer_shipping_address2
        self.input['buyer_shipping_address2'] = self.input['buyer_shipping_address2'] if self.input['buyer_shipping_address2'] else ''
        
        # set default value for buyer_shipping_phone
        self.input['buyer_shipping_phone'] = self.input['buyer_shipping_phone'] if self.input['buyer_shipping_phone'] else '3454565678'

        ts = str(time.time())
        
        self._lynxlog_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lynx_' + ts + '.log'))

        self._print_1_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'print_' + ts + '_1.txt'))
        self._print_2_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'print_' + ts + '_2.txt'))

        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_ordering'))

        amazonmws_utils.renew_tor_connection()

    def _remove_print_files(self):
        if os.path.isfile(self._print_1_filename):
            os.remove(self._print_1_filename)

        if os.path.isfile(self._print_2_filename):
            os.remove(self._print_2_filename)

    def _remove_lynxlog(self):
        if os.path.isfile(self._lynxlog_filename):
            os.remove(self._lynxlog_filename)

    def _lynxlog_line(self, content):
        return content + self.NEW_LINE

    def _convert_to_lynxlog_char(self, char):
        if char == ' ':
            return '<space>'
        else:
            return char


    def _build_lynxlog__item_screen(self):

        buf = ''
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 1: amazon item screen')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Add to Cart')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key A')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key C')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# click add to cart button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__shopping_cart_screenn(self):

        buf = ''
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 2: shopping cart screen')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Proceed to checkout')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key P')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key h')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key k')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key u')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# click proceed to checkout button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__signin_screen(self):

        amazon_pass_chars = list(self.input['amazon_pass'])

        buf = ''
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 3: signin screen')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Email')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key E')
        buf += self._lynxlog_line('key m')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key l')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# input amazon username')
        
        for amazon_user_char in list(self.input['amazon_user']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(amazon_user_char))
        
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('# input amazon password')

        for amazon_pass_char in list(self.input['amazon_pass']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(amazon_pass_char))

        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('# click submit')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__checkout_shipping_address_screen(self):

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 4: checkout screen')
        buf += self._lynxlog_line('##### screen 4.1: shipping address')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Add a new address')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key A')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key w')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key s')
        buf += self._lynxlog_line('key s')
        buf += self._lynxlog_line('key ^J')
        
        buf += self._lynxlog_line('# enter shipping full name')
        for buyer_fullname_char in list(self.input['buyer_fullname']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_fullname_char))

        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter shipping address 1')
        for buyer_shipping_address1_char in list(self.input['buyer_shipping_address1']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_address1_char))

        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter shipping address 2')
        for buyer_shipping_address2_char in list(self.input['buyer_shipping_address2']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_address2_char))

        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter city')
        for buyer_shipping_city_char in list(self.input['buyer_shipping_city']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_city_char))
        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter state')
        for buyer_shipping_state_char in list(self.input['buyer_shipping_state']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_state_char))
        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter zip/postal')
        for buyer_shipping_postal_char in list(self.input['buyer_shipping_postal']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_postal_char))
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# enter phone')
        for buyer_shipping_phone_char in list(self.input['buyer_shipping_phone']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(buyer_shipping_phone_char))
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')
        
        buf += self._lynxlog_line('# click use this address button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__checkout_shipping_option_screen(self):

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 4.2: select shipping option')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /FREE Two-Day Shipping')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key F')
        buf += self._lynxlog_line('key R')
        buf += self._lynxlog_line('key E')
        buf += self._lynxlog_line('key E')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key T')
        buf += self._lynxlog_line('key w')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key -')
        buf += self._lynxlog_line('key D')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key y')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key S')
        buf += self._lynxlog_line('key h')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key p')
        buf += self._lynxlog_line('key p')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key g')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# click radio button')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# search /Continue')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key C')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key u')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# click continue button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__checkout_payment_method_screen(self):

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 4.3: select payment method')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Gift card balance')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key G')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key f')
        buf += self._lynxlog_line('key t')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key b')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key l')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# move up and click checkfield')
        buf += self._lynxlog_line('key Up Arrow')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# move up and click submit')
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__print_screen(self, filename):

        buf = ''

        buf += self._lynxlog_line('################')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('# print page')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('key p')
        buf += self._lynxlog_line('key ^J')

        for i in range(200): # 200 <delete> key
            buf += self._lynxlog_line('key <delete>')

        for filename_char in list(filename):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(filename_char))

        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('#')
        buf += self._lynxlog_line('################')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)


    def _build_lynxlog__checkout_review_place_order_screen(self):

        # print this screen
        self._build_lynxlog__print_screen(self._print_1_filename)

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 4.4: review and place order')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# search /Place your order')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key P')
        buf += self._lynxlog_line('key l')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key y')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key u')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key d')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key ^J')
        buf += self._lynxlog_line('# search next')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('# click place your order button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__thank_you_screen(self):

        # print this screen
        self._build_lynxlog__print_screen(self._print_2_filename)

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 5: thank you screen')
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('# quit')
        buf += self._lynxlog_line('key q')
        buf += self._lynxlog_line('key y')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog(self):
        self._build_lynxlog__item_screen()
        self._build_lynxlog__shopping_cart_screenn()
        self._build_lynxlog__signin_screen()
        self._build_lynxlog__checkout_shipping_address_screen()
        self._build_lynxlog__checkout_shipping_option_screen()
        self._build_lynxlog__checkout_payment_method_screen()
        self._build_lynxlog__checkout_review_place_order_screen()
        self._build_lynxlog__thank_you_screen()

    def _log_error(self, error_type=None, error_message='Error during process'):
        if error_type:
            self.error_type = error_type
        if error_message:
            self.error_message = error_message
            self.logger.error('[error] {}'.format(error_message))

    def run(self):
        try:
            self._remove_print_files()

            self._build_lynxlog()

            proxy = 'http://{}:{}'.format(amazonmws_settings.APP_HOST_ORDERING, amazonmws_settings.PRIVOXY_LISTENER_PORT)
            command_line = 'export http_proxy={} && lynx -cmd_script={} -accept_all_cookies http://www.amazon.com/dp/{}'.format(proxy, self._lynxlog_filename, self.input['asin'])
            subprocess.check_call(command_line, shell=True)
            # subprocess.check_call(command_line, shell=True)
            if os.path.isfile(self._print_1_filename):
                with open(self._print_1_filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'Items:' in line and self.item_price == None:
                            print '****ITEM_PRICE**** ' + line.strip() + ' ****'
                            self.item_price = amazonmws_utils.str_to_float(line.strip())

                        elif 'Shipping & handling:' in line and self.shipping_and_handling == None:
                            print '****SHIPPING_PRICE**** ' + line.strip() + ' ****'
                            self.shipping_and_handling = amazonmws_utils.str_to_float(line.strip())

                        elif 'Estimated tax to be collected:' in line and self.tax == None:
                            print '****TAX**** ' + line.strip() + ' ****'
                            self.tax = amazonmws_utils.str_to_float(line.strip())

                        elif 'Total:' in line and self.total == None:
                            print '****TOTAL**** ' + line.strip() + ' ****'
                            self.total = amazonmws_utils.str_to_float(line.strip())

                        else:
                            continue

            if os.path.isfile(self._print_2_filename):
                with open(self._print_2_filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'Order Number:' in line and self.order_number == None:
                            print '****ORDER_NUMBER**** ' + line.strip() + ' ****'
                            self.order_number = amazonmws_utils.extract_amz_order_num(line.strip())
                            break

                        else:
                            continue

        except subprocess.CalledProcessError as e:
            self._log_error(error_message='system error')
            self.logger.exception(str(e))

        finally:
            # remove print files
            self._remove_lynxlog()
            self._remove_print_files()

            print ''
            print ''
            print '****ORDER_NUMBER**** ' + str(self.order_number) + ' ****'
            print '****ITEM_PRICE**** ' + str(self.item_price) + ' ****'
            print '****SHIPPING_PRICE**** ' + str(self.shipping_and_handling) + ' ****'
            print '****TAX**** ' + str(self.tax) + ' ****'
            print '****TOTAL**** ' + str(self.total) + ' ****'
