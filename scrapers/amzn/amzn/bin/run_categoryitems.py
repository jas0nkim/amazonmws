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
            # Books : Reference : Foreign Language Study & Reference
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A283155%2Cn%3A21%2Cn%3A11773%2Cn%3A11811%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750399&rnid=5016682011',
            
            # Beauty : Makeup : Eyes : Eyeliner
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11058281%2Cn%3A11058331%2Cn%3A11058521%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750464&rnid=5016682011',
            
            # Beauty : Skin Care : Eyes : Masks & Pillows
            'https://www.amazon.com/s/fst=as%3Aoff&rh=n%3A7730093011%2Ck%3Akorean%2Cp_85%3A2470955011&keywords=korean&ie=UTF8&qid=1451750490&rnid=2941120011',
            
            # Beauty : Skin Care : Face : Treatments & Masks : Masks
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11060451%2Cn%3A11060711%2Cn%3A11062031%2Cn%3A11061121%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750512&rnid=5016682011',

            # Beauty : Makeup : Face : Foundation
            'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11058281%2Cn%3A11058691%2Cn%3A11058871%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750514&rnid=5016682011',

            # Beauty : Bath & Body Care : Hands, Feet & Nails : Hand Creams & Lotions
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11055991%2Cn%3A11062211%2Cn%3A11062261%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750565&rnid=5016682011',            

            # Home & Kitchen : Kitchen & Dining : Kitchen Utensils & Gadgets
            'https://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A284507%2Cn%3A289754%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750567&rnid=5016682011',

            # Home & Kitchen : Kitchen & Dining : Dining & Entertaining : Flatware
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A284507%2Cn%3A13162311%2Cn%3A13218891%2Cn%3A13220831%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750592&rnid=5016682011',

            # Home & Kitchen
            'https://www.amazon.com/s/?rh=n%3A1055398%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1055398&keywords=korean&ie=UTF8&qid=1451750596',

            # Home & Kitchen : Bedding : Blankets & Throws : Bed Blankets
            'https://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A3732181%2Ck%3Akorean%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=korean&ie=UTF8&qid=1451750608&rnid=1063498',

            # Electronics : Computers & Accessories
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011&keywords=computer+accessories&ie=UTF8&qid=1451750828&rnid=2470954011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Cables & Interconnects
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A172463%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750832&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750855&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Skins & Decals
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A3011392011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750888&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Lap Desks
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A3011392011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750888&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Chargers & Adapters
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A11041841%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750933&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Bags, Cases & Sleeves : Sleeves
            'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A172470%2Cn%3A335609011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750961&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Batteries
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A720576%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451750982&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Cooling Pads
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A2243862011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751023&rnid=5016682011',

            # Electronics : Computers & Accessories : Laptop Accessories : Docking Stations 
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A778660%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751028&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751057&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Keyboard & Mice Accessories : Wrist Rests
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A3012566011%2Cn%3A705324011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751095&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Monitor Accessories : Monitor Arms & Monitor Stands
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A281062%2Cn%3A490624011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751099&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Keyboard & Mice Accessories : Mouse Pads
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A3012566011%2Cn%3A705323011%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751120&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Keyboards, Mice & Accessories : Mice
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548956011%2Cn%3A11036491%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751153&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Audio & Video Accessories : Computer Speakers
            'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548951011%2Cn%3A172471%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751155&rnid=5016682011',

            # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Cleaning & Repair : Repair Kits
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A281501%2Cn%3A13825561%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751192&rnid=5016682011',

            # Electronics : Accessories & Supplies : Cord Management
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A172282%2Cn%3A281407%2Cn%3A11042051%2Ck%3Acomputer+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=computer+accessories&ie=UTF8&qid=1451751252&rnid=5016682011',

            'http://www.amazon.com/s/?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acar+accessories%2Cp_85%3A2470955011&keywords=car+accessories&ie=UTF8&qid=1451751278&rnid=2470954011',

            # Cell Phones & Accessories : Accessories
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751282&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Chargers & Power Adapters : Car Chargers 
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407761011%2Cn%3A2407770011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751323&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Mounts & Stands : Stands
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A7072563011%2Cn%3A7073961011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751333&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Car Accessories : Car Kits
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407759011%2Cn%3A2407764011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751370&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Accessory Kits
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407756011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751381&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Replacement Parts
            'http://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407780011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751410&rnid=5016682011',

            # Cell Phones & Accessories : Accessories : Replacement Parts
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407755011%2Cn%3A2407780011%2Ck%3Acar+accessories%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=car+accessories&ie=UTF8&qid=1451751410&rnid=5016682011',

            # Tools & Home Improvement : Light Bulbs : LED Bulbs
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A322525011%2Cn%3A2314207011%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751525&rnid=5016682011',

            # Tools & Home Improvement : Painting Supplies & Wall Treatments
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A228899%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751735&rnid=5016682011',

            # Tools & Home Improvement : Lighting & Ceiling Fans : Wall Lights : Night Lights
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A5486429011%2Cn%3A3736651%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751757&rnid=5016682011',

            # Tools & Home Improvement : Lighting & Ceiling Fans : Lamps & Shades : Table Lamps
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A3736561%2Cn%3A1063296%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751784&rnid=5016682011',

            # Tools & Home Improvement : Lighting & Ceiling Fans : Outdoor Lighting : String Lights
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A228013%2Cn%3A495224%2Cn%3A495236%2Cn%3A3742221%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751823&rnid=5016682011',

            # Home & Kitchen : Home Decor : Kids' Room Decor : Wall Decor
            'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A1063278%2Cn%3A404454011%2Cn%3A404458011%2Ck%3Abedroom+decor%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=bedroom+decor&ie=UTF8&qid=1451751829&rnid=5016682011',

            # Home & Kitchen : Bedding & Bath
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%2113900811%2Cn%3A%211063496%2Cn%3A%21251263011%2Cn%3A1057792%2Cp_85%3A2470955011&bbn=1057792&ie=UTF8&qid=1451751877&rnid=2470954011',

            # Home & Kitchen : Bedding : Prime Eligible : Bedspreads, Coverlets & Sets
            'http://www.amazon.com/gp/search/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A1063252%2Cp_85%3A2470955011%2Cn%3A10671038011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=10671038011&ie=UTF8&qid=1451751894&rnid=5016682011',

            # Home & Kitchen : Kids' Home Store
            'http://www.amazon.com/s/?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A%211063498%2Cn%3A3206325011%2Cp_85%3A2470955011&bbn=3206325011&ie=UTF8&qid=1451751958&rnid=2470954011',


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

