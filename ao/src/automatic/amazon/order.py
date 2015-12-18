import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from selenium.common.exceptions import WebDriverException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger

from automatic import Automatic


class AmazonOrder(Automatic):

    _amazon_cart_url = 'https://www.amazon.com/gp/cart/view.html'
    
    # _input_default = {
    #     'asin': None,
    #     'amazon_user': None,
    #     'amazon_pass': None,
    #     'billing_addr_zip': None,
    #     'buyer_fullname': None,
    #     'buyer_shipping_address1': None,
    #     'buyer_shipping_address2': None,
    #     'buyer_shipping_city': None,
    #     'buyer_shipping_state': None,
    #     'buyer_shipping_postal': None,
    #     'buyer_shipping_phone': None,
    # }

    _input_default = {
        'asin': 'B003IG8RQW',
        'amazon_user': 'redflagitems.0020@gmail.com',
        'amazon_pass': '12ReDF002AZIt!em!s',
        'billing_addr_zip': 'M5B0A5',
        'buyer_fullname': 'Floyd Braswell',
        'buyer_shipping_address1': '605 Westover Hills Blvd',
        'buyer_shipping_address2': 'Apt K',
        'buyer_shipping_city': 'Richmond',
        'buyer_shipping_state': 'VA',
        'buyer_shipping_postal': '23225-4573',
        'buyer_shipping_phone': '8043973629',
    }

    order_number = None

    def __init__(self, **inputdata):
        super(AmazonOrder, self).__init__(**inputdata)

    def _run__item_screen(self):
        """screen 1: amazon item
        """
        try:
            self._renew_tor_connection()

            print '[screen] amazon item'

            print 'step 1: load item screen'
            self.driver.get(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % self.input['asin'])
            
            self._process_response()

            print 'step 1.1: click \'Add to Cart\' button'
            if self.is_element_visible('#add-to-cart-button'):
                addtocart_button = self.driver.find_element_by_css_selector('#add-to-cart-button')
                addtocart_button.click()
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
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
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
                if not giftreceipt_checkbox.is_selected():
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
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
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
                signin_form.find_element_by_css_selector('input[name="email"]').send_keys(self.input['amazon_user'])
                signin_form.find_element_by_css_selector('input[name="password"]').send_keys(self.input['amazon_pass'])
                signin_form.find_element_by_css_selector('#signInSubmit').click()
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

    def _run__signin_security_question(self):
        """screen 4.1: sign in security question (if necessary)
        """
        try:
            title = self.driver.execute_script('return document.title').strip().lower()
            
            if 'sign in security question' in title:
                print '[screen] signin security question'

                print 'step 4.1: fill in security question and submit'

                if self.is_element_visible('form#ap_dcq_form'):
                    securityquation_form = self.driver.find_element_by_css_selector('form#ap_dcq_form')
                    securityquation_form.find_element_by_css_selector('input[name="dcq_question_subjective_1"]').send_keys(self.input['billing_addr_zip'])
                    securityquation_form.find_element_by_css_selector('#dcq_submit').click()
            
            elif 'your amazon.com' in title:
                print '[screen] your amazon.com'

                print 'step 4.1: go back to shopping cart'

                # go back to shopping cart screen
                self.driver.get(self._amazon_cart_url)
            
            else: # title == amazon.com checkout
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

    def _run__checkout_screen(self):
        """screen 5: checkout
        """
        try:
            self._process_response()

            self._run__signin_security_question()

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
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressFullName"]').send_keys(self.input['buyer_fullname'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine1"]').send_keys(self.input['buyer_shipping_address1'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine2"]').send_keys(self.input['buyer_shipping_address2'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressCity"]').send_keys(self.input['buyer_shipping_city'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressStateOrRegion"]').send_keys(self.input['buyer_shipping_state'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPostalCode"]').send_keys(self.input['buyer_shipping_postal'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPhoneNumber"]').send_keys(self.input['buyer_shipping_phone'])
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

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error()
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__order_completed_screen(self):
        """screen 6: order completed
        """
        try:
            self._process_response()

            print '[screen] order completed'

            print 'step 6: Your order has been placed'
            if self.is_element_visible('#a-page h5 > span'):
                self.order_number = self.driver.find_element_by_css_selector('#a-page h5 > span').text.strip()
                print self.order_number
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
            self._run__item_screen()
            self._run__proceed_to_checkout_screen()
            self._run__shopping_cart_screen()
            self._run__signin_screen()
            self._run__checkout_screen()
            self._run__order_completed_screen()
        finally:
            self._quit()


if __name__ == "__main__":
    order = AmazonOrder()
    order.run()
