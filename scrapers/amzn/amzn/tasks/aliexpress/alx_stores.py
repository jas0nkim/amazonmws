import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

import getopt
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

# from atoe.helpers import ListingHandler

__alx_store_ids = [
    '1775014', # XianRan Clothes--Slow Life
    '1094341', # JAZZEVAR Official Store
    '1897083', # AILORIA
    '1662053', # GerrySnowy Store (Top-rated Seller)
]

__premium_ebay_store_ids = [1, 5, 6, 7]

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print 'alx_stores.py'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'alx_stores.py'
            sys.exit()
    run()


def run():
    task_id = uuid.uuid4()
    premium = True
    scrape_aliexpress_stores(premium=premium, task_id=task_id)

def scrape_aliexpress_stores(premium, task_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    alx_store_ids = __alx_store_ids

    # scrape aliexpress stores
    if len(alx_store_ids) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('aliexpress_store',
            alx_store_ids=alx_store_ids,
            premium=premium)
        process.start()
    else:
        logger.error('No aliexpress stores found')
        return False
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
