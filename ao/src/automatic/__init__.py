import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import random
import logging
import time

from httplib import NotConnected

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name


class Automatic(object):
    
    _input_default = {}

    # TOR
    _retry_tor_connection_times = 0
    _use_tor = True

    _start_url = None

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
        service_args = [
            '--proxy=%s:%d' % (amazonmws_settings.TOR_CLIENT_IP, amazonmws_settings.TOR_CLIENT_PORT),
            '--proxy-type=%s' % amazonmws_settings.TOR_CLIENT_PORT_TYPE,
        ]

        # init tor connection
        amazonmws_utils.renew_tor_connection()

        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)

        self.driver.implicitly_wait(amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC) # seconds
        self.wait = WebDriverWait(self.driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)
        
        self.input = self._input_default.copy()
        self.input.update(inputdata)

        self.logger = logger
        # self.logger.addFilter(StaticFieldFilter(get_logger_name()))

    def _quit(self):
        if self.driver:
            self.driver.quit()

    def _renew_proxy_connection(self):
        self._renew_tor_connection()

    def _renew_tor_connection(self):
        if self._use_tor:
            if self._retry_tor_connection_times < amazonmws_settings.APP_HTTP_CONNECT_RETRY_TIMES:
                amazonmws_utils.renew_tor_connection()
                self._retry_tor_connection_times += 1
                self.logger.info('Tor connection renewed: retried {} time(s)'.format(self._retry_tor_connection_times))

                if self.driver.current_url:
                    self.driver.get(self.driver.current_url) # refresh current url

                elif self._start_url:
                    self.driver.get(self._start_url) # restart

                self._process_response()

            else:
                self.logger.warning('Tor connection trial reached to max: <{}>'.format(self._retry_tor_connection_times))
                raise NotConnected('Tor connection trial reached to max: <{}>'.format(self._retry_tor_connection_times))

    def _reset_retry_tor_connection_times(self):
        self._retry_tor_connection_times = 0

    def _log_error(self, error_type=None, error_message='Error during process'):

        filename_prefix = str(time.time())

        if error_type:
            self.error_type = error_type
        if error_message:
            self.error_message = error_message
            self.logger.error('[error] {} - (related screenshot: {}, html: {})'.format(error_message, filename_prefix + '.ao.png', filename_prefix + '.ao.html'))

        amazonmws_utils.take_screenshot(filename=filename_prefix + '.ao.png', webdriver=self.driver)
        amazonmws_utils.file_error(filename=filename_prefix + '.ao.html', content=self.driver.page_source)

    def _process_response(self):
        """check amazon ban ip address
        """
        title = self.driver.execute_script('return document.title').strip().lower()
        self.logger.info('<{}>'.format(title))

        if title == '':
            self.logger.info('connection failed <{}>'.format(self.driver.current_url))
            self._log_error(error_message='connection failed')
            raise NotConnected('Connection failed: <{}>'.format(self.driver.current_url))

        elif 'forwarding failure' in title: # 503
            self.logger.info('503 forwarding failure <{}> - renewing Tor connection'.format(self.driver.current_url))
            self._log_error(error_message='503 forwarding failure')
            self._renew_proxy_connection()

        elif 'robot check' in title: # robot check (captcha)
            self.logger.info('IP caught by amazon.com <{}> - renewing Tor connection'.format(self.driver.current_url))
            self._log_error(error_message='amazon robot check')
            self._renew_proxy_connection()

        elif 'sign in security question' in title: # security question - enter zip code
            self.logger.info('Signin security question <{}>'.format(self.driver.current_url))

            if self.is_element_visible('form#ap_dcq_form', 3):
                self.logger.info('Security question form found')
                securityquation_form = self.driver.find_element_by_css_selector('form#ap_dcq_form')
                securityquation_form.find_element_by_css_selector('input[name="dcq_question_subjective_1"]').send_keys(self.input['billing_addr_zip'])
                self.logger.info('Entered zip code')
                securityquation_form.find_element_by_css_selector('#dcq_submit').click()
                self.logger.info('Sign in using our secure server button clicked')

        elif 'your amazon.com' in title:
            self.logger.info('Incorrect screen shown <{}> - refresh screen'.format(self.driver.current_url))
            self._log_error(error_message='incorrect screen <{}>'.format(title))
            if self.driver.current_url:
                self.driver.get(self.driver.current_url) # refresh current url

        elif 'place your order' in title: # screen shown on duplication order attempted
            self.logger.info('Place your order - duplicated <{}> - refresh screen'.format(self.driver.current_url))
            if self._ignore_duplidate_order_warning:
                if self.is_element_visible('input[name=forcePlaceOrder]', 3):
                    self.driver.find_element_by_css_selector('input[name=forcePlaceOrder]').click()
                    self.logger.info('Place this duplicate order button clicked')
            else:
                raise UserWarning('Duplicated order attempted <{}>'.format(self.driver.current_url))

        elif self.is_element_visible('#auth-warning-message-box', 3): # captcha
            logging.error('IP caught by amazon.com <{}> - asking re-enter password and captcha. Renewing Tor connection'.format(self.driver.current_url))
            self._log_error(error_message='amazon auth warning')
            self._renew_proxy_connection()

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
            self.logger.exception('selector <{}> not present - {}'.format(css_selector, str(e)))
            return False

    def is_element_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._log_error(error_message=error_message)
            self.logger.exception('selector <{}> not present - {}'.format(css_selector, str(e)))
            return False

    def is_element_not_visible(self, css_selector, timeout=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC, error_message=None):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except TimeoutException as e:
            self._log_error(error_message=error_message)
            self.logger.exception('selector <{}> not present - {}'.format(css_selector, str(e)))
            return False
