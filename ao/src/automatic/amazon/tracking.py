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
        pass

    def _build_lynxlog__order_info_screen(self):
        pass

    def _build_lynxlog__tracking_info_screen(self):
        pass

    def _build_lynxlog(self):
        self._build_lynxlog__signin_screen()
        self._build_lynxlog__order_info_screen()
        self._build_lynxlog__tracking_info_screen()

    def run(self):
        try:
            self._remove_print_files()

            self._build_lynxlog()

            #command_line = 'export http_proxy={} && lynx -useragent="{}" -cmd_script={} -accept_all_cookies https://www.amazon.com/gp/your-account/order-history/?search={}'.format(self._proxy, self._user_agent, self._lynxlog_filename, self.input['asin'])
            command_line = 'export http_proxy={} && lynx -useragent="{}" -cmd_script={} -accept_all_cookies https://www.amazon.com/gp/your-account/order-history/?search={} > /dev/null'.format(self._proxy, self._user_agent, self._lynxlog_filename, self.input['order_number'])

            subprocess.check_call(command_line, shell=True)

            if os.path.isfile(self._print_filenames[0]):
                with open(self._print_filenames[0], 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'Tracking #:' in line and self.carrier == None and self.tracking_number == None:
                            # print '****CARRIER/TRACKING_NUMBER**** ' + line.strip() + ' ****'
                            self.carrier = amazonmws_utils.str_to_unicode(amazonmws_utils.extract_amz_order_num(line.strip()))
                            self.tracking_number = amazonmws_utils.str_to_unicode(amazonmws_utils.extract_amz_order_num(line.strip()))
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
