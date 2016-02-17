import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..'))

from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

import BasePage


class ItemPage(BasePage):
    
    _url_prefix = 'https://www.amazon.com/dp/'

    _selector = {
        'add_to_cart': '#add-to-cart-button'
    }

    def go_to(self, asin):
        try:
            self._driver.get('{url_prefix}{asin}'.format(url_prefix=self._url_prefix, asin=asin))
        except WebDriverException as e:
            self._logger.exception(e)
            raise e

    def add_to_cart(self):
        self._driver.find_element_by_css_selector(css_selector=self._selector['add_to_cart']).click()
