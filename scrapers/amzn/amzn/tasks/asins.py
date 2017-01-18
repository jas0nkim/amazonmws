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

from atoe.helpers import ListingHandler


__asins = [
    u'B007BID4T8',
]

__premium_ebay_store_ids = [1, 5, 6, 7]

def main(argv):
    ebay_store_id = 1
    force_crawl = False
    try:
        opts, args = getopt.getopt(argv, "hfe:", ["ebaystoreid=", "forcecrawl" ])
    except getopt.GetoptError:
        print 'asins.py [-f] -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'asins.py [-f] -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
        elif opt in ("-f", "--forcecrawl"):
            force_crawl = True
    run(ebay_store_id=ebay_store_id, force_crawl=force_crawl)


def run(ebay_store_id, force_crawl=False):
    task_id = uuid.uuid4()
    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True
    scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id, force_crawl=force_crawl)

def scrape_amazon(premium, task_id, ebay_store_id, force_crawl=False):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = __asins

    # scrape amazon items (variations)
    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin',
            asins=asins,
            dont_parse_variations=False,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            force_crawl=force_crawl,
            list_new=True,
            dont_list_ebay=True)
        process.start()
    else:
        logger.error('No amazon items found')
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
