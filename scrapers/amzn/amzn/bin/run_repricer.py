import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


__popularity_levels = {
    'popular': 1,
    'normal': 2,
    'slow': 3,
}

def main(argv):
    is_premium = False
    popularity = 2 # default 'normal'
    try:
        opts, args = getopt.getopt(argv, "hs:p:", ["service=", "popularity=" ])
    except getopt.GetoptError:
        print('run_repricer.py -s <basic|premium> -p <popular|normal|slow>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_repricer.py -s <basic|premium> -p <popular|normal|slow>')
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
        elif opt in ("-p", "--popularity") and arg in ("popular", "normal", "slow"):
            popularity = __popularity_levels[arg]
    run(premium=is_premium, popularity=popularity)


def run(premium, popularity=2):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    scrapy_settings = get_project_settings()
    ebay_store_ids = []

    if premium:
        scrapy_settings.set('CONCURRENT_REQUESTS', 20)
        scrapy_settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 20)
        ebay_store_ids = [1, 5, 6, 7]
    else:
        scrapy_settings.set('CONCURRENT_REQUESTS', 4)
        scrapy_settings.set('CONCURRENT_REQUESTS_PER_DOMAIN', 4)
        ebay_store_ids = [ e.id for e in EbayStoreModelManager.fetch() ]

    # get distinct parent asins
    asins = EbayItemPopularityModelManager.fetch_distinct_parent_asins(
                ebay_store_id__in=ebay_store_ids,
                popularity=popularity)

    if len(asins) > 0:
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_pricewatch',
            asins=asins,
            premium=premium,
            popularity=popularity)
        process.start()
    else:
        logger.error('No amazon items found')


if __name__ == "__main__":
    main(sys.argv[1:])
