import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tasks'))

from storm.exceptions import StormError

from amazonmws import settings, utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from clry_tasks import automations

if __name__ == "__main__":

    automations.ordering_task.delay(3205)
