import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..'))

from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

import BasePage


class ShoppingCartPage(BasePage):
    
    _url = 'https://www.amazon.com/gp/aw/c'

    _selector = {
        'items': '.sc-list-body .sc-list-item',
        'item_quantity': '.a-dropdown-prompt',
        'checkout': '#sc-mini-buy-box button'
    }

    def go_to(self):
        try:
            self._driver.get(self._url)
        except WebDriverException as e:
            self._logger.exception(e)
            raise e

    def proceed_to_checkout(self):
        try:
            checkout_button = self.get_visible_element(css_selector=self._selector['checkout'])
            if not checkout_button:
                raise ElementNotVisibleException('Proceed to checkout button found')

            checkout_button.click()

        except InvalidElementStateException as e:
            self._logger.exception(e)
            raise e

        except ElementNotVisibleException as e:
            self._logger.error(str(e))
            raise e

        except WebDriverException as e:
            self._logger.exception(e)
            raise e
