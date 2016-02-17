import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

import random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

from pages.login import LoginPage as login_page


class Workflow(object):
    _webdriver = None
    _page = None

    @staticmethod
    def open_browser(phantomjs_service_args=[], 
            phantomjs_dcaps={"phantomjs.page.settings.userAgent": random.choice(amazonmws_settings.USER_AGENT_LIST)}, 
            web_driver_wait=amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC):
        """init webdriver
        """        
        dcap = DesiredCapabilities.PHANTOMJS.copy()
        dcap.update(phantomjs_dcaps)

        try:
            Workflow._webdriver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=phantomjs_service_args)
            Workflow._webdriver.set_window_size(375, 667) # iphone 6/6s screen size
            Workflow._webdriver.implicitly_wait(time_to_wait=web_driver_wait)
        
        except WebDriverException as e:
            return None

    @staticmethod
    def close_browser():
        """close webdriver
        """
        if Workflow._webdriver:
            Workflow._webdriver.quit()

    class LoginPage(object):
        @staticmethod
        def go_to():
            if not isinstance(Workflow._page, login_page):
                Workflow._page = login_page(Workflow._webdriver)
            Workflow._page.go_to()

        @staticmethod
        def login(username, password):
            if not isinstance(Workflow._page, login_page):
                Workflow._page = login_page(Workflow._webdriver)
            Workflow._page.login(username, password)

