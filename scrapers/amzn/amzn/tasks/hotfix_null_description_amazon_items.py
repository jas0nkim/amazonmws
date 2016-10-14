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

__asins = []

__ebay_store_id = 1


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'hotfix_null_description_amazon_items.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'hotfix_null_description_amazon_items.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)


def run(premium):

    task_id = uuid.uuid4()
    ebay_store_id = __ebay_store_id
    scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id)


def __is_description_null(parent_asin):
    is_null = False
    amazon_items = AmazonItemModelManager.fetch(parent_asin=parent_asin)
    for a in amazon_items:
        if a.description is None:
            is_null = True
            break
    return is_null


def __get_asins(ebay_store_id):
    # get distinct parent asins
    asins = __asins if len(__asins) > 0 else EbayItemModelManager.fetch_distinct_parent_asins(ebay_store_id=ebay_store_id, status__in=[1, 2,])
    filtered_asins = []
    for asin in asins:
        if __is_description_null(asin):
            filtered_asins.append(asin)
    return filtered_asins

def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = __get_asins(ebay_store_id)

    # scrape amazon items (variations)
    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_asin',
            asins=asins,
            dont_parse_pictures=False,
            dont_parse_variations=False,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            force_crawl=True)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True


if __name__ == "__main__":
    main(sys.argv[1:])
