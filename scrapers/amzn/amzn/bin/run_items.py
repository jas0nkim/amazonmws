import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from storm.expr import Select
from storm.exceptions import StormError

from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.models import StormStore, zzAmazonBestsellers as AmazonBestsellers


if __name__ == "__main__":
    configure_logging(install_root_handler=False)
    set_root_graylogger()

    asins = [b.asin for b in StormStore.find(AmazonBestsellers, 
        AmazonBestsellers.asin.is_in(Select(AmazonBestsellers.asin, distinct=True)))]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins)
    process.start()

