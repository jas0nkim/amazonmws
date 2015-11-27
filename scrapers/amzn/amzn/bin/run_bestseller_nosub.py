import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from amazonmws import utils as amazonmws_utils
from amazonmws.loggers import set_root_graylogger


if __name__ == "__main__":
    lock_filename = 'bestseller_scrapy.lock'
    amazonmws_utils.check_lock(lock_filename)
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    try:
        start_urls=[
            'http://www.amazon.com/gp/bestsellers/pc/541966/',
            'http://www.amazon.com/Best-Sellers-Electronics-Data-Storage/zgbs/electronics/1292110011/',
            'http://www.amazon.com/Best-Sellers-Electronics-Laptop-Accessories/zgbs/electronics/3011391011/',
            'http://www.amazon.com/Best-Sellers-Toys-Games-Dolls-Accessories/zgbs/toys-and-games/166118011/',

            # 'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/',
            # 'http://www.amazon.com/best-sellers-camera-photo/zgbs/photo/',
            # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Bags-Cases/zgbs/photo/172437/',
            # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Tripod-Monopod-Cases/zgbs/photo/3346131/',
            # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Telescope-Cases/zgbs/photo/3346091/',
            # 'http://www.amazon.com/Best-Sellers-Camera-Photo-Video-Projector-Cases/zgbs/photo/1205270/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Bath-Products/zgbs/home-garden/1063236/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Store/zgbs/home-garden/3206325011/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Baking-Supplies/zgbs/home-garden/2231407011/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bedding/zgbs/home-garden/1063268/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Nursery-Bedding/zgbs/home-garden/166742011/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Baby-Child-Products/zgbs/hpc/16025501/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Products/zgbs/hpc/3760941/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Alternative-Medicine-Products/zgbs/hpc/13052911/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Acupuncture-Products/zgbs/hpc/13052921/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Ayurveda-Products/zgbs/hpc/13052941/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Flower-Essences/zgbs/hpc/3767761/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Light-Therapy-Products/zgbs/hpc/13053141/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Manipulation-Therapy-Products/zgbs/hpc/13053161/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Oxygen-Therapy-Products/zgbs/hpc/13052971/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Single-Homeopathic-Remedies/zgbs/hpc/3767781/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Sound-Therapy-Products/zgbs/hpc/13052981/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Foot-Products/zgbs/hpc/3779911/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Moleskin/zgbs/hpc/3779981/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Foot-Odor-Control-Products/zgbs/hpc/3780131/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Wart-Removal-Products/zgbs/hpc/3780171/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Corn-Callus-Trimmers/zgbs/hpc/3779971/',
            # 'http://www.amazon.com/Best-Sellers-Health-Personal-Care-Diabetic-Foot/zgbs/hpc/3780001/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Furniture/zgbs/home-garden/1063306/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bath/zgbs/home-garden/3263108011/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Bath-Towels/zgbs/home-garden/3263111011/',
            # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Shower-Accessories/zgbs/home-garden/3265576011/',
            # 'http://www.amazon.com/Best-Sellers-Watches/zgbs/watches/',
            # 'http://www.amazon.com/gp/bestsellers/toys-and-games/',
            # 'http://www.amazon.com/Best-Sellers-Toys-Games-Toy-Figures-Playsets/zgbs/toys-and-games/165993011/',
            # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Toy-Figures/zgbs/toys-and-games/2514571011/',
            # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Figure-Vehicles-Playsets/zgbs/toys-and-games/7620514011/',
            # 'http://www.amazon.com/Best-Sellers-Toys-Games-Action-Figure-Vehicles/zgbs/toys-and-games/274293011/',
            # 'http://www.amazon.com/gp/bestsellers/pc/541966/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-External-Components/zgbs/electronics/3012292011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-External-Sound-Cards/zgbs/electronics/3015427011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-External-TV-Tuners/zgbs/electronics/3015428011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-Graphics-Card-Fans/zgbs/electronics/3015421011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-Water-Cooling-Systems/zgbs/electronics/3015422011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-Internal-Hard-Drive-Cooling-Fans/zgbs/electronics/3228286011/',
            # 'http://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/',
        ]

        process = CrawlerProcess(get_project_settings())
        process.crawl('amazon_bestseller', start_urls=start_urls)
        # process.crawl('amazon_bestseller_sub', start_urls=start_urls)
        process.start()
    finally:
        amazonmws_utils.release_lock(lock_filename)
