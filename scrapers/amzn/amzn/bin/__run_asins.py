import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    asins = [
        u'B0173DIFBC',
        u'B00P7QLUO2',
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_asin', asins=asins, premium=True)
    process.start()

