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
    # process.crawl('amazon_bestseller', 
    #     start_urls=['http://www.amazon.com/Best-Sellers/zgbs',])
    process.crawl('amazon_bestseller', 
        start_urls=['http://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products',
        	'http://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive',
        	'http://www.amazon.com/Best-Sellers-Beauty-Tools-Accessories/zgbs/beauty/11062741',
        	'http://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts',
        	'http://www.amazon.com/Best-Sellers-Electronics-Computers-Accessories/zgbs/electronics/541966',
        	'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games',
        	'http://www.amazon.com/Best-Sellers-Kitchen-Dining-Utensils-Gadgets/zgbs/kitchen/289754',])
    process.start()