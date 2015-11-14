import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws.loggers import set_root_graylogger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_base', 
        start_urls=['http://www.amazon.com/b?ie=UTF8&node=12896641',])
    # process.crawl('amazon_bestseller', 
    #     start_urls=['http://www.amazon.com/Best-Sellers/zgbs',])
    # process.crawl('amazon_asin', asins=['B00RWZIDQO', 
    #     'B00T4RH8E6',
    #     'B00TG8IJZ0',])
    # process.crawl('amazon_pricewatch', asins=['B00RWZIDQO', 
    #     'B00T4RH8E6',
    #     'B00TG8IJZ0',])
    process.start()