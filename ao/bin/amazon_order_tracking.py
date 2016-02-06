import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'tasks'))

import datetime

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
from amazonmws.model_managers import *

from clry_tasks import automations


if __name__ == "__main__":
    one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)

    # this tracking starts since 2016-01-14
    service_start_date = datetime.datetime(year=2016, month=1, day=14, hour=0,minute=0,second=0,microsecond=0)
    if one_week_ago < service_start_date:
        one_week_ago = service_start_date

    transactions_to_track = TransactionModelManager.fetch_not_tracked(since=one_week_ago)

    for transaction in transactions_to_track:
        automations.order_tracking_task(transaction.id)
