import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

import getopt
import uuid

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import django_cli
django_cli.execute()

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger, GrayLogger as logger
from amazonmws.model_managers import *

from atoe.helpers import ListingHandler

__start_urls = [

    # Best Sellers in Toys & Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0',

    # Best Sellers in Baby Health & Care Products
    # 'https://www.amazon.com/Best-Sellers-Baby-Health-Care-Products/zgbs/baby-products/166856011/ref=zg_bs_nav_ba_1_ba',

    # Best Sellers in Nursery Decor
    # 'https://www.amazon.com/Best-Sellers-Baby-Nursery-Decor/zgbs/baby-products/166875011/ref=zg_bs_nav_ba_1_ba',

    # Best Sellers in Pregnancy & Maternity Products
    # 'https://www.amazon.com/Best-Sellers-Baby-Pregnancy-Maternity-Products/zgbs/baby-products/166804011/ref=zg_bs_nav_ba_1_ba',

    # Best Sellers in Action & Toy Figures
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Action-Toy-Figures/zgbs/toys-and-games/2514571011/ref=zg_bs_nav_t_2_165993011',

    # Best Sellers in Action Figure Vehicles & Playsets
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Action-Figure-Vehicles-Playsets/zgbs/toys-and-games/7620514011/ref=zg_bs_nav_t_3_2514571011',

    # Best Sellers in Kids' Costumes
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Costumes/zgbs/toys-and-games/14702634011/ref=zg_bs_nav_t_2_166316011',

    # Best Sellers in Pretend Play
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Pretend-Play/zgbs/toys-and-games/166309011/ref=zg_bs_nav_t_3_14702634011',

    # Best Sellers in Toy Kitchen Products
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Toy-Kitchen-Products/zgbs/toys-and-games/166343011/ref=zg_bs_nav_t_3_166309011',

    # Best Sellers in Toy Construction Tools
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Toy-Construction-Tools/zgbs/toys-and-games/166342011/ref=zg_bs_nav_t_3_166309011',

    # Best Sellers in Kids' Fashion & Beauty Dress-Up Toys
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Fashion-Beauty-Dress-Up/zgbs/toys-and-games/166310011/ref=zg_bs_nav_t_3_14702635011',

    # Best Sellers in Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/166220011/ref=zg_bs_nav_t_1_t',

    # Best Sellers in Battling Top Toys
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Battling-Top/zgbs/toys-and-games/166224011/ref=zg_bs_nav_t_2_166220011',

    # Best Sellers in Board Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Board/zgbs/toys-and-games/166225011/ref=zg_bs_nav_t_3_166224011',

    # Best Sellers in Card Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Card/zgbs/toys-and-games/166239011/ref=zg_bs_nav_t_3_166225011',

    # Best Sellers in Dice & Gaming Dice
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Dice-Gaming/zgbs/toys-and-games/1265807011/ref=zg_bs_nav_t_3_166239011',

    # Best Sellers in Floor Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Floor/zgbs/toys-and-games/166250011/ref=zg_bs_nav_t_3_274314011',

    # Best Sellers in Game Accessories
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Game-Accessories/zgbs/toys-and-games/166221011/ref=zg_bs_nav_t_3_166250011',

    # Best Sellers in Game Pieces
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Game-Pieces/zgbs/toys-and-games/1265811011/ref=zg_bs_nav_t_3_166221011',

    # Best Sellers in Game Collections
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Game-Collections/zgbs/toys-and-games/166267011/ref=zg_bs_nav_t_2_166220011',

    # Best Sellers in Rec Room Games & Equipment for Kids
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Rec-Room-Equipment-Kids/zgbs/toys-and-games/166249011/ref=zg_bs_nav_t_3_166267011',

    # Best Sellers in Kids' Handheld Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Handheld/zgbs/toys-and-games/166179011/ref=zg_bs_nav_t_2_166220011',

    # Best Sellers in Stacking Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Stacking/zgbs/toys-and-games/166263011/ref=zg_bs_nav_t_3_166179011',

    # Best Sellers in Standard Playing Card Decks
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Standard-Playing-Card-Decks/zgbs/toys-and-games/166244011/ref=zg_bs_nav_t_3_166263011',

    # Best Sellers in Domino & Tile Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Domino-Tile/zgbs/toys-and-games/166248011/ref=zg_bs_nav_t_3_166244011',

    # Best Sellers in Collectible Card Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Collectible-Card/zgbs/toys-and-games/166242011/ref=zg_bs_nav_t_3_166248011',

    # Best Sellers in Collectible Trading Card Decks & Sets
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Collectible-Trading-Card-Decks-Sets/zgbs/toys-and-games/2522067011/ref=zg_bs_nav_t_2_166242011',

    # Best Sellers in Collectible Trading Card Albums, Cases & Sleeves
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Collectible-Trading-Card-Albums-Cases-Sleeves/zgbs/toys-and-games/5374108011/ref=zg_bs_nav_t_3_2522067011',

    # Best Sellers in Collectible Trading Card Booster Packs
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Collectible-Trading-Card-Booster-Packs/zgbs/toys-and-games/5374111011/ref=zg_bs_nav_t_3_2522067011',

    # Best Sellers in Travel Games
    # 'https://www.amazon.com/Best-Sellers-Toys-Games-Travel/zgbs/toys-and-games/166265011/ref=zg_bs_nav_t_3_166248011',

    # Best Sellers in Women's Leggings
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Leggings/zgbs/apparel/1258967011/ref=zg_bs_nav_a_2_1040660',

    # Best Sellers in Women's Sweaters
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Sweaters/zgbs/apparel/1044456/ref=zg_bs_nav_a_3_1258967011',

    # Best Sellers in Women's Cardigans
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Cardigans/zgbs/apparel/1044612/ref=zg_bs_nav_a_3_1044456',

    # Best Sellers in Women's Pullover Sweaters
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Pullover-Sweaters/zgbs/apparel/2368384011/ref=zg_bs_nav_a_4_1044612',

    # Best Sellers in Women's Sweater Vests
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Sweater-Vests/zgbs/apparel/1044606/ref=zg_bs_nav_a_4_2368385011',

    # Best Sellers in Women's Socks & Hosiery
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Socks-Hosiery/zgbs/apparel/1044886/ref=zg_bs_nav_a_2_1040660',

    # Best Sellers in Women's Casual Socks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Casual-Socks/zgbs/apparel/2376196011/ref=zg_bs_nav_a_3_1044886',

    # Best Sellers in Women's Dress & Trouser Socks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Dress-Trouser-Socks/zgbs/apparel/2376197011/ref=zg_bs_nav_a_4_2376196011',

    # Best Sellers in Women's Athletic Socks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Socks/zgbs/apparel/1044920/ref=zg_bs_nav_a_4_2376197011',

    # Best Sellers in Women's No Show & Liner Socks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-No-Show-Liner-Socks/zgbs/apparel/2376200011/ref=zg_bs_nav_a_4_2376199011',

    # # Best Sellers in Blouses & Button-Down Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Blouses-Button-Down-Shirts/zgbs/apparel/2368365011/ref=zg_bs_nav_a_3_2368343011',

    # # Best Sellers in Women's Knits & Tees
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Knits-Tees/zgbs/apparel/1044544/ref=zg_bs_nav_a_4_5418124011',

    # # Best Sellers in Women's Tanks & Camis
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Tanks-Camis/zgbs/apparel/2368344011/ref=zg_bs_nav_a_4_1044544',

    # # Best Sellers in Women's Tunics
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Tunics/zgbs/apparel/5418125011/ref=zg_bs_nav_a_4_2368344011',

    # # Best Sellers in Women's Fashion Hoodies & Sweatshirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Fashion-Hoodies-Sweatshirts/zgbs/apparel/1258603011/ref=zg_bs_nav_a_2_1040660',

    # # Best Sellers in Women's Jeans
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Jeans/zgbs/apparel/1048188/ref=zg_bs_nav_a_3_1258603011',

    # # Best Sellers in Women's Casual Pants & Capris
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Casual-Pants-Capris/zgbs/apparel/2348576011/ref=zg_bs_nav_a_3_1048184',

    # # Best Sellers in Women's Wear to Work Pants & Capris
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Wear-Work-Pants-Capris/zgbs/apparel/2528696011/ref=zg_bs_nav_a_4_2348576011',

    # # Best Sellers in Women's Athletic Hoodies
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Hoodies/zgbs/apparel/1044642/ref=zg_bs_nav_a_3_3456051',

    # # Best Sellers in Women's Sweatshirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Sweatshirts/zgbs/apparel/1044608/ref=zg_bs_nav_a_4_1044642',

    # # Best Sellers in Women's Athletic Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Jackets/zgbs/apparel/2211994011/ref=zg_bs_nav_a_4_1044608',

    # # Best Sellers in Women's Athletic Clothing Sets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Sets/zgbs/apparel/2374290011/ref=zg_bs_nav_a_4_2211994011',

    # # Best Sellers in Women's Athletic Shirts & Tees
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Shirts-Tees/zgbs/apparel/1046580/ref=zg_bs_nav_a_4_2374290011',

    # # Best Sellers in Women's Athletic Pants
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Pants/zgbs/apparel/1046600/ref=zg_bs_nav_a_4_1046580',

    # # Best Sellers in Women's Athletic Leggings
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Leggings/zgbs/apparel/1046592/ref=zg_bs_nav_a_4_1046600',

    # # Best Sellers in Women's Athletic Shorts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Shorts/zgbs/apparel/1046590/ref=zg_bs_nav_a_4_1046592',

    # # Best Sellers in Women's Athletic Base Layers
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Base-Layers/zgbs/apparel/2211982011/ref=zg_bs_nav_a_4_2211990011',

    # # Best Sellers in Women's Sports Bras
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Sports-Bras/zgbs/apparel/1044990/ref=zg_bs_nav_a_4_2211982011',

    # # Best Sellers in Women's Athletic Underwear
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Underwear/zgbs/apparel/1046606/ref=zg_bs_nav_a_4_1044990',

    # # Best Sellers in Women's Athletic Socks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Athletic-Socks/zgbs/apparel/1044920/ref=zg_bs_nav_a_4_1046606',

    # Men's Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Running/zgbs/shoes/679286011/ref=zg_bs_nav_shoe_3_6127770011',

    # Men's Road Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Road-Running/zgbs/shoes/14210389011/ref=zg_bs_nav_shoe_4_679286011',

    # # Men's Track & Field & Cross Country Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Track-Field-Cross-Country/zgbs/shoes/3420973011/ref=zg_bs_nav_shoe_5_14210389011',

    # # Men's Trail Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Trail-Running/zgbs/shoes/1264575011/ref=zg_bs_nav_shoe_5_3420973011',

    # # Fashion Scarves
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Fashion-Scarves/zgbs/apparel/2474943011',

    # Men's Shirts
    'https://www.amazon.com/Best-Sellers-Clothing-Mens-Shirts/zgbs/apparel/2476517011/ref=zg_bs_nav_a_2_1040658',

    # Men's T-Shirts
    'https://www.amazon.com/Best-Sellers-Clothing-Mens-T-Shirts/zgbs/apparel/1045624/ref=zg_bs_nav_a_3_2476517011',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__min_amazon_rating = 4.0

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'bestsellers.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'bestsellers.py -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
    run(ebay_store_id=ebay_store_id)


def run(ebay_store_id):
    task_id = uuid.uuid4()
    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True
    scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id)

def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls = __start_urls
    min_amazon_rating = __min_amazon_rating

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_bestseller',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            list_new=True,
            min_amazon_rating=min_amazon_rating)
        process.start()
    else:
        logger.error('No amazon items found')
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
