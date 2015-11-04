import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws.loggers import set_root_graylogger


if __name__ == "__main__":
    configure_logging(install_root_handler=False)
    set_root_graylogger()

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_base', 
        start_urls=['http://www.amazon.com/b?ie=UTF8&node=12896641'])
    process.crawl('amazon_asin', asins=['B00TP0J6DI', 
        'B00VE8EG9I',
        'B00VKI4BDI',])
    process.start()