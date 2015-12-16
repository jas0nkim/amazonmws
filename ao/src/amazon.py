import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import random
import logging

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger


class AmazonAutomaticOrder(object):

    MAX_RETRY_TOR_CONNECTION_TIMES = 10
    _retry_tor_connection_times = 0

    def __init__(self):
        # self.driver = webdriver.Firefox()

        dcap = DesiredCapabilities.PHANTOMJS.copy()
        dcap["phantomjs.page.settings.userAgent"] = (
            random.choice(amazonmws_settings.USER_AGENT_LIST),
        )
        # dcap["phantomjs.page.settings.javascriptEnabled"] = ( True )
        service_args = [
            '--proxy=%s:%d' % (amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT),
        ]
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        
        self.wait = WebDriverWait(self.driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
        
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        self.__quit()

    def __quit(self):
        if self.driver:
            self.driver.quit()

    def _renew_tor_connection(self):
        if self._retry_tor_connection_times < self.MAX_RETRY_TOR_CONNECTION_TIMES:
            amazonmws_utils.renew_tor_connection()
            self._retry_tor_connection_times += 1
            print 'Tor connection renewed'
            if self.driver.current_url:
                self.driver.get(self.driver.current_url) # refresh current url
        else:
            print 'Tor connection trial reached to max: <%d>. Quit process.' % self._retry_tor_connection_times
            self.__quit()

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

    def _run__item_screen(self):
        """screen 1: amazon item
        """
        try:
            print '[screen] amazon item'

            print 'step 1: load item screen'
            self.driver.get(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % 'B003IG8RQW')
            self._process_response()

            print 'step 2: click \'Add to Cart\' button'
            addtocart_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#add-to-cart-button"))
            )
            addtocart_button.click()
        
        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__proceed_to_checkout_screen(self):
        """screen 2: proceed to checkout
        """
        try:
            print '[screen] proceed to checkout'
            self._process_response()

            # step 3: click 'Proceed to checkout' button
            # self.logger.info('step 3: click \'Proceed to checkout\' button')

            print 'step 2.1: click \'Cart\' button'
            viewcart_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#hlb-view-cart-announce"))
            )
            viewcart_button.click()

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__shopping_cart_screen(self):
        """screen 3: shopping cart
        """
        try:
            print '[screen] shopping cart'
            self._process_response()

            print 'step 3: Shopping Cart'
            print 'step 3.1: check gift receipt option'
            giftreceipt_checkbox = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#sc-buy-box-gift-checkbox"))
            )
            giftreceipt_checkbox.click()

            print 'step 3.2: click \'Proceed to checkout\' button'
            ptc_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#sc-buy-box-ptc-button input[type='submit']"))
            )
            ptc_button.click()

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__signin_screen(self):
        """screen 4: sign in
        """
        try:
            print '[screen] sign in'
            self._process_response()

            # step 4: fill Sign In form and submit
            # self.logger.info('step 4: fill Sign In form and submit')
            print 'step 4: fill Sign In form and submit'
            signin_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form[name="signIn"]'))
            )

            signin_form.find_element_by_css_selector('input[name="email"]').send_keys("YOUR-ID")
            signin_form.find_element_by_css_selector('input[name="password"]').send_keys("YOUR-PASS")
            signin_form.find_element_by_css_selector('#signInSubmit').click()

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__checkout_screen(self):
        """screen 5: checkout
        """
        try:
            print '[screen] checkout'
            self._process_response()

            # step 5: Checkout
            
            # step 5.1.1: Choose a shipping address - click to open new address popup
            # self.logger.info('step 5.1.1: Choose a shipping address - click to open new address popup')
            print 'step 5: Checkout'
            print 'step 5.1: Shipping address'
            print 'step 5.1.1: Choose a shipping address - click to open new address popup'
            addaddress_link = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#add-address-popover-link"))
            )
            addaddress_link.click()
            
            # step 5.1.2: fill and submit new address form
            # self.logger.info('step 5.1.2: fill and submit new address form')
            print 'step 5.1.2: fill and submit new address form'
            shippingaddress_form = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "form#domestic-address-popover-form"))
            )
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressFullName"]').send_keys("Floyd Braswell")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine1"]').send_keys("605 Westover Hills Blvd")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine2"]').send_keys("Apt K")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressCity"]').send_keys("Richmond")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressStateOrRegion"]').send_keys("VA")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPostalCode"]').send_keys("23225-4573")
            shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPhoneNumber"]').send_keys("8043973629")
            self.driver.find_element_by_css_selector('.a-popover-footer > div > span:nth-of-type(1)').click()
            # self.driver.find_element_by_css_selector('.a-popover-footer > div > span:nth-of-type(1) > span::nth-of-type(1)').click()

            # self.logger.info('step 5.1.2-1: submitted')
            # print 'step 5.1.2-1: submitted'

            # self.logger.info('step 5.1.3: Shipping information entered, and displayed')
            print 'step 5.1.3: Shipping information entered, and displayed'
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.displayAddressDiv"))
            )

            print 'step 5.2: Choose gift options'
            gift_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form#giftForm"))
            )

            print 'step 5.2.1: clear message'
            gift_form.find_element_by_css_selector("textarea[name='message.0']").clear()

            print 'step 5.2.2: click \'Save gift options and continue\' button'
            gift_form.find_element_by_css_selector("div.save-gift-button-box > div > span:nth-of-type(1)").click()

            # self.logger.info('step 5.2: Choose a payment method')
            print 'step 5.3: Payment method'
            print 'step 5.3.1: Select Gift Card option'
            gc_radio = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#pm_gc_radio"))
                )
            gc_radio.click();

            print 'step 5.3.2: Click Use This Payment Method button'
            usepaymentmethod_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span#useThisPaymentMethodButtonId input[type='submit']"))
            )
            usepaymentmethod_button.click();

            print 'step 5.4: Items and shipping'
            print 'step 5.4.1: Choose delivery option'
            deliveryoption_radio = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#spc-orders div.shipping-speeds input[value='second']"))
            )
            deliveryoption_radio.click();

            print 'step 5.5: Place order'
            placeorder_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span#submitOrderButtonId input[name='placeYourOrder1']"))
            )
            placeorder_button.click();

        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except WebDriverException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

    def _run__order_completed_screen(self):
        """screen 6: order completed
        """
        try:
            print '[screen] order completed'
            self._process_response()

            print 'step 6: Your order has been placed'
            order_number = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#a-page h5 > span"))
            )
            print order_number.text.strip()
        
        except TimeoutException as e:
            amazonmws_utils.take_screenshot(self.driver)
            raise e

        except InvalidElementStateException as e:
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
