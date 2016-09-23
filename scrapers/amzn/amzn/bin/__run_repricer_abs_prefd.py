import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = []
    for pref in EbayStorePreferredCategoryModelManager.fetch(ebay_store_id=1, status=1):
        if pref.category_type == 'amazon_bestseller':
            asins += [ b.asin for b in AmazonBestsellerModelManager.fetch(category=pref.category_name) ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins, premium=True)
    process.start()
