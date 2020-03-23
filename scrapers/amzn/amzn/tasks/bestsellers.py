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

__start_urls = [

    # Women's Casual Shorts
    'https://www.amazon.com/Best-Sellers-Womens-Casual-Shorts/zgbs/fashion/2348585011/ref=zg_bs_nav_4_1048186',

    # Women's Denim Shorts
    'https://www.amazon.com/Best-Sellers-Womens-Denim-Shorts/zgbs/fashion/2348586011/ref=zg_bs_nav_5_2348585011',

    # Women's Leggings
    'https://www.amazon.com/Best-Sellers-Womens-Leggings/zgbs/fashion/1258967011/ref=zg_bs_nav_3_1040660',

    # Women's Night Out Pants & Capris
    # 'https://www.amazon.com/Best-Sellers-Womens-Night-Out-Pants-Capris/zgbs/fashion/2528697011/ref=zg_bs_nav_5_2528696011',

]

__premium_ebay_store_ids = [1, 8]
__min_amazon_rating = 3.0

def main(argv):
    ebay_store_id = 1
    force_crawl = False
    try:
        opts, args = getopt.getopt(argv, "hfe:", ["ebaystoreid=", "forcecrawl" ])
    except getopt.GetoptError:
        print 'bestsellers.py [-f] -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'bestsellers.py [-f] -e <1|2|3|4|...ebaystoreid>'
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

    start_urls = __start_urls
    min_amazon_rating = __min_amazon_rating

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_bestseller',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            list_new=True,
            min_amazon_rating=min_amazon_rating,
            force_crawl=force_crawl,
            dont_list_ebay=True)
        process.start()
    else:
        logger.error('No amazon items found')
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
