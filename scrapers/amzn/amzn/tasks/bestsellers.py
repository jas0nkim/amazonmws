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
    'https://www.amazon.com/Best-Sellers-Clothing-Womens-Leggings/zgbs/apparel/1258967011/ref=zg_bs_nav_a_2_1040660',

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
    
    # # Women's Pants
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Pants/zgbs/apparel/1048184/ref=zg_bs_nav_a_2_1040660',

    # # Women's Casual Pants & Capris
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Casual-Pants-Capris/zgbs/apparel/2348576011/ref=zg_bs_nav_a_3_1048184',

    # # Women's Wear to Work Pants & Capris
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Wear-Work-Pants-Capris/zgbs/apparel/2528696011/ref=zg_bs_nav_a_4_2348576011',

    # # Women's Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Womens/zgbs/shoes/679337011/ref=zg_bs_nav_shoe_1_shoe',

    # # Women's Boots
    # 'https://www.amazon.com/Best-Sellers-Shoes-Womens-Boots/zgbs/shoes/679380011/ref=zg_bs_nav_shoe_2_679337011',

    # # Women's Mid-Calf Boots
    # 'https://www.amazon.com/Best-Sellers-Shoes-Womens-Mid-Calf-Boots/zgbs/shoes/11721154011/ref=zg_bs_nav_shoe_3_679380011',

    # # Women's Knee-High Boots
    # 'https://www.amazon.com/Best-Sellers-Shoes-Womens-Knee-High-Boots/zgbs/shoes/11721155011/ref=zg_bs_nav_shoe_4_11721156011',

    # # Women's Coats, Jackets & Vests
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Coats-Jackets-Vests/zgbs/apparel/1044646/ref=zg_bs_nav_a_2_1040660',

    # # Women's Down Coats & Parkas
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Down-Coats-Parkas/zgbs/apparel/12643250011/ref=zg_bs_nav_a_3_1044646',

    # # Women's Down Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Down-Jackets-Coats/zgbs/apparel/2348894011/ref=zg_bs_nav_a_4_12643250011',

    # # Women's Parkas
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Parkas/zgbs/apparel/12643251011/ref=zg_bs_nav_a_5_2348894011',

    # # Women's Wool & Pea Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Wool-Pea-Coats/zgbs/apparel/12643255011/ref=zg_bs_nav_a_3_1044646',

    # # Women's Trench, Rain & Anoraks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Trench-Rain-Anoraks/zgbs/apparel/2348895011/ref=zg_bs_nav_a_4_12643255011',

    # # Women's Anoraks
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Anoraks/zgbs/apparel/7132356011/ref=zg_bs_nav_a_4_2348895011',

    # # Women's Raincoats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Raincoats/zgbs/apparel/7132359011/ref=zg_bs_nav_a_5_7132356011',

    # # Women's Trench Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Trench-Coats/zgbs/apparel/7132360011/ref=zg_bs_nav_a_5_7132359011',

    # # Women's Quilted Lightweight Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Quilted-Lightweight-Jackets/zgbs/apparel/7132358011/ref=zg_bs_nav_a_3_1044646',

    # # Women's Casual Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Casual-Jackets/zgbs/apparel/12643253011/ref=zg_bs_nav_a_4_7132358011',

    # # Women's Denim Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Denim-Jackets/zgbs/apparel/7132357011/ref=zg_bs_nav_a_4_12643253011',

    # # Women's Leather & Faux Leather Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Leather-Faux-Jackets-Coats/zgbs/apparel/2348892011/ref=zg_bs_nav_a_4_7132357011',

    # # Women's Fur & Faux Fur Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Fur-Faux-Jackets-Coats/zgbs/apparel/2348896011/ref=zg_bs_nav_a_4_2348892011',

    # # Women's Outerwear Vests
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Outerwear-Vests/zgbs/apparel/2348899011/ref=zg_bs_nav_a_4_2348896011',

    # # Women's Active & Performance Outerwear
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Active-Performance-Outerwear/zgbs/apparel/2348893011/ref=zg_bs_nav_a_4_2348899011',

    # # Women's Fleece Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Fleece-Jackets-Coats/zgbs/apparel/2348897011/ref=zg_bs_nav_a_4_2348893011',

    # # Women's Insulated Shells
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Insulated-Shells/zgbs/apparel/7132349011/ref=zg_bs_nav_a_5_2348897011',

    # # Women's Active Wind & Rain Outerwear
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Active-Wind-Rain-Outerwear/zgbs/apparel/12643246011/ref=zg_bs_nav_a_5_7132349011',

    # # Women's Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Dresses/zgbs/apparel/1045024/ref=zg_bs_nav_a_2_1040660',

    # # Women's Casual Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Casual-Dresses/zgbs/apparel/2346727011/ref=zg_bs_nav_a_3_1045024',

    # # Women's Wear to Work Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Wear-Work-Dresses/zgbs/apparel/2346728011/ref=zg_bs_nav_a_4_2346727011',

    # # Women's Cocktail Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Cocktail-Dresses/zgbs/apparel/11006703011/ref=zg_bs_nav_a_4_2346728011',

    # # Women's Formal Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Formal-Dresses/zgbs/apparel/11006704011/ref=zg_bs_nav_a_4_11006703011',

    # # Wedding & Bridal Party Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Wedding-Bridal-Party-Dresses/zgbs/apparel/2969486011/ref=zg_bs_nav_a_4_11006704011',

    # # Wedding Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Wedding-Dresses/zgbs/apparel/2969489011/ref=zg_bs_nav_a_4_2969486011',

    # # Bridesmaid Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Bridesmaid-Dresses/zgbs/apparel/2969491011/ref=zg_bs_nav_a_5_2969489011',

    # # Mother of the Bride Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mother-Bride-Dresses/zgbs/apparel/2969490011/ref=zg_bs_nav_a_5_2969491011',

    # # Prom & Homecoming Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Prom-Homecoming-Dresses/zgbs/apparel/11006705011/ref=zg_bs_nav_a_3_1045024',

    # # Women's Club Dresses
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Club-Dresses/zgbs/apparel/11006702011/ref=zg_bs_nav_a_4_11006705011',

    # # Women's Tops & Tees
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Tops-Tees/zgbs/apparel/2368343011/ref=zg_bs_nav_a_2_1040660',

    # # Blouses & Button-Down Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Blouses-Button-Down-Shirts/zgbs/apparel/2368365011/ref=zg_bs_nav_a_3_2368343011',

    # # Women's Henley Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Henley-Shirts/zgbs/apparel/5418124011/ref=zg_bs_nav_a_4_2368365011',

    # # Women's Knits & Tees
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Knits-Tees/zgbs/apparel/1044544/ref=zg_bs_nav_a_4_5418124011',

    # # Women's Polo Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Polo-Shirts/zgbs/apparel/1044548/ref=zg_bs_nav_a_4_1044544',

    # # Women's Tanks & Camis
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Tanks-Camis/zgbs/apparel/2368344011/ref=zg_bs_nav_a_4_1044548',

    # # Women's Tunics
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Tunics/zgbs/apparel/5418125011/ref=zg_bs_nav_a_4_2368344011',

    # # Women's Fashion Vests
    # 'https://www.amazon.com/Best-Sellers-Clothing-Womens-Fashion-Vests/zgbs/apparel/5418126011/ref=zg_bs_nav_a_4_5418125011',

    # # Men's Outerwear Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Outerwear-Jackets-Coats/zgbs/apparel/1045830/ref=zg_bs_nav_a_2_1040658',

    # # Men's Active & Performance Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Active-Performance-Jackets/zgbs/apparel/2476494011/ref=zg_bs_nav_a_3_1045830',

    # # Men's Down Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Down-Jackets-Coats/zgbs/apparel/2476602011/ref=zg_bs_nav_a_4_2476494011',

    # # Men's Fleece Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Fleece-Jackets-Coats/zgbs/apparel/2476496011/ref=zg_bs_nav_a_5_2476602011',

    # # Men's Active & Performance Insulated Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Active-Performance-Insulated-Jackets/zgbs/apparel/7132366011/ref=zg_bs_nav_a_5_2476496011',

    # # Men's Active & Performance Shell Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Active-Performance-Shell-Jackets/zgbs/apparel/7132367011/ref=zg_bs_nav_a_5_7132366011',

    # # Men's Leather & Faux Leather Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Leather-Faux-Jackets-Coats/zgbs/apparel/2476603011/ref=zg_bs_nav_a_3_1045830',

    # # Men's Lightweight Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Lightweight-Jackets/zgbs/apparel/2528780011/ref=zg_bs_nav_a_4_2476603011',

    # # Men's Cotton Lightweight Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Cotton-Lightweight-Jackets/zgbs/apparel/7132374011/ref=zg_bs_nav_a_4_2528780011',

    # # Men's Denim Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Denim-Jackets/zgbs/apparel/2476495011/ref=zg_bs_nav_a_5_7132374011',

    # # Men's Golf Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Golf-Jackets/zgbs/apparel/2420126011/ref=zg_bs_nav_a_5_2476495011',

    # # Men's Varsity Jackets
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Varsity-Jackets/zgbs/apparel/7132373011/ref=zg_bs_nav_a_5_2420126011',

    # # Men's Windbreakers
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Windbreakers/zgbs/apparel/7132372011/ref=zg_bs_nav_a_5_7132373011',

    # # Men's Trench & Rain Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Trench-Rain-Coats/zgbs/apparel/2476604011/ref=zg_bs_nav_a_3_1045830',

    # # Men's Outerwear Vests
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Outerwear-Vests/zgbs/apparel/2562597011/ref=zg_bs_nav_a_4_2476604011',

    # # Men's Wool Jackets & Coats
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Wool-Jackets-Coats/zgbs/apparel/2476613011/ref=zg_bs_nav_a_4_2562597011',

    # # Men's Work Utility & Safety Outerwear
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Work-Utility-Safety-Outerwear/zgbs/apparel/6572902011/ref=zg_bs_nav_a_4_2476613011',

    # # Men's Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Shirts/zgbs/apparel/2476517011/ref=zg_bs_nav_a_2_1040658',

    # # Men's T-Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-T-Shirts/zgbs/apparel/1045624/ref=zg_bs_nav_a_3_2476517011',

    # # Men's Tank Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Tank-Shirts/zgbs/apparel/2476518011/ref=zg_bs_nav_a_4_1045624',

    # # Men's Polo Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Polo-Shirts/zgbs/apparel/1045640/ref=zg_bs_nav_a_4_2476518011',

    # # Men's Henley Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Henley-Shirts/zgbs/apparel/1045642/ref=zg_bs_nav_a_4_1045640',

    # # Men's Casual Button-Down Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Casual-Button-Down-Shirts/zgbs/apparel/1045630/ref=zg_bs_nav_a_4_1045642',

    # # Men's Dress Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Dress-Shirts/zgbs/apparel/1045626/ref=zg_bs_nav_a_4_1045630',

    # # Men's Tuxedo Shirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Tuxedo-Shirts/zgbs/apparel/2476499011/ref=zg_bs_nav_a_4_1045626',

    # # Men's Fashion Hoodies & Sweatshirts
    # 'https://www.amazon.com/Best-Sellers-Clothing-Mens-Fashion-Hoodies-Sweatshirts/zgbs/apparel/1258644011/ref=zg_bs_nav_a_2_1040658',

    # # Men's Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Running/zgbs/shoes/679286011/ref=zg_bs_nav_shoe_3_6127770011',

    # # Men's Road Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Road-Running/zgbs/shoes/14210389011/ref=zg_bs_nav_shoe_4_679286011',

    # # Men's Track & Field & Cross Country Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Track-Field-Cross-Country/zgbs/shoes/3420973011/ref=zg_bs_nav_shoe_5_14210389011',

    # # Men's Trail Running Shoes
    # 'https://www.amazon.com/Best-Sellers-Shoes-Mens-Trail-Running/zgbs/shoes/1264575011/ref=zg_bs_nav_shoe_5_3420973011',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__min_amazon_rating = 4.0

def main(argv):
    ebay_store_id = 1
    force_crawl = False
    try:
        opts, args = getopt.getopt(argv, "hfe:", ["ebaystoreid=", "forcecrawl" ])
    except getopt.GetoptError:
        print 'bestsellers.py [-f] -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'bestsellers.py [-f] -e <1|2|3|4|...ebaystoreid>'
            sys.exit()
        elif opt in ("-e", "--ebaystoreid"):
            ebay_store_id = int(arg)
        elif opt in ("-f", "--forcecrawl"):
            force_crawl = True
    run(ebay_store_id=ebay_store_id, force_crawl=force_crawl)


def run(ebay_store_id, force_crawl=False):
    task_id = uuid.uuid4()
    premium = False
    if ebay_store_id in __premium_ebay_store_ids:
        premium = True
    scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id, force_crawl=force_crawl)

def scrape_amazon(premium, task_id, ebay_store_id, force_crawl=False):
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
            min_amazon_rating=min_amazon_rating,
            force_crawl=force_crawl,
            dont_list_ebay=True)
        process.start()
    else:
        logger.error('No amazon items found')
        return False
    return True

if __name__ == "__main__":
    main(sys.argv[1:])
