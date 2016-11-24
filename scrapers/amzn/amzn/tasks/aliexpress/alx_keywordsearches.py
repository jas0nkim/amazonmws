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

__start_urls = [
    # Home > All Categories > Women's... > Sweaters > Pullovers > "sweater"
    'https://www.aliexpress.com/wholesale?catId=200000879&initiative_id=AS_20161124103742&SearchText=sweater',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__max_source_price = None
__min_source_price = None
__max_page = 5

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'alx_keywordsearches.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'alx_keywordsearches.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)


def run(ebay_store_id):
    task_id = uuid.uuid4()
    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True
    scrape_aliexpress(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id)

def scrape_aliexpress(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls = __start_urls
    max_source_price = __max_source_price
    min_source_price = __min_source_price
    max_page = __max_page

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('aliexpress_keyword_search',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            list_new=False,
            max_source_price=max_source_price,
            min_source_price=min_source_price,
            max_page=max_page,
            dont_list_ebay=True)
        process.start()
    else:
        logger.error('No aliexpress items found')
        return False
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
