import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class AutomateFramework(object):

    _driver = None
    _wait = None
    _logger = None

    def __init__(self, phantomjs_service_args=[], phantomjs_dcaps=[], web_driver_wait=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        self._logger = logger
        self._logger.addFilter(StaticFieldFilter(env=get_logger_name(), task='automate_framework'))

        dcap = DesiredCapabilities.PHANTOMJS.copy()
        dcap.update(phantomjs_dcaps)

        try:
            self._driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=phantomjs_service_args)
            self._driver.implicitly_wait(time_to_wait=web_driver_wait)
            self._wait = WebDriverWait(driver=self._driver, timeout=web_driver_wait)
        except WebDriverException as e:
            self._logger.exceptions(e)
            raise e

    def _quit(self):
        if self._driver:
            self._driver.quit()

    def get_present_element(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except TimeoutException as e:
            self._logger.error('selector <{}> not present'.format(css_selector))
            return False

    def get_visible_element(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            return WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except TimeoutException as e:
            self._logger.error('selector <{}> not visible'.format(css_selector))
            return False

    def is_element_not_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            element = WebDriverWait(driver=self._driver, timeout=timeout).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._logger.error('selector <{}> is visible'.format(css_selector))
            return False



