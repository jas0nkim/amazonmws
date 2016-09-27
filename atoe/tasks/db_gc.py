import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

import getopt
import datetime

from amazonmws import django_cli
django_cli.execute()

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger
from amazonmws.model_managers import *


def __delete_legacy_data():
    # 1. delete inactive ebay items older than 90 days
    # 2. delete entries in error db tables which older than 30 days
    
    # inactive ebay items
    legacy_inactive_items = EbayItemModelManager.fetch(status=0, 
        updated_at__lt=(datetime.datetime.now() - datetime.timedelta(days=90)))

    total_item_deleted = 0
    for legacy_inactive_item in legacy_inactive_items:
        try:
            legacy_inactive_item.delete()
            total_item_deleted += 1
        except Exception as e:
            logger.exception("Failed to delete ebay item - {}".format(str(e)))
            continue
    
    # logger.info("Total ebay items deleted - {}".format(str(total_item_deleted)))

    # error db - ebay_trading_api_errors
    legacy_trading_api_errors = EbayTradingApiErrorModelManager.fetch(created_at__lt=(datetime.datetime.now() - datetime.timedelta(days=15)))

    total_trading_api_error_deleted = 0
    for legacy_trading_api_error in legacy_trading_api_errors:
        try:
            legacy_trading_api_error.delete()
            total_trading_api_error_deleted += 1
        except Exception as e:
            logger.exception("Failed to delete trading api error - {}".format(str(e)))
            continue
    
    logger.info("Total trading api errors deleted - {}".format(str(total_trading_api_error_deleted)))

    # error db - ebay_notification_errors
    legacy_notif_errors = EbayNotificationErrorModelManager.fetch(created_at__lt=(datetime.datetime.now() - datetime.timedelta(days=30)))

    total_notif_error_deleted = 0
    for legacy_notif_error in legacy_notif_errors:
        try:
            legacy_notif_error.delete()
            total_notif_error_deleted += 1
        except Exception as e:
            logger.exception("Failed to delete notification error - {}".format(str(e)))
            continue
    
    logger.info("Total notification errors deleted - {}".format(str(total_notif_error_deleted)))

    # error db - error_ebay_invalid_category - do not delete this table for now...
    # legacy_category_errors = ErrorEbayInvalidCategoryModelManager.fetch(created_at__lt=(datetime.datetime.now() - datetime.timedelta(days=30)))

    # total_category_error_deleted = 0
    # for legacy_category_error in legacy_category_errors:
    #     try:
    #         legacy_category_error.delete()
    #         total_category_error_deleted += 1
    #     except Exception as e:
    #         logger.exception("Failed to delete ebay category error - {}".format(str(e)))
    #         continue
    
    # logger.info("Total ebay category errors deleted - {}".format(str(total_category_error_deleted)))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'db_gc.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'db_gc.py'
            sys.exit()
    run()

def run():
    __delete_legacy_data()


if __name__ == "__main__":
    main(sys.argv[1:])
