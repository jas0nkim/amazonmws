import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from amazonmws import settings as amazonmws_settings
from settings import *

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': amazonmws_settings.APP_MYSQL_HOST,
        'PORT': amazonmws_settings.APP_MYSQL_PORT,
        'NAME': amazonmws_settings.APP_MYSQL_DATABASE,
        'USER': amazonmws_settings.APP_MYSQL_USERNAME,
        'PASSWORD': amazonmws_settings.APP_MYSQL_PASSWORD,
        'CONN_MAX_AGE': None,
    }
}
