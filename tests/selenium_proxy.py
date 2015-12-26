import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

if __name__ == "__main__":

    dcap = DesiredCapabilities.PHANTOMJS.copy()
    dcap["phantomjs.page.settings.userAgent"] = (
        random.choice(amazonmws_settings.USER_AGENT_LIST),
    )
    # dcap["phantomjs.page.settings.javascriptEnabled"] = ( True )
    service_args = [
        '--proxy=%s:%d' % (amazonmws_settings.APP_HOST_ORDERING, amazonmws_settings.PRIVOXY_LISTENER_PORT),
    ]

    # init tor connection
    amazonmws_utils.renew_tor_connection()

    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)

    driver.implicitly_wait(amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC) # seconds
    wait = WebDriverWait(self.driver, amazonmws_settings.APP_DEFAULT_WEBDRIVERWAIT_SEC)

    driver.get('www.itsitonline.com')
