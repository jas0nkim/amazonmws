import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from storm.exceptions import StormError

from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.models import StormStore, zzAmazonItem as AmazonItem


if __name__ == "__main__":
    configure_logging(install_root_handler=False)
    set_root_graylogger()

    items = []
    try:
        items = StormStore.find(AmazonItem)
    except StormError, e:
        logger.exception('Failed to fetch amazon items')
        raise e

    if items.count() > 0:
        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_pricewatch', asins=[x.asin for x in items])
        process.start()
    else:
        logger.error('No amazon items found')

