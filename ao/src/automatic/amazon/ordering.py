import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from selenium.common.exceptions import WebDriverException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from automatic import Automatic


class AmazonOrdering(Automatic):

    _amazon_cart_url = 'https://www.amazon.com/gp/cart/view.html'
    
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

    # _input_default = {
    #     'asin': 'B003IG8RQW',
    #     'ebay_order_id': '2134135343453-23428347238',
    #     'amazon_user': 'redflagitems.0020@gmail.com',
    #     'amazon_pass': '12ReDF002AZIt!em!s',
    #     'billing_addr_zip': 'M5B0A5',
    #     'buyer_fullname': 'Floyd Braswell',
    #     'buyer_shipping_address1': '605 Westover Hills Blvd',
    #     'buyer_shipping_address2': 'Apt K',
    #     'buyer_shipping_city': 'Richmond',
    #     'buyer_shipping_state': 'VA',
    #     'buyer_shipping_postal': '23225-4573',
    #     'buyer_shipping_phone': '8043973629',
    # }

    _gift_receipt_available = True

    order_number = None

    def __init__(self, **inputdata):
        super(AmazonOrdering, self).__init__(**inputdata)
        
        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name(), 'amazon_ordering'))

    def _run__item_screen(self):
        """screen 1: amazon item
        """
        try:
            self.logger.info('[{}] [screen] amazon item'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 1: load item screen'.format(self.input['ebay_order_id']))

            self.driver.get(amazonmws_settings.AMAZON_ITEM_LINK_FORMAT % self.input['asin'])

            self._process_response()

            self.logger.info('[{}] step 1.1: click \'Add to Cart\' button'.format(self.input['ebay_order_id']))
            if self.is_element_visible('#add-to-cart-button'):
                addtocart_button = self.driver.find_element_by_css_selector('#add-to-cart-button')
                addtocart_button.click()
            else:
                raise ElementNotVisibleException('Add to Cart not found')
        
        except InvalidElementStateException as e:
            self._log_error(error_message='Amazon item not found')
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
            raise e

        except WebDriverException as e:
            self._log_error(error_message='Amazon item not found')
            raise e

    def _run__proceed_to_checkout_screen(self):
        """screen 2: proceed to checkout
        """
        try:
            self._process_response()

            self.logger.info('[{}] [screen] proceed to checkout'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 2: click \'Cart\' button'.format(self.input['ebay_order_id']))

            if self.is_element_visible('#hlb-view-cart-announce'):
                self.driver.find_element_by_css_selector('#hlb-view-cart-announce').click()
            else:
                if self.is_element_visible('form[action="/gp/verify-action/templates/add-to-cart/ordering"]'):

                    self.logger.info('[{}] step 2-1: verify adding to cart...'.format(self.input['ebay_order_id']))

                    verify_form = self.driver.find_element_by_css_selector('form[action="/gp/verify-action/templates/add-to-cart/ordering"]')
                    verify_form.find_element_by_css_selector('input[name="submit.addToCart"]').click()

                    self.logger.info('[{}] repeating step 2...'.format(self.input['ebay_order_id']))

                    self._run__proceed_to_checkout_screen()
                else:
                    raise ElementNotVisibleException('Verify Add to Cart not found')

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__shopping_cart_screen(self):
        """screen 3: shopping cart
        """
        try:
            self._process_response()

            self.logger.info('[{}] [screen] shopping cart'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 3: Shopping Cart'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 3.1: check gift receipt option'.format(self.input['ebay_order_id']))

            if self.is_element_visible('#sc-buy-box-gift-checkbox'):
                giftreceipt_checkbox = self.driver.find_element_by_css_selector('#sc-buy-box-gift-checkbox')
                if not giftreceipt_checkbox.is_selected():
                    giftreceipt_checkbox.click()
            else:
                self._gift_receipt_available = False
                self.logger.info('[{}] No gift receipt available'.format(self.input['ebay_order_id']))

            self.logger.info('[{}] step 3.2: click \'Proceed to checkout\' button'.format(self.input['ebay_order_id']))

            if self.is_element_visible('#sc-buy-box-ptc-button input[type=submit]'):
                ptc_button = self.driver.find_element_by_css_selector('#sc-buy-box-ptc-button input[type=submit]')
                ptc_button.click()
            else:
                raise ElementNotVisibleException('Proceed to checkout not found')

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__signin_screen(self):
        """screen 4: sign in
        """
        try:
            self._process_response()

            self.logger.info('[{}] [screen] sign in'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 4: fill Sign In form and submit'.format(self.input['ebay_order_id']))

            if self.is_element_visible('form[name="signIn"]'):
                signin_form = self.driver.find_element_by_css_selector('form[name="signIn"]')
                signin_form.find_element_by_css_selector('input[name="email"]').send_keys(self.input['amazon_user'])
                signin_form.find_element_by_css_selector('input[name="password"]').send_keys(self.input['amazon_pass'])
                signin_form.find_element_by_css_selector('#signInSubmit').click()
            else:
                raise ElementNotVisibleException('Signin form not found')

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
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
                self.logger.info('[{}] [screen] signin security question'.format(self.input['ebay_order_id']))
                self.logger.info('[{}] step 4.1: fill in security question and submit'.format(self.input['ebay_order_id']))

                if self.is_element_visible('form#ap_dcq_form'):
                    securityquation_form = self.driver.find_element_by_css_selector('form#ap_dcq_form')
                    securityquation_form.find_element_by_css_selector('input[name="dcq_question_subjective_1"]').send_keys(self.input['billing_addr_zip'])
                    securityquation_form.find_element_by_css_selector('#dcq_submit').click()
            
            elif 'your amazon.com' in title:
                self.logger.info('[{}] [screen] your amazon.com'.format(self.input['ebay_order_id']))
                self.logger.info('[{}] step 4.1: go back to shopping cart'.format(self.input['ebay_order_id']))

                # go back to shopping cart screen
                self.driver.get(self._amazon_cart_url)
            
            else: # title == amazon.com checkout
                pass

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
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

            self.logger.info('[{}] [screen] checkout'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 5: Checkout'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 5.1: Shipping address'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 5.1.1: Choose a shipping address - click to open new address popup'.format(self.input['ebay_order_id']))

            if self.is_element_visible('#add-address-popover-link'):
                addaddress_link = self.driver.find_element_by_css_selector('#add-address-popover-link')
                addaddress_link.click()
            else:
                raise ElementNotVisibleException('Unable to add shipping address')
            
            self.logger.info('[{}] step 5.1.2: fill and submit new address form'.format(self.input['ebay_order_id']))

            if self.is_element_visible('form#domestic-address-popover-form'):
                shippingaddress_form = self.driver.find_element_by_css_selector('form#domestic-address-popover-form')
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressFullName"]').send_keys(self.input['buyer_fullname'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine1"]').send_keys(self.input['buyer_shipping_address1'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressAddressLine2"]').send_keys(self.input['buyer_shipping_address2'] if self.input['buyer_shipping_address2'] else '')
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressCity"]').send_keys(self.input['buyer_shipping_city'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressStateOrRegion"]').send_keys(self.input['buyer_shipping_state'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPostalCode"]').send_keys(self.input['buyer_shipping_postal'])
                shippingaddress_form.find_element_by_css_selector('input[name="enterAddressPhoneNumber"]').send_keys(self.input['buyer_shipping_phone'] if self.input['buyer_shipping_phone'] else '3454565678') # enter fake number if no number provided..
                self.driver.find_element_by_css_selector('.a-popover-footer > div > span:nth-of-type(1)').click()
            else:
                raise ElementNotVisibleException('Add shipping address form not found')

            # self.self.logger.info('step 5.1.3: Shipping information entered, and displayed')
            self.logger.info('[{}] step 5.1.3: Shipping information entered, and displayed'.format(self.input['ebay_order_id']))

            if not self.is_element_visible('div.displayAddressDiv'):
                raise ElementNotVisibleException('Shipping address not added')

            if self._gift_receipt_available:
                self.logger.info('[{}] step 5.2: Choose gift options'.format(self.input['ebay_order_id']))

                if self.is_element_visible('form#giftForm'):
                    self.logger.info('[{}] step 5.2.1: Gift option form opened'.format(self.input['ebay_order_id']))
                    gift_form = self.driver.find_element_by_css_selector('form#giftForm')
                    self.logger.info('[{}] step 5.2.2: Remove gift message'.format(self.input['ebay_order_id']))
                    gift_form.find_element_by_css_selector("textarea[name='message.0']").clear()
                    self.logger.info('[{}] step 5.2.3: Click save gift options and continue button'.format(self.input['ebay_order_id']))
                    gift_form.find_element_by_css_selector("div.save-gift-button-box > div > span:nth-of-type(1)").click()
                else:
                    raise ElementNotVisibleException('Gift receipt option not found')
            else:
                self.logger.info('[{}] step 5.2: gift option not available. skip...'.format(self.input['ebay_order_id']))

            self.logger.info('[{}] step 5.3: Payment method'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 5.3.1: Select Gift Card option'.format(self.input['ebay_order_id']))

            if self.is_element_visible('input#pm_gc_radio'):
                gc_radio = self.driver.find_element_by_css_selector('input#pm_gc_radio')
                gc_radio.click();
            else:
                raise ElementNotVisibleException('Amazon gift card payment method not found')

            self.logger.info('[{}] step 5.3.2: Click Use This Payment Method button'.format(self.input['ebay_order_id']))

            if self.is_element_visible('span#useThisPaymentMethodButtonId input[type=submit]'):
                usepaymentmethod_button = self.driver.find_element_by_css_selector('span#useThisPaymentMethodButtonId input[type=submit]')
                usepaymentmethod_button.click();
            else:
                raise ElementNotVisibleException('Unable to proceed with selected payment method')

            self.logger.info('[{}] step 5.4: Items and shipping'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 5.4.1: Choose delivery option'.format(self.input['ebay_order_id']))

            if self.is_element_visible('div#spc-orders div.shipping-speeds input[value="second"]'):
                deliveryoption_radio = self.driver.find_element_by_css_selector('div#spc-orders div.shipping-speeds input[value=second]')
                deliveryoption_radio.click();
            else:
                raise ElementNotVisibleException('Unable to proceed with selected payment method')

            self.logger.info('[{}] step 5.5: Place order'.format(self.input['ebay_order_id']))

            if self.is_element_visible('span#submitOrderButtonId input[name="placeYourOrder1"]'):
                placeorder_button = self.driver.find_element_by_css_selector('span#submitOrderButtonId input[name="placeYourOrder1"]')
                placeorder_button.click();
            else:
                raise ElementNotVisibleException('Place order not found')

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
            raise e

        except WebDriverException as e:
            self._log_error()
            raise e

    def _run__order_completed_screen(self):
        """screen 6: order completed
        """
        try:
            self._process_response()

            self.logger.info('[{}] [screen] order completed'.format(self.input['ebay_order_id']))
            self.logger.info('[{}] step 6: Your order has been placed'.format(self.input['ebay_order_id']))

            if self.is_element_visible('#a-page h5 > span'):
                self.order_number = self.driver.find_element_by_css_selector('#a-page h5 > span').text.strip()
            else:
                raise ElementNotVisibleException('Order number not found')

        except InvalidElementStateException as e:
            self._log_error()
            raise e

        except ElementNotVisibleException as e:
            self._log_error(error_message=str(e))
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

        except Exception as e:
            self._log_error(error_message='system error')
            self.logger.exception(str(e))
            return False

        finally:
            self._quit()
            return True


# if __name__ == "__main__":
#     order = AmazonOrdering()
#     order.run()

#     print "order number: %s" % order.order_number
