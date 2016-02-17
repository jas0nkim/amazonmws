import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class BasePage(object):

    _logger = None
    _driver = None
    _wait = None

    def __init__(self, driver, driver_wait_timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        self._logger = logger
        self._logger.addFilter(StaticFieldFilter(env=get_logger_name(), task='automate_framework_page'))
        self._driver = driver
        self._wait = WebDriverWait(driver=self._driver, timeout=driver_wait_timeout)

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

    def ss(self):
        amazonmws_utils.take_screenshot(filename=str(time.time()) + '.ao.png', webdriver=self._driver)
