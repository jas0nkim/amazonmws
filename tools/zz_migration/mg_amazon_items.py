import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scrapers', 'amzn'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from storm.expr import Select
from storm.exceptions import StormError

from amazonmws import settings as amazon_settings, utils as amazon_utils
from amazonmws.loggers import set_root_graylogger
from amazonmws.models import StormStore, AmazonItem


if __name__ == "__main__":
    configure_logging(install_root_handler=False)
    set_root_graylogger()

    asins = [b.asin for b in StormStore.find(AmazonItem, 
        AmazonItem.asin.is_in(Select(AmazonItem.asin, distinct=True)))]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins)
    process.start()
