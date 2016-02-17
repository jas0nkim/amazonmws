import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..'))

from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from . import BasePage


class LoginPage(BasePage):
    
    _url = 'https://www.amazon.com/gp/sign-in.html'

    _selector = {
        'signin_form': 'form[name="signIn"]',
        'email_field': 'input[name="email"]',
        'password_field': 'input[name="password"]',
        'submit': 'input[type="submit"]',
    }

    def go_to(self):
        try:
            self._driver.get(self._url)
            self.ss()
        except WebDriverException as e:
            self._logger.exception(e)
            raise e

    def login(self, username=None, password=None):
        try:
            signin_form = self.get_visible_element(css_selector=self._selector['signin_form'])
            if not signin_form:
                raise ElementNotVisibleException('Signin form not found')

            signin_form.find_element_by_css_selector(css_selector=self._selector['email_field']).send_keys(username)
            signin_form.find_element_by_css_selector(css_selector=self._selector['password_field']).send_keys(password)
            self.ss()
            signin_form.find_element_by_css_selector(css_selector=self._selector['submit']).click()

        except InvalidElementStateException as e:
            self._logger.exception(e)
            raise e

        except ElementNotVisibleException as e:
            self._logger.error(str(e))
            raise e

        except WebDriverException as e:
            self._logger.exception(e)
            raise e
