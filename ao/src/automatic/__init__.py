import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import random
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger


class Automatic(object):
    
    _input_default = {}

    # TOR
    MAX_RETRY_TOR_CONNECTION_TIMES = 10
    _retry_tor_connection_times = 0
    _use_tor = True

    # error
    error_type = None
    error_message = None

    def __init__(self, **inputdata):
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
        
        self.input = self._input_default.copy()
        self.input.update(inputdata)

        self.logger = logger
        self.logger.addFilter(StaticFieldFilter(get_logger_name()))

    def _quit(self):
        if self.driver:
            self.driver.quit()
        # pass

    def _renew_tor_connection(self):
        if self._use_tor:
            if self._retry_tor_connection_times < self.MAX_RETRY_TOR_CONNECTION_TIMES:
                amazonmws_utils.renew_tor_connection()
                self._retry_tor_connection_times += 1

                self.logger('Tor connection renewed')

                if self.driver.current_url:
                    self.driver.get(self.driver.current_url) # refresh current url
            else:
                self.logger('Tor connection trial reached to max: <{}>. Exit process.'.format(self._retry_tor_connection_times))
                
                sys.exit(0)

    def _reset_retry_tor_connection_times(self):
        self._retry_tor_connection_times = 0

    def _log_error(self, error_type=None, error_message=None):
        if error_type:
            self.error_type = error_type
        if error_message:
            self.error_message = error_message
            self.logger.error('[error] {}'.format(error_message))

        amazonmws_utils.take_screenshot(self.driver)
        amazonmws_utils.file_error(str(time.time()) + '.ao.html', self.driver.page_source)

    def _process_response(self):
        """check amazon ban ip address
        """
        title = self.driver.execute_script('return document.title').strip().lower()

        self.logger('<{}>'.format(title))

        if 'robot check' in title:

            self.logger('IP caught by amazon.com <{}> - renewing Tor connection'.format(self.driver.current_url))

            self._renew_tor_connection()
        else:
            self._reset_retry_tor_connection_times()

    def is_element_present(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._log_error(error_message=error_message)

            self.logger('selector <{}> not present'.format(css_selector))

            return False

    def is_element_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._log_error(error_message=error_message)
            self.logger('selector <{}> not present'.format(css_selector))
            return False

    def is_element_not_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._log_error(error_message=error_message)
            self.logger('selector <{}> not present'.format(css_selector))
            return False
