import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from selenium.common.exceptions import WebDriverException, InvalidElementStateException, ElementNotVisibleException

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger

from automatic import Automatic


class AmazonOrderTracking(Automatic):

    _input_default = {
        'order_id': None,
    }

    # _input_default = {
    #     'order_id': '108-4909203-5267447',
    # }

    def __init__(self, **inputdata):
        super(AmazonOrderTracking, self).__init__(**inputdata)

    def run(self):
        try:
            # do coding here...
        
        finally:
            self._quit()



if __name__ == "__main__":
    tracking = AmazonOrderTracking()
    tracking.run()
