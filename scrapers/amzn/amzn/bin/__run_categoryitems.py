import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws.loggers import set_root_graylogger, GrayLogger as logger


if __name__ == "__main__":
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_base', 
        start_urls=[
            # Tools & Home Improvement : Lighting & Ceiling Fans : Lamps & Shades : Desk Lamps
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A3736561%2Cn%3A1063292%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=living+accents&ie=UTF8&qid=1454455492&rnid=5016682011',

            # Tools & Home Improvement : Lighting & Ceiling Fans : Lamps & Shades : Floor Lamps
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A3736561%2Cn%3A1063294%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=living+accents&ie=UTF8&qid=1454455553&rnid=5016682011',

            # Tools & Home Improvement : Lighting & Ceiling Fans : Wall Lights : Night Lights
            'http://www.amazon.com/s/ref=sr_nr_n_3?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A3736651%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=living+accents&ie=UTF8&qid=1454455566&rnid=468240',

            # Tools & Home Improvement 
            'http://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A228013%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=228013&keywords=living+accents&ie=UTF8&qid=1454455572',

            # Tools & Home Improvement : Light Bulbs : LED Bulbs
            'http://www.amazon.com/s/ref=sr_nr_n_7?fst=as%3Aoff&rh=n%3A228013%2Cn%3A2314207011%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=living+accents&ie=UTF8&qid=1454455591&rnid=468240',

            # Tools & Home Improvement : Power & Hand Tools
            'http://www.amazon.com/gp/search/ref=sr_nr_n_17?fst=as%3Aoff&rh=n%3A228013%2Cn%3A328182011%2Ck%3Aliving+accents%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=living+accents&ie=UTF8&qid=1454455591&rnid=468240',

            #  Office Products : Office Electronics : Calculators
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A1064954%2Cn%3A%211084128%2Cn%3A172574%2Cn%3A172518%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=172518&ie=UTF8&qid=1454456000&rnid=5016682011',

            # Office Products : Office Electronics : Telephones & Accessories
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A1064954%2Cn%3A%211084128%2Cn%3A172574%2Cn%3A172606%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=172606&ie=UTF8&qid=1454456053&rnid=5016682011',

            # Office Products : Office Electronics : Telephones & Accessories : Telephone Accessories
            'http://www.amazon.com/gp/search/ref=sr_nr_n_4?fst=as%3Aoff&rh=n%3A1064954%2Cn%3A%211084128%2Cn%3A172574%2Cn%3A172606%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A172607&bbn=172606&ie=UTF8&qid=1454456054&rnid=172606',

            # Office Products : Office Electronics : Telephones & Accessories : Telephone Accessories : Headsets
            'http://www.amazon.com/s/ref=sr_nr_n_3?fst=as%3Aoff&rh=n%3A1064954%2Cn%3A%211084128%2Cn%3A172574%2Cn%3A172606%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A172607%2Cn%3A229193&bbn=172607&ie=UTF8&qid=1454456076&rnid=172607',

            # Baby Products : Feeding : Baby Foods
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A165796011%2Cn%3A%21165797011%2Cn%3A166777011%2Cn%3A16323111%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=16323111&ie=UTF8&qid=1454456809&rnid=5016682011',

            # Baby Products : Feeding : Baby Foods : Baby Formula
            'http://www.amazon.com/s/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A165796011%2Cn%3A%21165797011%2Cn%3A166777011%2Cn%3A16323111%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A16323121&bbn=16323111&ie=UTF8&qid=1454456810&rnid=16323111',

            # # Home & Kitchen : Heating, Cooling & Air Quality : Space Heaters & Accessories : Space Heaters
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206324011%2Cn%3A9425950011%2Cn%3A510182%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=510182&ie=UTF8&qid=1453674975&rnid=5016682011',

            # # Home & Kitchen : Heating, Cooling & Air Quality : Humidifiers & Accessories
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206324011%2Cn%3A267555011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=267555011&ie=UTF8&qid=1453675043&rnid=5016682011',

            # # Home & Kitchen : Heating, Cooling & Air Quality : Air Purifiers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206324011%2Cn%3A267554011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=267554011&ie=UTF8&qid=1453675066&rnid=5016682011',

            # # Home & Kitchen : Home Decor : Weather Instruments
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063278%2Cn%3A554038%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=554038&ie=UTF8&qid=1453675092&rnid=5016682011',

            # # Home & Kitchen : Heating, Cooling & Air Quality : Dehumidifiers & Accessories : Dehumidifiers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206324011%2Cn%3A9425949011%2Cn%3A267557011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=267557011&ie=UTF8&qid=1453675115&rnid=5016682011',

            # # Health & Personal Care : Household Supplies : Air Fresheners : Prime Eligible
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A15342811%2Cn%3A15356121%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_n_is_pantry%3A8417613011&bbn=15356121&ie=UTF8&qid=1453675151&rnid=8410679011',

            # # Home & Kitchen : Cleaning Supplies : Brushes
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A15342891%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15342891&ie=UTF8&qid=1453675177&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Dusting
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A15356181%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15356181&ie=UTF8&qid=1453675200&rnid=5016682011',

            # # Health & Personal Care : Household Supplies : Cleaning Tools : Gloves
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A15342811%2Cn%3A15342831%2Cn%3A15342901%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15342901&ie=UTF8&qid=1453675238',

            # # Home & Kitchen : Cleaning Supplies : Mopping
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A2245503011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2245503011&ie=UTF8&qid=1453675291&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Paper Towels
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A15347401%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15347401&ie=UTF8&qid=1453675314&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Sponges
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A15754811%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15754811&ie=UTF8&qid=1453675338&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Squeegees
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A2245500011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2245500011&ie=UTF8&qid=1453675361&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Sweeping
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A2245502011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2245502011&ie=UTF8&qid=1453675389&rnid=5016682011',

            # # Home & Kitchen : Cleaning Supplies : Trash Bags
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cn%3A15342971%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15342971&ie=UTF8&qid=1453675416&rnid=5016682011',

            # # Health & Personal Care : Sports Nutrition : Protein
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A6973663011%2Cn%3A6973704011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6973704011&ie=UTF8&qid=1453675453&rnid=5016682011',

            # # Health & Personal Care : Sports Nutrition : Endurance & Energy
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A6973663011%2Cn%3A6973669011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6973669011&ie=UTF8&qid=1453675480&rnid=5016682011',

            # # Health & Personal Care : Sports Nutrition : Amino Acids
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A6973663011%2Cn%3A10781161%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=10781161&ie=UTF8&qid=1453675507&rnid=5016682011',

            # # Health & Personal Care : Vitamins & Dietary Supplements : Weight Loss : Appetite Control & Suppressants
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A3764441%2Cn%3A3774931%2Cn%3A3774941%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3774941&ie=UTF8&qid=1453675550&rnid=5016682011',

            # # Health & Personal Care : Vitamins & Dietary Supplements : Weight Loss : Supplements
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A3764441%2Cn%3A3774931%2Cn%3A3775151%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3775151&ie=UTF8&qid=1453675583&rnid=5016682011',

            # # Health & Personal Care : Vitamins & Dietary Supplements : Weight Loss : Shakes & Powders
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A3764441%2Cn%3A3774931%2Cn%3A4076121%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=4076121&ie=UTF8&qid=1453675610&rnid=5016682011',

            # # Health & Personal Care : Vitamins & Dietary Supplements : Herbal Supplements : Ginseng
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A3764441%2Cn%3A3764461%2Cn%3A3765711%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3765711&ie=UTF8&qid=1453675637&rnid=5016682011',

            # # Health & Personal Care : Vitamins & Dietary Supplements : Herbal Supplements : Echinacea
            # 'https://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%213760931%2Cn%3A3764441%2Cn%3A3764461%2Cn%3A3765501%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3765501&ie=UTF8&qid=1453675658&rnid=5016682011',

            # # Health & Personal Care : Build Muscle
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760901%2Cn%3A%212334097011%2Cn%3A%212334159011%2Cn%3A6195905011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6195905011&ie=UTF8&qid=1453675694&rnid=5016682011',

            # # Beauty : Skin Care : Face
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11060451%2Cn%3A11060711%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11060711&ie=UTF8&qid=1453675725&rnid=5016682011',

            # # Beauty : Skin Care : Eyes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11060451%2Cn%3A11061941%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11061941&ie=UTF8&qid=1453675748&rnid=5016682011',

            # # Beauty : Bath & Body Care : Lip Care
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11055991%2Cn%3A3761351%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3761351&ie=UTF8&qid=1453675771&rnid=5016682011',

            # # Beauty : Bath & Body Care
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11055991%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11055991&ie=UTF8&qid=1453675795&rnid=5016682011',

            # # Beauty : Bath & Body Care : Hands, Feet & Nails
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11055991%2Cn%3A11062211%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11062211&ie=UTF8&qid=1453675835&rnid=5016682011',

            # # Beauty : Beauty Tools
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%212334087011%2Cn%3A%212334149011%2Cn%3A2234655011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2234655011&ie=UTF8&qid=1453675861&rnid=5016682011',

            # # Beauty : Hair Care : Tools & Appliances
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11058091&ie=UTF8&qid=1453675957&rnid=5016682011',

            # # Pet Supplies : Dogs : Food : Dry
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975359011%2Cn%3A2975360011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975360011&ie=UTF8&qid=1453678306&rnid=5016682011',

            # # Pet Supplies : Dogs : Food : Wet
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975359011%2Cn%3A2975361011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975361011&ie=UTF8&qid=1453678333&rnid=5016682011',

            # # Pet Supplies : Dogs : Food : Dehydrated/Freeze-Dried
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975359011%2Cn%3A6514320011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6514320011&ie=UTF8&qid=1453678355&rnid=5016682011',

            # # Pet Supplies : Dogs : Food : Food Toppers
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975359011%2Cn%3A6514323011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6514323011&ie=UTF8&qid=1453678381&rnid=5016682011',

            # # Pet Supplies : Dogs : Food : Frozen
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975359011%2Cn%3A7239525011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=7239525011&ie=UTF8&qid=1453678408&rnid=5016682011',

            # # Pet Supplies : Dogs : Treats : Animal Ears
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975434011%2Cn%3A3024234011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3024234011&ie=UTF8&qid=1453678434&rnid=5016682011',

            # # Pet Supplies : Dogs : Treats : Bones
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975434011%2Cn%3A2975435011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975435011&ie=UTF8&qid=1453678458&rnid=5016682011',

            # # Pet Supplies : Dogs : Treats : Cookies, Biscuits & Snacks
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975434011%2Cn%3A2975436011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975436011&ie=UTF8&qid=1453678480&rnid=5016682011',

            # # Pet Supplies : Dogs : Treats : Jerky
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975434011%2Cn%3A2975439011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975439011&ie=UTF8&qid=1453678502&rnid=5016682011',

            # # Pet Supplies : Dogs : Treats : Rawhide
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975434011%2Cn%3A2975440011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975440011&ie=UTF8&qid=1453678524&rnid=5016682011',

            # # Pet Supplies : Dogs : Beds & Furniture : Bed Blankets
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975326011%2Cn%3A3024177011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3024177011&ie=UTF8&qid=1453678554&rnid=5016682011',

            # # Pet Supplies : Dogs : Beds & Furniture : Bed Covers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975326011%2Cn%3A2975327011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975327011&ie=UTF8&qid=1453678581&rnid=5016682011',

            # # Pet Supplies : Dogs : Beds & Furniture : Beds
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975326011%2Cn%3A2975330011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975330011&ie=UTF8&qid=1453678607&rnid=5016682011',

            # # Pet Supplies : Dogs : Beds & Furniture : Stairs & Steps
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975326011%2Cn%3A2975332011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975332011&ie=UTF8&qid=1453678628&rnid=5016682011',

            # # Pet Supplies : Dogs : Beds & Furniture : Bed Mats
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975326011%2Cn%3A3024178011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3024178011&ie=UTF8&qid=1453678658&rnid=5016682011',

            # # Pet Supplies : Dogs : Grooming : Brushes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975362011%2Cn%3A2975363011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975363011&ie=UTF8&qid=1453678698&rnid=5016682011',

            # # Pet Supplies : Dogs : Doors, Gates & Ramps : Doors
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975346011%2Cn%3A2975349011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975349011&ie=UTF8&qid=1453678736&rnid=5016682011',

            # # Pet Supplies : Dogs : Health Supplies
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975377011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975377011&ie=UTF8&qid=1453678759&rnid=5016682011',

            # # Pet Supplies : Dogs : Toys : Balls
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975413011%2Cn%3A2975414011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975414011&ie=UTF8&qid=1453678788&rnid=5016682011',

            # # Pet Supplies : Dogs : Toys : Chew Toys
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975413011%2Cn%3A2975415011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975415011&ie=UTF8&qid=1453678816&rnid=5016682011',

            # # Pet Supplies : Dogs : Toys : Ropes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975413011%2Cn%3A2975418011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975418011&ie=UTF8&qid=1453678842&rnid=5016682011',

            # # Pet Supplies : Dogs : Health Supplies : Dental Care
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975377011%2Cn%3A2975378011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975378011&ie=UTF8&qid=1453678877&rnid=5016682011',

            # # Pet Supplies : Dogs : Feeding & Watering Supplies : Nursing Supplies
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975351011%2Cn%3A2975356011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975356011&ie=UTF8&qid=1453678904&rnid=5016682011',

            # # Pet Supplies : Dogs : Health Supplies : Itch Remedies
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975377011%2Cn%3A2975393011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975393011&ie=UTF8&qid=1453678927&rnid=5016682011',

            # # Pet Supplies : Dogs : Feeding & Watering Supplies : Raised Bowls & Feeding Stations
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975351011%2Cn%3A2975357011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975357011&ie=UTF8&qid=1453678953&rnid=5016682011',

            # # Pet Supplies : Dogs : Feeding & Watering Supplies : Food Storage
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975351011%2Cn%3A2975354011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975354011&ie=UTF8&qid=1453678983&rnid=5016682011',

            # # Pet Supplies : Dogs : Training & Behavior Aids : Training Collars
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975312011%2Cn%3A2975420011%2Cn%3A2975428011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975428011&ie=UTF8&qid=1453679014&rnid=5016682011',

            # # Pet Supplies : Birds : Toys
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975221011%2Cn%3A2975240011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975240011&ie=UTF8&qid=1453679041&rnid=5016682011',

            # # Pet Supplies : Reptiles & Amphibians : Food
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975504011%2Cn%3A2975505011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2975505011&ie=UTF8&qid=1453679059&rnid=5016682011',

            # # Pet Supplies : Small Animals : Treats
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975520011%2Cn%3A3048877011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3048877011&ie=UTF8&qid=1453679081&rnid=5016682011',

            # # Automotive : Interior Accessories : Air Fresheners
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A15684181%2Cn%3A%2115690151%2Cn%3A15857501%2Cn%3A15735121%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15735121&ie=UTF8&qid=1453679120&rnid=5016682011',

            # # Automotive : Car Care : Cleaning Kits
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A15684181%2Cn%3A%2115690151%2Cn%3A15718271%2Cn%3A15718281%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15718281&ie=UTF8&qid=1453679158&rnid=5016682011',

            # # search - car charger
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acar+charger%2Cp_85%3A2470955011&keywords=car+charger&ie=UTF8&qid=1453679262&rnid=2470954011',

            # # Cell Phones & Accessories : Cases, Holsters & Clips
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407760011%2Cp_85%3A2470955011%2Cp_n_feature_nine_browse-bin%3A10030581011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=2407760011&ie=UTF8&qid=1453679338&rnid=5016682011',

            # # Wearable Technology: Healthcare Devices
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A8849528011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=8849528011&ie=UTF8&qid=1453679390&rnid=5016682011',

            # # search - watch
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Awatch%2Cp_85%3A2470955011&keywords=watch&ie=UTF8&qid=1453679492&rnid=2470954011',

            # # Sports & Outdoors : Outdoor Recreation : Accessories : Sport Watches, search - watch
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3375251%2Cn%3A706814011%2Cn%3A11051400011%2Cn%3A378526011%2Ck%3Awatch%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=watch&ie=UTF8&qid=1453679527&rnid=5016682011',

            # # Appliances : Parts & Accessories
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2619525011%2Cn%3A%212619526011%2Cn%3A3741181%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3741181&ie=UTF8&qid=1453679678&rnid=5016682011',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making
            # 'https://www.amazon.com/s/ref=lp_12896081_nr_p_85_0?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011&bbn=12896081&ie=UTF8&qid=1452468937&rnid=2470954011',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Storage
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A8090936011&bbn=12896081&ie=UTF8&qid=1452468970&rnid=12896081',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Metal Stamping Tools
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A8090814011&bbn=12896081&ie=UTF8&qid=1452468970&rnid=12896081',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Polishing & Buffing
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A12896191&bbn=12896081&ie=UTF8&qid=1452469014&rnid=12896081',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Purse Making
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A3097796011&bbn=12896081&ie=UTF8&qid=1452469014&rnid=12896081',

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Jewelry Making Kits
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A12896171&bbn=12896081&ie=UTF8&qid=1452469014&rnid=12896081'

            # # Arts, Crafts & Sewing : Beading & Jewelry Making : Jewelry Making Tools & Accessories
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2617941011%2Cn%3A%212617942011%2Cn%3A12896081%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A12896181&bbn=12896081&ie=UTF8&qid=1452469014&rnid=12896081',

            # # # Beauty : Hair Care : Tools & Appliances
            # # 'https://www.amazon.com/s/fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=11058091&ie=UTF8&qid=1452469098&rnid=5016682011',

            # # Beauty : Hair Care : Tools & Appliances : Crimpers & Wavers
            # 'https://www.amazon.com/gp/search/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A3784341&bbn=11058091&ie=UTF8&qid=1452469102&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Curling Irons & Wands
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058251&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Diffusers & Dryer Attachments
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058111&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Brushes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058121&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Combs
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058131&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Cutting Tools
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A10676449011&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Rollers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A3784371&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Dryers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058141&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hair Rollers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A3784371&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Hot-Air Brushes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058221&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Beauty : Hair Care : Tools & Appliances : Straighteners
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11057241%2Cn%3A11058091%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A11058261&bbn=11058091&ie=UTF8&qid=1452469137&rnid=11058091',

            # # Home & Kitchen : Bath : Bath Rugs
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063242%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1063242&ie=UTF8&qid=1452469313&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories : Shower Accessories : Shower Caddies
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cn%3A3731941%2Cn%3A85969011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=85969011&ie=UTF8&qid=1452469364&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories : Bathroom Accessory Sets
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cn%3A3731911%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3731911&ie=UTF8&qid=1452469395&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories : Makeup Organizers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cn%3A3743871%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3743871&ie=UTF8&qid=1452469420&rnid=5016682011',

            # # Home & Kitchen : Bath : Bath Linen Sets
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A3731671%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3731671&ie=UTF8&qid=1452469446&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories : Holders & Dispensers
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cn%3A3731971%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=3731971&ie=UTF8&qid=1452469470&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories : Towel Holders : Towel Racks
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cn%3A16350971%2Cn%3A16350721%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=16350721&ie=UTF8&qid=1452469491&rnid=5016682011',

            # # Home & Kitchen : Bath : Bathroom Accessories
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063236%2Cn%3A1063238%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1063238&ie=UTF8&qid=1452469514&rnid=5016682011',

            # # # Home & Kitchen : Cleaning Supplies
            # # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=10802561&ie=UTF8&qid=1452469559&rnid=5016682011',
            
            # # Home & Kitchen : Cleaning Supplies : Air Fresheners
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A15356121&bbn=10802561&ie=UTF8&qid=1452469562&rnid=10802561',

            # # Home & Kitchen : Cleaning Supplies : Brushes
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A15342891&bbn=10802561&ie=UTF8&qid=1452469589&rnid=10802561',

            # # Home & Kitchen : Cleaning Supplies : Dusting
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A15356181&bbn=10802561&ie=UTF8&qid=1452469589&rnid=10802561',

            # # Home & Kitchen : Cleaning Supplies : Gloves
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A15342901&bbn=10802561&ie=UTF8&qid=1452469589&rnid=10802561',

            # # Home & Kitchen : Cleaning Supplies : Squeegees
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A2245500011&bbn=10802561&ie=UTF8&qid=1452469589&rnid=10802561',

            # # Home & Kitchen : Cleaning Supplies : Trash Bags
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A10802561%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A15342971&bbn=10802561&ie=UTF8&qid=1452469589&rnid=10802561',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Cables & Interconnects
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:172282,n:!493964,n:541966,n:172456,n:172463,p_85:2470955011,p_n_is-min-purchase-required:5016683011&bbn=172463&ie=UTF8&qid=1452469734&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Components
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:172282,n:!493964,n:541966,n:193870011,p_85:2470955011,p_n_is-min-purchase-required:5016683011&bbn=193870011&ie=UTF8&qid=1452469789&rnid=5016682011',

            # # # Automotive : Automotive Outlet
            # # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011&bbn=701624011&ie=UTF8&qid=1452469832&rnid=5016682011',
            
            # # Automotive : Automotive Outlet : Car Care
            # 'http://www.amazon.com/gp/search/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:15718271&bbn=701624011&ie=UTF8&qid=1452469836&rnid=15690151',

            # # Automotive : Automotive Outlet : Car Electronics & Accessories
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:2230642011&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Automotive : Automotive Outlet : Exterior Accessories
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:15857511&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Automotive : Automotive Outlet : Interior Accessories
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:15857501&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Automotive : Automotive Outlet : Lights & Lighting Accessories
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:15736321&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Automotive : Automotive Outlet : Motorcycle & Powersports
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:346333011&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Automotive : Automotive Outlet : Replacement Parts
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:15684181,n:!15690231,n:701624011,p_85:2470955011,p_n_is-min-purchase-required:5016683011,n:15719731&bbn=701624011&ie=UTF8&qid=1452469863&rnid=15690151',

            # # Home & Kitchen : Vacuums & Floor Care : Vacuums
            # 'http://www.amazon.com/s/?fst=as:off&rh=n:1055398,n:!1063498,n:510106,n:3743521,p_85:2470955011,p_n_is-min-purchase-required:5016683011&bbn=3743521&ie=UTF8&qid=1452470049&rnid=5016682011',

            # # Books : Reference : Foreign Language Study & Reference
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A283155%2Cn%3A21%2Cn%3A11773%2Cn%3A11811%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750399&rnid=5016682011',
            
            # # Beauty : Makeup : Eyes : Eyeliner
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11058281%2Cn%3A11058331%2Cn%3A11058521%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750464&rnid=5016682011',
            
            # # Beauty : Skin Care : Eyes : Masks & Pillows
            # 'https://www.amazon.com/s/fst=as%3Aoff&rh=n%3A7730093011%2Ck%3Akorean%2Cp_85%3A2470955011&keywords=korean&ie=UTF8&qid=1451750490&rnid=2941120011',
            
            # # Beauty : Skin Care : Face : Treatments & Masks : Masks
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11060451%2Cn%3A11060711%2Cn%3A11062031%2Cn%3A11061121%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750512&rnid=5016682011',

            # # Beauty : Makeup : Face : Foundation
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11058281%2Cn%3A11058691%2Cn%3A11058871%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750514&rnid=5016682011',

            # # Beauty : Bath & Body Care : Hands, Feet & Nails : Hand Creams & Lotions
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11055991%2Cn%3A11062211%2Cn%3A11062261%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750565&rnid=5016682011',            

            # # Home & Kitchen : Kitchen & Dining : Kitchen Utensils & Gadgets
            # 'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A284507%2Cn%3A289754%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750567&rnid=5016682011',

            # # Home & Kitchen : Kitchen & Dining : Dining & Entertaining : Flatware
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A284507%2Cn%3A13162311%2Cn%3A13218891%2Cn%3A13220831%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750592&rnid=5016682011',

            # # Home & Kitchen
            # 'https://www.amazon.com/s/?rh=n%3A1055398%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1055398&keywords=korean&ie=UTF8&qid=1451750596',

            # # Home & Kitchen : Bedding : Blankets & Throws : Bed Blankets
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A3732181%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750608&rnid=1063498',

            # # Electronics : Computers & Accessories
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011&keywords=computer+accessories&ie=UTF8&qid=1451750828&rnid=2470954011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Cables & Interconnects
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A172463%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750832&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750855&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Skins & Decals
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A3011392011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750888&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Lap Desks
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A3011392011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750888&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Chargers & Adapters
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A11041841%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750933&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Bags, Cases & Sleeves : Sleeves
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A172470%2Cn%3A335609011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750961&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Batteries
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A720576%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750982&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Cooling Pads
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A2243862011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751023&rnid=5016682011',

            # # Electronics : Computers & Accessories : Laptop Accessories : Docking Stations 
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A778660%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751028&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751057&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Keyboard & Mice Accessories : Wrist Rests
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A3012566011%2Cn%3A705324011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751095&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Monitor Accessories : Monitor Arms & Monitor Stands
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A281062%2Cn%3A490624011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751099&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Keyboard & Mice Accessories : Mouse Pads
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A3012566011%2Cn%3A705323011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751120&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Mice
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A11036491%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751153&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Audio & Video Accessories : Computer Speakers
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548951011%2Cn%3A172471%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751155&rnid=5016682011',

            # # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Cleaning & Repair : Repair Kits
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A281501%2Cn%3A13825561%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751192&rnid=5016682011',

            # # Electronics : Accessories & Supplies : Cord Management
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A281407%2Cn%3A11042051%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751252&rnid=5016682011',

            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acar+accessories%2Cp_85%3A2470955011&keywords=car+accessories&ie=UTF8&qid=1451751278&rnid=2470954011',

            # # # Cell Phones & Accessories : Accessories
            # # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751282&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Chargers & Power Adapters : Car Chargers 
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407761011%2Cn%3A2407770011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751323&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Mounts & Stands : Stands
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A7072563011%2Cn%3A7073961011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751333&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Car Accessories : Car Kits
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407759011%2Cn%3A2407764011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751370&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Accessory Kits
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407756011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751381&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Replacement Parts
            # 'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407780011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751410&rnid=5016682011',

            # # Cell Phones & Accessories : Accessories : Replacement Parts
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407780011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751410&rnid=5016682011',

            # # Tools & Home Improvement : Light Bulbs : LED Bulbs
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A322525011%2Cn%3A2314207011%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751525&rnid=5016682011',

            # # Tools & Home Improvement : Painting Supplies & Wall Treatments
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A228899%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751735&rnid=5016682011',

            # # Tools & Home Improvement : Lighting & Ceiling Fans : Wall Lights : Night Lights
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A5486429011%2Cn%3A3736651%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751757&rnid=5016682011',

            # # Tools & Home Improvement : Lighting & Ceiling Fans : Lamps & Shades : Table Lamps
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A3736561%2Cn%3A1063296%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751784&rnid=5016682011',

            # # Tools & Home Improvement : Lighting & Ceiling Fans : Outdoor Lighting : String Lights
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A495236%2Cn%3A3742221%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751823&rnid=5016682011',

            # # Home & Kitchen : Home Decor : Kids' Room Decor : Wall Decor
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A1063278%2Cn%3A404454011%2Cn%3A404458011%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751829&rnid=5016682011',

            # # Home & Kitchen : Bedding & Bath
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%2113900811%2Cn%3A%211063496%2Cn%3A%21251263011%2Cn%3A1057792%2Cp_85%3A2470955011&bbn=1057792&ie=UTF8&qid=1451751877&rnid=2470954011',

            # # Home & Kitchen : Bedding : Prime Eligible : Bedspreads, Coverlets & Sets
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063252%2Cp_85%3A2470955011%2Cn%3A10671038011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=10671038011&ie=UTF8&qid=1451751894&rnid=5016682011',

            # # Home & Kitchen : Kids' Home Store
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206325011%2Cp_85%3A2470955011&bbn=3206325011&ie=UTF8&qid=1451751958&rnid=2470954011',


            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Aheadphones%2Cp_85%3A2470955011&keywords=headphones&ie=UTF8&qid=1451354355&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A12097480011%2Ck%3Aheadphones%2Cp_85%3A2470955011&keywords=headphones&ie=UTF8&qid=1451354347&rnid=2941120011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2407777011%2Ck%3Aheadphones%2Cp_85%3A2470955011&keywords=headphones&ie=UTF8&qid=1451354399&rnid=2941120011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Akitchen+gadgets%2Cp_85%3A2470955011&keywords=kitchen+gadgets&ie=UTF8&qid=1451354468&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A284507%2Cn%3A289754%2Cn%3A289783%2Ck%3Akitchen+gadgets%2Cp_85%3A2470955011&keywords=kitchen+gadgets&ie=UTF8&qid=1451354475&rnid=1063498',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A15684181%2Cn%3A15706941%2Cn%3A387679011%2Ck%3Acar+charger%2Cp_85%3A2470955011&keywords=car+charger&ie=UTF8&qid=1451354575&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A15684181%2Cn%3A15706941%2Cn%3A387679011%2Cn%3A583328%2Ck%3Acar+charger%2Cp_85%3A2470955011&keywords=car+charger&ie=UTF8&qid=1451354593&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Awatch%2Cp_85%3A2470955011&keywords=watch&ie=UTF8&qid=1451354650&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Ascarfs%2Cp_85%3A2470955011&keywords=scarfs&ie=UTF8&qid=1451354709&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A165793011%2Ck%3Ascarfs%2Cp_85%3A2470955011&keywords=scarfs&ie=UTF8&qid=1451354750&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A165793011%2Cn%3A365427011%2Ck%3Ascarfs%2Cp_85%3A2470955011&keywords=scarfs&ie=UTF8&qid=1451354760&rnid=165795011',
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A15706831%2Ck%3Acar%2Cp_85%3A2470955011&keywords=car&ie=UTF8&qid=1451354843&rnid=2941120011',


            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A16310251%2Cn%3A387559011%2Cn%3A6524625011%2Ck%3Ahealthy+snacks%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=healthy+snacks&ie=UTF8&qid=1449276212&rnid=5016682011',
            # 'https://www.amazon.com/s/?rh=n%3A16310101%2Cn%3A16310251%2Cn%3A387559011%2Ck%3Ahealthy+snacks%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=387559011&keywords=healthy+snacks&ie=UTF8&qid=1449276209',
            # 'https://www.amazon.com/s/?ie=UTF8&node=5599475011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-3&pf_rd_r=JR0PTQ41TXMMTJ936YBP&pf_rd_t=101&pf_rd_p=2253012962&pf_rd_i=16310231',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2116310211%2Cn%3A16310231%2Cn%3A16318651%2Cn%3A5782442011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=5782442011&ie=UTF8&qid=1449276311&rnid=5016682011',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2116310211%2Cn%3A16310231%2Cn%3A16318171%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=16318171&ie=UTF8&qid=1449276361&rnid=5016682011',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Ayoga%2Cp_85%3A2470955011&keywords=yoga&ie=UTF8&qid=1449276385&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Amassage%2Cp_85%3A2470955011&keywords=massage&ie=UTF8&qid=1449276497&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acute+accessories%2Cp_85%3A2470955011&keywords=cute+accessories&ie=UTF8&qid=1449276542&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407756011%2Ck%3Acute+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=cute+accessories&ie=UTF8&qid=1449276549&rnid=5016682011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407779011%2Ck%3Acute+accessories%2Cp_85%3A2470955011&keywords=cute+accessories&ie=UTF8&qid=1449276590&rnid=2335753011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Aheadphone%2Cp_85%3A2470955011&keywords=headphone&ie=UTF8&qid=1449276644&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548951011%2Cn%3A3015405011%2Ck%3Aheadphone%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=headphone&ie=UTF8&qid=1449276652&rnid=5016682011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Abath+and+body+works%2Cp_85%3A2470955011&keywords=bath+and+body+works&ie=UTF8&qid=1449276680&rnid=2470954011',
            # 'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A11056291%2Ck%3Abath+and+body+works%2Cp_85%3A2470955011&keywords=bath+and+body+works&ie=UTF8&qid=1449276677&rnid=2941120011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Ck%3Abath+and+body+works%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bath+and+body+works&ie=UTF8&qid=1449276717&rnid=5016682011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11062211%2Ck%3Abath+and+body+works%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bath+and+body+works&ie=UTF8&qid=1449276721&rnid=11055981',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2112880941%2Cn%3A%21251285011%2Cn%3A6682399011%2Cn%3A6684055011%2Cn%3A6684056011%2Cp_85%3A2470955011&bbn=6684056011&ie=UTF8&qid=1449276796&rnid=2470954011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2112880941%2Cn%3A%21251285011%2Cn%3A6682399011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=6682399011&ie=UTF8&qid=1449276842&rnid=5016682011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2112880941%2Cn%3A%21251285011%2Cn%3A6682399011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A6684066011&bbn=6682399011&ie=UTF8&qid=1449276840&rnid=6682399011',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A%2112880941%2Cn%3A%21251285011%2Cn%3A6682399011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cn%3A6684066011%2Cn%3A6684071011&bbn=6684066011&ie=UTF8&qid=1449276854&rnid=6684066011',


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

            # 'https://www.amazon.com/s/?url=search-alias%3Dgrocery&field-keywords=food',
            # 'https://www.amazon.com/Breakfast-Foods-Grocery/b/?ie=UTF8&node=16310251',
            # 'https://www.amazon.com/b/?ie=UTF8&node=11139497011',
            # 'https://www.amazon.com/International-British-Asian-Foods/b/?ie=UTF8&node=376936011',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2151536011%2Cn%3A376936011%2Cn%3A16320321&bbn=376936011&ie=UTF8&qid=1448825253&rnid=16310211',
            # 'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A16310101%2Cn%3A%2151536011%2Cn%3A376936011%2Cn%3A16310231&bbn=376936011&ie=UTF8&qid=1448825253&rnid=16310211',
            # 'http://www.amazon.com/b/?node=2975268011&ie=UTF8&qid=1448825345',
            # 'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2619533011%2Cn%3A%212619534011%2Cn%3A2975241011%2Cn%3A2975268011%2Cn%3A2975271011&bbn=2975268011&ie=UTF8&qid=1448825351&rnid=2975268011',
            # 'http://www.amazon.com/b/?node=2975528011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=3048877011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975524011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975529011&ie=UTF8',
            # 'http://www.amazon.com/b/?node=2975539011&ie=UTF8',
        ])
    process.start()

