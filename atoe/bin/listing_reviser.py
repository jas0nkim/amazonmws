import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import datetime
from django.utils import timezone

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import EbayStoreModelManager

from atoe.helpers import ListingHandler


def run():
    __exclude_store_ids = [2, ]

    ebay_stores = EbayStoreModelManager.fetch()
    for ebay_store in ebay_stores:
        if ebay_store.id in __exclude_store_ids:
            continue        
        handler = ListingHandler(ebay_store)
        one_day_before = timezone.now() - datetime.timedelta(1) # updated within last 24 hours
        handler.run_revise(updated_since=one_day_before)


if __name__ == "__main__":
    run()
