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

    asins = EbayItemModelManager.fetch_distinct_asin()
    if len(asins) > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_pricewatch', asins=asins)
        process.start()
    else:
        logger.error('No amazon items found')
