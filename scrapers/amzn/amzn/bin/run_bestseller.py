import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls=[
        'http://www.amazon.com/Best-Sellers-Electronics-Household-Batteries/zgbs/electronics/15745581/',

        #'http://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/',

        # 'http://www.amazon.com/Best-Sellers-Books-Architecture/zgbs/books/',
        # 'http://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/',
        # 'http://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/',
        # 'http://www.amazon.com/Best-Sellers-Beauty-Tools-Accessories/zgbs/beauty/11062741/',
        # 'http://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Computers-Accessories/zgbs/electronics/541966/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/',
        # 'http://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/',
        # 'http://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/',
        # 'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/',
        # 'http://www.amazon.com/best-sellers-camera-photo/zgbs/photo/',
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/',
        # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care/zgbs/hpc/'
    ]

    process = CrawlerProcess(get_project_settings())
    # process.crawl('amazon_bestseller',
    #     start_urls=['http://www.amazon.com/Best-Sellers/zgbs',])
    process.crawl('amazon_bestseller', start_urls=start_urls)
    process.crawl('amazon_bestseller_sub', start_urls=start_urls)
    process.start()
