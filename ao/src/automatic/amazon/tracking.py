import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import shlex, subprocess

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from automatic import Automatic, AutomaticException


class AmazonOrderTracking(Automatic):

    _input_default = {
        'order_id': None,
        'amazon_user': None,
        'amazon_pass': None,
        'billing_addr_zip': None,
    }

    carrier = None
    tracking_number = None

    def __init__(self, **inputdata):
        super(AmazonOrderTracking, self).__init__(**inputdata)

        self._lynxlog_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lynx_tracking_' + self._ts + '.log'))

        self._print_filenames.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'print_tracking_' + self._ts + '.txt')))

        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_order_tracking'))

    def _build_lynxlog__signin_screen(self):
        
        buf = ''
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 1: sign in screen')
        buf += self._lynxlog_line('#####')
        
        buf += self._lynxlog_line('# search /E-mail or mobile number:')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key E')
        buf += self._lynxlog_line('key -')
        buf += self._lynxlog_line('key m')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key l')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key m')
        buf += self._lynxlog_line('key o')
        buf += self._lynxlog_line('key b')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key l')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key u')
        buf += self._lynxlog_line('key m')
        buf += self._lynxlog_line('key b')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key :')
        buf += self._lynxlog_line('key ^J')
        
        buf += self._lynxlog_line('# input amazon username')
        for amazon_user_char in list(self.input['amazon_user']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(amazon_user_char))

        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')
        buf += self._lynxlog_line('key Down Arrow')

        buf += self._lynxlog_line('# input amazon password')

        for amazon_pass_char in list(self.input['amazon_pass']):
            buf += self._lynxlog_line('key ' + self._convert_to_lynxlog_char(amazon_pass_char))

        buf += self._lynxlog_line('key Down Arrow')
        
        buf += self._lynxlog_line('# search /Sign In')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key S')
        buf += self._lynxlog_line('key i')
        buf += self._lynxlog_line('key g')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key I')
        buf += self._lynxlog_line('key n')
        buf += self._lynxlog_line('key ^J')
        
        buf += self._lynxlog_line('# click sign in button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__order_info_screen(self):
        
        buf = ''
        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 2: order info screen')
        buf += self._lynxlog_line('#####')
        
        buf += self._lynxlog_line('# search /Track package')
        buf += self._lynxlog_line('key /')
        buf += self._lynxlog_line('key T')
        buf += self._lynxlog_line('key r')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key k')
        buf += self._lynxlog_line('key <space>')
        buf += self._lynxlog_line('key p')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key c')
        buf += self._lynxlog_line('key k')
        buf += self._lynxlog_line('key a')
        buf += self._lynxlog_line('key g')
        buf += self._lynxlog_line('key e')
        buf += self._lynxlog_line('key ^J')
        
        buf += self._lynxlog_line('# click track package button')
        buf += self._lynxlog_line('key ^J')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog__tracking_info_screen(self):

        # print this screen
        self._build_lynxlog__print_screen(self._print_filenames[0])

        buf = ''

        buf += self._lynxlog_line('#####')
        buf += self._lynxlog_line('##### screen 3: tracking info screen')
        buf += self._lynxlog_line('#####')

        buf += self._lynxlog_line('# quit')
        buf += self._lynxlog_line('key q')
        buf += self._lynxlog_line('key y')

        with open(self._lynxlog_filename, "a+") as f:
            f.write(buf)

    def _build_lynxlog(self):
        self._build_lynxlog__signin_screen()
        self._build_lynxlog__order_info_screen()
        self._build_lynxlog__tracking_info_screen()

    def run(self):
        try:
            self._remove_print_files()

            self._build_lynxlog()

            # command_line = 'export http_proxy={} && lynx -useragent="{}" -cmd_script={} -accept_all_cookies https://www.amazon.com/gp/your-account/order-history/?search={}'.format(self._proxy, self._user_agent, self._lynxlog_filename, self.input['asin'])
            command_line = 'export http_proxy={} && lynx -useragent="{}" -cmd_script={} -accept_all_cookies https://www.amazon.com/gp/your-account/order-history/?search={} > /dev/null'.format(self._proxy, self._user_agent, self._lynxlog_filename, self.input['order_number'])

            subprocess.check_call(command_line, shell=True)

            if os.path.isfile(self._print_filenames[0]):
                with open(self._print_filenames[0], 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'Tracking #:' in line and self.carrier == None and self.tracking_number == None:
                            # print '****CARRIER/TRACKING_NUMBER**** ' + line.strip() + ' ****'
                            (_carrier_partial, _tracking_number_partial) = line.split(',')

                            self.carrier = amazonmws_utils.str_to_unicode(amazonmws_utils.extract_amz_carrier(_carrier_partial))
                            self.tracking_number = amazonmws_utils.str_to_unicode(amazonmws_utils.extract_amz_tracking_num(_tracking_number_partial))
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

            # print ''
            # print ''
            # print '****CARRIER**** ' + str(self.carrier) + ' ****'
            # print '****TRACKING_NUMBER**** ' + str(self.tracking_number) + ' ****'
