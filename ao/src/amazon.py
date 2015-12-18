import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import logging

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger


class AmazonAutomaticOrder(object):

    _use_tor = False

    MAX_RETRY_TOR_CONNECTION_TIMES = 10
    _retry_tor_connection_times = 0

    def __init__(self):
        # self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome()

        dcap = DesiredCapabilities.PHANTOMJS.copy()
        dcap["phantomjs.page.settings.userAgent"] = (
            random.choice(amazonmws_settings.USER_AGENT_LIST),
        )
        # dcap["phantomjs.page.settings.javascriptEnabled"] = ( True )
        service_args = [
            '--proxy=%s:%d' % (amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT),
        ]
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        
        self.driver.implicitly_wait(amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC) # seconds
        self.wait = WebDriverWait(self.driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
        
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        self.__quit()

    def __quit(self):
        # if self.driver:
        #     self.driver.quit()
        pass

    def _renew_tor_connection(self):
        if self._use_tor:
            if self._retry_tor_connection_times < self.MAX_RETRY_TOR_CONNECTION_TIMES:
                amazonmws_utils.renew_tor_connection()
                self._retry_tor_connection_times += 1
                print 'Tor connection renewed'
                if self.driver.current_url:
                    self.driver.get(self.driver.current_url) # refresh current url
            else:
                print 'Tor connection trial reached to max: <%d>. Exit process.' % self._retry_tor_connection_times
                sys.exit(0)

    def _reset_retry_tor_connection_times(self):
        self._retry_tor_connection_times = 0

    def _process_response(self):
        """check amazon ban ip address
        """
        title = self.driver.execute_script('return document.title').strip().lower()
        print "<" + title + ">"
        if title == 'robot check':
            print 'IP caught by amazon.com <%s> - renewing Tor connection' % self.driver.current_url
            self._renew_tor_connection()
        else:
            self._reset_retry_tor_connection_times()

    def is_element_present(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            print "selector <{}> not present".format(css_selector)
            return False

    def is_element_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            print "selector <{}> not visible".format(css_selector)
            return False

    def is_element_not_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            print "selector <{}> still visible".format(css_selector)
            return False

    def _run__item_screen(self):
        """screen 1: amazon item
        """
        try:
            self._renew_tor_connection()

            print '[screen] amazon item'

            print 'step 1: load item screen'
            self.driver.get(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % 'B003IG8RQW')
            
            self._process_response()

            print 'step 1.1: click \'Add to Cart\' button'
            if self.is_element_visible('#add-to-cart-button'):
                addtocart_button = self.driver.find_element_by_css_selector('#add-to-cart-button')
                addtocart_button.click()
            else:
                sys.exit(0)
        
        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__proceed_to_checkout_screen(self):
        """screen 2: proceed to checkout
        """
        try:
            self._process_response()

            print '[screen] proceed to checkout'

            # step 3: click 'Proceed to checkout' button
            # self.logger.info('step 3: click \'Proceed to checkout\' button')

            print 'step 2: click \'Cart\' button'
            if self.is_element_visible('#hlb-view-cart-announce'):
                self.driver.find_element_by_css_selector('#hlb-view-cart-announce').click()
            else:
                if self.is_element_visible('form[action="/gp/verify-action/templates/add-to-cart/ordering"]'):
                    print 'step 2-1: verify adding to cart...'
                    verify_form = self.driver.find_element_by_css_selector('form[action="/gp/verify-action/templates/add-to-cart/ordering"]')
                    verify_form.find_element_by_css_selector('input[name="submit.addToCart"]').click()
                    print 'repeating step 2...'
                    self._run__proceed_to_checkout_screen()
                else:
                    sys.exit(0)

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__shopping_cart_screen(self):
        """screen 3: shopping cart
        """
        try:
            self._process_response()

            print '[screen] shopping cart'

            print 'step 3: Shopping Cart'
            print 'step 3.1: check gift receipt option'
            if self.is_element_visible('#sc-buy-box-gift-checkbox'):
                giftreceipt_checkbox = self.driver.find_element_by_css_selector('#sc-buy-box-gift-checkbox')
                giftreceipt_checkbox.click()
            else:
                sys.exit(0)

            print 'step 3.2: click \'Proceed to checkout\' button'
            if self.is_element_visible('#sc-buy-box-ptc-button input[type=submit]'):
                ptc_button = self.driver.find_element_by_css_selector('#sc-buy-box-ptc-button input[type=submit]')
                ptc_button.click()
            else:
                sys.exit(0)

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__signin_screen(self):
        """screen 4: sign in
        """
        try:
            self._process_response()

            print '[screen] sign in'

            # step 4: fill Sign In form and submit
            # self.logger.info('step 4: fill Sign In form and submit')
            print 'step 4: fill Sign In form and submit'
            if self.is_element_visible('form[name="signIn"]'):
                signin_form = self.driver.find_element_by_css_selector('form[name="signIn"]')
                signin_form.find_element_by_css_selector('input[name="email"]').send_keys("YOUR-ID")
                signin_form.find_element_by_css_selector('input[name="password"]').send_keys("YOUR-PASS")
                signin_form.find_element_by_css_selector('#signInSubmit').click()
            else:
                sys.exit(0)

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__checkout_screen(self):
        """screen 5: checkout
        """
        try:
            self._process_response()

            print '[screen] checkout'

            # step 5: Checkout
            
            # step 5.1.1: Choose a shipping address - click to open new address popup
            # self.logger.info('step 5.1.1: Choose a shipping address - click to open new address popup')
            print 'step 5: Checkout'
            print 'step 5.1: Shipping address'
            print 'step 5.1.1: Choose a shipping address - click to open new address popup'
            if self.is_element_visible('#add-address-popover-link'):
                addaddress_link = self.driver.find_element_by_css_selector('#add-address-popover-link')
                addaddress_link.click()
            else:
                sys.exit(0)
            
            # step 5.1.2: fill and submit new address form
            # self.logger.info('step 5.1.2: fill and submit new address form')
            print 'step 5.1.2: fill and submit new address form'
            if self.is_element_visible('form#domestic-address-popover-form'):
                shippingaddress_form = self.driver.find_element_by_css_selector('form#domestic-address-popover-form')
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressFullName"]').send_keys("Floyd Braswell")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine1"]').send_keys("605 Westover Hills Blvd")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine2"]').send_keys("Apt K")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressCity"]').send_keys("Richmond")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressStateOrRegion"]').send_keys("VA")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPostalCode"]').send_keys("23225-4573")
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPhoneNumber"]').send_keys("8043973629")
                self.driver.find_element_by_css_selector('.a-popover-footer > div > span:nth-of-type(1)').click()
            else:
                sys.exit(0)

            # self.logger.info('step 5.1.3: Shipping information entered, and displayed')
            print 'step 5.1.3: Shipping information entered, and displayed'
            if not self.is_element_visible('div.displayAddressDiv'):
                sys.exit(0)

            print 'step 5.2: Choose gift options'
            if self.is_element_visible('form#giftForm'):
                gift_form = self.driver.find_element_by_css_selector('form#giftForm')
                gift_form.find_element_by_css_selector("textarea[name='message.0']").clear()
                gift_form.find_element_by_css_selector("div.save-gift-button-box > div > span:nth-of-type(1)").click()
            else:
                sys.exit(0)

            # self.logger.info('step 5.2: Choose a payment method')
            print 'step 5.3: Payment method'
            print 'step 5.3.1: Select Gift Card option'
            if self.is_element_visible('input#pm_gc_radio'):
                gc_radio = self.driver.find_element_by_css_selector('input#pm_gc_radio')
                gc_radio.click();
            else:
                sys.exit(0)

            print 'step 5.3.2: Click Use This Payment Method button'
            if self.is_element_visible('span#useThisPaymentMethodButtonId input[type=submit]'):
                usepaymentmethod_button = self.driver.find_element_by_css_selector('span#useThisPaymentMethodButtonId input[type=submit]')
                usepaymentmethod_button.click();
            else:
                sys.exit(0)

            print 'step 5.4: Items and shipping'
            print 'step 5.4.1: Choose delivery option'
            if self.is_element_visible('div#spc-orders div.shipping-speeds input[value="second"]'):
                deliveryoption_radio = self.driver.find_element_by_css_selector('div#spc-orders div.shipping-speeds input[value=second]')
                deliveryoption_radio.click();
            else:
                sys.exit(0)

            print 'step 5.5: Place order'
            if self.is_element_visible('span#submitOrderButtonId input[name="placeYourOrder1"]'):
                placeorder_button = self.driver.find_element_by_css_selector('span#submitOrderButtonId input[name="placeYourOrder1"]')
                placeorder_button.click();
            else:
                sys.exit(0)

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__order_completed_screen(self):
        """screen 6: order completed
        """
        try:
            self._process_response()

            print '[screen] order completed'

            print 'step 6: Your order has been placed'
            if self.is_element_visible('#a-page h5 > span'):
                order_number = self.driver.find_element_by_css_selector('#a-page h5 > span')
                print order_number.text.strip()
            else:
                sys.exit(0)

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except ElementNotVisibleException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def run(self):
        self._run__item_screen()
        self._run__proceed_to_checkout_screen()
        self._run__shopping_cart_screen()
        self._run__signin_screen()
        self._run__checkout_screen()
        self._run__order_completed_screen()


if __name__ == "__main__":
    monitor = AmazonAutomaticOrder()
    monitor.run()
