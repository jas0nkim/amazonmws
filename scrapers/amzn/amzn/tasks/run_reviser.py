import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

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

__premium_ebay_store_ids = [1, 5, 6, 7]

__popularity_levels = {
    'popular': 1,
    'normal': 2,
    'slow': 3,
}

def main(argv):
    ebay_store_id = 1
    popularity = 2 # default 'normal'
    revise_inventory_only = False
    try:
        opts, args = getopt.getopt(argv, "hie:p:", ["ebaystoreid=", "popularity=", "inventoryonly", ])
    except getopt.GetoptError:
        print('run_reviser.py -e <1|2|3|4|...ebaystoreid> -p <popular|normal|slow>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_reviser.py -e <1|2|3|4|...ebaystoreid> -p <popular|normal|slow>')
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
        elif opt in ("-p", "--popularity") and arg in ("popular", "normal", "slow"):
            popularity = __popularity_levels[arg]
        elif opt in ("-i", "--inventoryonly"):
            revise_inventory_only = True
    run(ebay_store_id=ebay_store_id, popularity=popularity, revise_inventory_only=revise_inventory_only)


def run(ebay_store_id, popularity=2, revise_inventory_only=False):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    task_id = uuid.uuid4()

    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True

    scrapy_settings = get_project_settings()

    if premium and ebay_store_id == 1:
        if popularity == 1:
            scrapy_settings.set('CONCURRENT_REQUESTS', 40)
            scrapy_settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 40)
        else:
            scrapy_settings.set('CONCURRENT_REQUESTS', 20)
            scrapy_settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 20)
    else:
        scrapy_settings.set('CONCURRENT_REQUESTS', 2)
        scrapy_settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 2)

    # get distinct parent asins
    asins = EbayItemModelManager.fetch_distinct_parent_asins_by_popularity(
                ebay_store_id=ebay_store_id,
                popularity=popularity)

    if len(asins) > 0:
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_pricewatch',
            asins=asins,
            premium=premium,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            revise_inventory_only=revise_inventory_only,
            popularity=popularity)
        process.start()
    else:
        logger.error('No amazon items found')


if __name__ == "__main__":
    main(sys.argv[1:])
