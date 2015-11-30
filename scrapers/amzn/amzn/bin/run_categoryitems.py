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

            # 'http://www.amazon.com/b/?node=2975505011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975434011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=7955292011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975462011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975478011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975309011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975242011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975268011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975250011&ie=UTF8',

            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A5174%2Cn%3A%2144259011%2Cn%3A%21251269011%2Cn%3A%21468038%2Cn%3A291920%2Cp_n_format_browse-bin%3A1294043011&bbn=291920&ie=UTF8&qid=1448422583&rnid=492502011',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%212334088011%2Cn%3A%212334119011%2Cn%3A13108091011%2Cn%3A13123727011%2Cp_n_condition-type%3A1294422011&bbn=13123727011&ie=UTF8&qid=1448422785&rnid=1294421011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2625373011%2Cn%3A%212644981011%2Cn%3A%212644982011%2Cn%3A%212998369011%2Cn%3A501230%2Cp_n_format_browse-bin%3A2650305011%2Cp_n_price_fma%3A10346819011&bbn=501230&ie=UTF8&qid=1448423218&rnid=10346811011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A165793011%2Cn%3A%212334111011%2Cn%3A%212334142011%2Cn%3A9765225011%2Cp_6%3AATVPDKIKX0DER&bbn=9765225011&ie=UTF8&qid=1448423064&rnid=275224011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%212334096011%2Cn%3A%212334127011%2Cn%3A13130343011%2Cn%3A13130347011%2Cp_6%3AATVPDKIKX0DER&bbn=13130347011&ie=UTF8&qid=1448423143&rnid=698480011',

            'https://www.amazon.com/s/?url=search-alias%3Dgrocery&field-keywords=food',
            'https://www.amazon.com/Breakfast-Foods-Grocery/b/?ie=UTF8&node=16310251',
            'https://www.amazon.com/b/?ie=UTF8&node=11139497011',
            'https://www.amazon.com/International-British-Asian-Foods/b/?ie=UTF8&node=376936011',
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2151536011%2Cn%3A376936011%2Cn%3A16320321&bbn=376936011&ie=UTF8&qid=1448825253&rnid=16310211',
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2151536011%2Cn%3A376936011%2Cn%3A16310231&bbn=376936011&ie=UTF8&qid=1448825253&rnid=16310211',
            'http://www.amazon.com/b/?node=2975268011&ie=UTF8&qid=1448825345',
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975241011%2Cn%3A2975268011%2Cn%3A2975271011&bbn=2975268011&ie=UTF8&qid=1448825351&rnid=2975268011',
            'http://www.amazon.com/b/?node=2975528011&ie=UTF8',
            'http://www.amazon.com/b/?node=3048877011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975524011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975529011&ie=UTF8',
            'http://www.amazon.com/b/?node=2975539011&ie=UTF8',
        ])
    process.start()

