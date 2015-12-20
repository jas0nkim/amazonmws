import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from selenium.common.exceptions import WebDriverException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger

from automatic import Automatic


class AmazonOrderTracking(Automatic):

    # _input_default = {
    #     'order_id': None,
    #     'amazon_user': None,
    #     'amazon_pass': None,
    # }

    _input_default = {
        'order_id': '108-5490206-2993824',
        'amazon_user': 'redflagitems.0020@gmail.com',
        'amazon_pass': '12ReDF002AZIt!em!s',
        'billing_addr_zip': 'M5B0A5',
    }

    is_delivered = False

    carrier = None
    tracking_number = None

    def __init__(self, **inputdata):
        super(AmazonOrderTracking, self).__init__(**inputdata)

    def _run__signin_screen(self):
        """screen 0.1: signin 
        """
        try:
            title = self.driver.execute_script('return document.title').strip().lower()
            
            if 'sign in' in title:
                print '[screen] signin'

                print 'step 0.1: sign in'

                if self.is_element_visible('form#ap_signin_form'):
                    signin_form = self.driver.find_element_by_css_selector('form#ap_signin_form')
                    signin_form.find_element_by_css_selector('input[name="email"]').send_keys(self.input['amazon_user'])
                    signin_form.find_element_by_css_selector('input#ap_signin_existing_radio').click()
                    signin_form.find_element_by_css_selector('input[name="password"]').send_keys(self.input['amazon_pass'])
                    signin_form.find_element_by_css_selector('#signInSubmit-input').click()
            
            else: # title == your orders
                pass

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__signin_security_question(self):
        """screen 0.2: sign in security question (if necessary)
        """
        try:
            title = self.driver.execute_script('return document.title').strip().lower()
            
            if 'sign in security question' in title:
                print '[screen] signin security question'

                print 'step 0.2: fill in security question and submit'

                if self.is_element_visible('form#ap_dcq_form'):
                    securityquation_form = self.driver.find_element_by_css_selector('form#ap_dcq_form')
                    securityquation_form.find_element_by_css_selector('input[name="dcq_question_subjective_1"]').send_keys(self.input['billing_addr_zip'])
                    securityquation_form.find_element_by_css_selector('#dcq_question_submit').click()
            
            else: # title == your orders
                pass

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__order_screen(self):
        """screen 1: amazon order
        """
        try:
            self._renew_tor_connection()

            self.driver.get(amazonmws_settings.AMAZON_ORDER_LINK_FORMAT % self.input['order_id'])

            self._process_response()

            self._run__signin_screen()

            self._run__signin_security_question()

            print '[screen] amazon order'

            print 'step 1: load order screen'

            print 'step 1.1: click \'Track package\' button'
            if self.is_element_visible('#a-autoid-1-announce'):
                if self.is_element_visible('.shipment-is-delivered', 2):
                    self.is_delivered = True

                self.driver.find_element_by_css_selector('#a-autoid-1-announce').click()
            else:
                sys.exit(0)
        
        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__track_package_screen(self):
        """screen 2: track package
        """
        try:
            self._process_response()

            print '[screen] track package'

            print 'step 2: get tracking number if possible'
            if self.is_element_visible('#a-page > div.ship-track-page-container > div:nth-of-type(5) > div.a-span-last .ship-track-time-grid:nth-of-type(1) .ship-track-grid-subtext'):

                _tracking = self.driver.find_element_by_css_selector('#a-page > div.ship-track-page-container > div:nth-of-type(5) > div.a-span-last .ship-track-time-grid:nth-of-type(1) .ship-track-grid-subtext').text.strip()
                _tracking_info = _tracking.split(',')

                _carrier_info = _tracking_info[0].split(':')
                _tracking_number_info = _tracking_info[1].split(':')

                self.carrier = _carrier_info[1].strip()
                self.tracking_number = _tracking_number_info[1].strip()

            else:
                sys.exit(0)
        
        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def run(self):
        try:
            self._run__order_screen()
            self._run__track_package_screen()
        
        finally:
            self._quit()


if __name__ == "__main__":
    tracking = AmazonOrderTracking()
    tracking.run()

    print "is delivered? %s" % str(tracking.is_delivered)
    print "carrier: %s" % tracking.carrier
    print "tracking #: %s" % str(tracking.tracking_number)

