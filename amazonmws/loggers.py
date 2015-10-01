import logging
import graypy

from . import settings

class StaticFieldFilter(logging.Filter):
    """
    Python logging filter that adds the given static contextual information
    in the ``fields`` dictionary to all logging records.
    """
    def __init__(self, env):
        self.environment = env

    def filter(self, record):
        record.environment = self.environment
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


__logger_name = 'staging' if settings.APP_ENV == 'stage' else 'production'
__logger_level = logging.DEBUG if settings.APP_ENV == 'stage' else logging.ERROR

__graylogger_handler = graypy.GELFHandler(settings.APP_LOG_SERVER_HOST, settings.APP_LOG_SERVER_PORT)

GrayLogger = logging.getLogger(__logger_name)
GrayLogger.setLevel(__logger_level)
GrayLogger.addHandler(__graylogger_handler)
GrayLogger.addFilter(StaticFieldFilter(__logger_name))
