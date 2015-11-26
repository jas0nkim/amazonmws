import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from storm.exceptions import StormError

from amazonmws.loggers import set_root_graylogger, GrayLogger as logger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_base', 
        start_urls=[
            # 'http://www.amazon.com/b/?ie=UTF8&node=12896641',
            # 'http://www.amazon.com/cookware/b/?ie=UTF8&node=289814',
            'http://www.amazon.com/b/?node=2975505011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975434011&ie=UTF8',
            'http://www.amazon.com/b/?node=7955292011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975462011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975478011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975309011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975242011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975268011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975250011&ie=UTF8',
        ])
    process.start()

