import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from storm.exceptions import StormError

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *


if __name__ == "__main__":
    lock_filename = 'amazon_item_monitor.lock'
    amazonmws_utils.check_lock(lock_filename)
    
    try:
        configure_logging(install_root_handler=False)
        set_root_graylogger()

        items = EbayItemModelManager.fetch_distinct_asin()
        if items.count() > 0:
            process = CrawlerProcess(get_project_settings())
            process.crawl('amazon_pricewatch', asins=[x.asin for x in items])
            process.start()
        else:
            logger.error('No amazon items found')
    finally:
        amazonmws_utils.release_lock(lock_filename)
