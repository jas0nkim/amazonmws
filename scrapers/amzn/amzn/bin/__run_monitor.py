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


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'run_monitor.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'run_monitor.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)

def run(premium):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = []

    if premium:
        asins = EbayItemModelManager.fetch_distinct_asin(ebay_store_id=1)
    else:
        asins = EbayItemModelManager.fetch_distinct_asin()

    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin', asins=asins, premium=premium)
        process.start()
    else:
        logger.error('No amazon items found')


if __name__ == "__main__":
    main(sys.argv[1:])