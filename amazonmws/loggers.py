import logging
import graypy

from . import settings

class StaticFieldFilter(logging.Filter):
    """
    Python logging filter that adds the given static contextual information
    in the ``fields`` dictionary to all logging records.
    """
    def __init__(self, env="production", task="general"):
        self.environment = env
        self.task = task

    def filter(self, record):
        record.environment = self.environment
        record.task = self.task
        return True


# class RequestFilter(logging.Filter):
#     """
#     Python logging filter that removes the (non-pickable) Django ``request``
#     object from the logging record.
#     """
#     def filter(self, record):
#         if hasattr(record, 'request'):
#             del record.request
#         return True


def get_logger_name():
    return 'staging' if settings.APP_ENV == 'stage' else 'production'

def get_logger_level():
    return settings.APP_LOG_LEVEL

def get_graylogger_handler():
    return graypy.GELFHandler(settings.APP_LOG_SERVER_HOST, settings.APP_LOG_SERVER_PORT)

def set_root_graylogger():
    logging.getLogger(get_logger_name())
    logging.root.setLevel(get_logger_level())
    logging.root.addHandler(get_graylogger_handler())
    # filter is not working
    # logging.root.addFilter(StaticFieldFilter(get_logger_name()))

GrayLogger = logging.getLogger(get_logger_name())
GrayLogger.setLevel(get_logger_level())
GrayLogger.addHandler(get_graylogger_handler())
GrayLogger.addFilter(StaticFieldFilter(get_logger_name()))
