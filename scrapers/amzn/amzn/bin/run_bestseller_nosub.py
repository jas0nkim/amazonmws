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
        # # Office Electronics Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Office-Products/zgbs/electronics/172574',

        # # Security & Surveillance Equipment
        # 'http://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136',

        # # Outlet
        # 'http://www.amazon.com/Best-Sellers-Electronics-Outlet/zgbs/electronics/301793',

        # # Portable Audio & Video
        # 'http://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623',

        # # Televisions & Video Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011',

        # # Video Game Consoles & Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011',

        # # Electronics Accessories & Supplies
        # 'http://www.amazon.com/Best-Sellers-Electronics-Accessories-Supplies/zgbs/electronics/281407',

        # # Cell Phone Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011',

        # # Computer Accessories & Peripherals
        # 'http://www.amazon.com/Best-Sellers-Electronics-Computer-Accessories-Peripherals/zgbs/electronics/172456',

        # # Blank Media Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Blank-Media-Products/zgbs/electronics/281408',

        # # Electronics Cables
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cables/zgbs/electronics/12954861',

        # # Recording Microphones & Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Recording-Microphones-Accessories/zgbs/electronics/11974521',

        # # Electronics Power Protection Products
        # 'http://www.amazon.com/Best-Sellers-Electronics-Power-Protection-Products/zgbs/electronics/2223901011',

        # # Electrical Cord Management
        # 'http://www.amazon.com/Best-Sellers-Electronics-Electrical-Cord-Management/zgbs/electronics/11042051',

        # # School Adhesives
        # 'http://www.amazon.com/Best-Sellers-Office-Products-School-Adhesives/zgbs/office-products/1068992',

        # # Art Supplies & Craft Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Art-Supplies-Craft/zgbs/office-products/490778011',

        # # Filing Products
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Filing/zgbs/office-products/1069554',

        # # Math Materials
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Math-Materials/zgbs/office-products/12900191',

        # # Appliances
        # 'http://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances',

        # #####################

        # Beauty
        'http://www.amazon.com/Best-Sellers-Beauty/zgbs/beauty',

        # Bath & Body Care
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Body-Care/zgbs/beauty/11055991',

        # Bath Products
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Products/zgbs/beauty/11056211',

        # Bath Salts
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Salts/zgbs/beauty/11056251',

        # Bath Oils
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Oils/zgbs/beauty/11056261',

        # Bathing Accessories
        'http://www.amazon.com/Best-Sellers-Beauty-Bathing-Accessories/zgbs/beauty/11056491',

        # Bath & Body Brushes
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Body-Brushes/zgbs/beauty/11056501',

        # Bath Loofahs & Body Sponges
        'http://www.amazon.com/Best-Sellers-Beauty-Bath-Loofahs-Body-Sponges/zgbs/beauty/11056551',

        # Hair Drying Towels
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Drying-Towels/zgbs/beauty/3784491',

        # Body Cleansers
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Cleansers/zgbs/beauty/11056281',

        # Hair Removal Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Products/zgbs/beauty/3779051',

        # Hair Removal Tweezers
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Tweezers/zgbs/beauty/3779181',

        # Hair Removal Waxing Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Removal-Waxing-Products/zgbs/beauty/3779191',

        # Hands, Feet & Nail Care
        'http://www.amazon.com/Best-Sellers-Beauty-Hands-Feet-Nail-Care/zgbs/beauty/11062211',

        # Callus Shavers
        'http://www.amazon.com/Best-Sellers-Beauty-Callus-Shavers/zgbs/beauty/11063571',

        # Cuticle Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Cuticle-Care-Products/zgbs/beauty/11062221',

        # Hand Creams & Lotions
        'http://www.amazon.com/Best-Sellers-Beauty-Hand-Creams-Lotions/zgbs/beauty/11062261',

        # Hand Soaps
        'http://www.amazon.com/Best-Sellers-Beauty-Hand-Soaps/zgbs/beauty/11062271',

        # Nail Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Care-Products/zgbs/beauty/11062291',

        # Nail Growth Products
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Growth-Products/zgbs/beauty/11062311',

        # Nail Repair
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Repair/zgbs/beauty/11062321',

        # Nail Strengtheners
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Strengtheners/zgbs/beauty/11062331',

        # Lip Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Lip-Care-Products/zgbs/beauty/3761351',

        # Lip Balms & Moisturizers
        'http://www.amazon.com/Best-Sellers-Beauty-Lip-Balms-Moisturizers/zgbs/beauty/979546011',

        # Body Moisturizers
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Moisturizers/zgbs/beauty/11060661',

        # Body Butter
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Butter/zgbs/beauty/11060671',

        # Body Creams
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Creams/zgbs/beauty/11060681',

        # Body Lotions
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Lotions/zgbs/beauty/14024031',

        # Body Oils
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Oils/zgbs/beauty/11060691',

        # Body Scrubs & Treatments
        'http://www.amazon.com/Best-Sellers-Beauty-Body-Scrubs-Treatments/zgbs/beauty/11056421',

        # Perfumes & Fragrances
        'http://www.amazon.com/Best-Sellers-Beauty-Perfumes-Fragrances/zgbs/beauty/11056591',

        # Women's Fragrances
        'http://www.amazon.com/Best-Sellers-Beauty-Womens-Fragrances/zgbs/beauty/11056931',

        # Hair Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Care-Products/zgbs/beauty/11057241',

        # Hair Shampoo
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Shampoo/zgbs/beauty/11057651',

        # Hair Conditioner
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Conditioner/zgbs/beauty/11057251',

        # Hair Styling Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Styling-Products/zgbs/beauty/11057841',

        # Hair Coloring Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Coloring-Products/zgbs/beauty/11057451',

        # Hair & Scalp Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Scalp-Care-Products/zgbs/beauty/10666241011',

        # Hair & Scalp Treatments
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Scalp-Treatments/zgbs/beauty/11057431',

        # Hair Loss Products
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Loss-Products/zgbs/beauty/10898755011',

        # Hair Relaxers & Texturizers
        'http://www.amazon.com/Best-Sellers-Beauty-Hair-Relaxers-Texturizers/zgbs/beauty/10702858011',

        # Makeup
        'http://www.amazon.com/Best-Sellers-Beauty-Makeup/zgbs/beauty/11058281',

        # Eye Makeup
        'http://www.amazon.com/Best-Sellers-Beauty-Eye-Makeup/zgbs/beauty/11058331',

        # Face Makeup
        'http://www.amazon.com/Best-Sellers-Beauty-Face-Makeup/zgbs/beauty/11058691',

        # Lip Makeup
        'http://www.amazon.com/Best-Sellers-Beauty-Lip-Makeup/zgbs/beauty/11059031',

        # Makeup Remover
        'http://www.amazon.com/Best-Sellers-Beauty-Makeup-Remover/zgbs/beauty/11059231',

        # Nail Polish & Nail Decoration Products
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Polish-Decoration-Products/zgbs/beauty/11059311',

        # Nail Top & Base Coats
        'http://www.amazon.com/Best-Sellers-Beauty-Nail-Top-Base-Coats/zgbs/beauty/11059361',

        # Skin Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Skin-Care-Products/zgbs/beauty/11060451',

        # Eye Treatment Products
        'http://www.amazon.com/Best-Sellers-Beauty-Eye-Treatment-Products/zgbs/beauty/11061941',

        # Facial Skin Care Products
        'http://www.amazon.com/Best-Sellers-Beauty-Facial-Skin-Care-Products/zgbs/beauty/11060711',

        # Maternity Skin Care
        'http://www.amazon.com/Best-Sellers-Beauty-Maternity-Skin-Care/zgbs/beauty/11062371',

        # Beauty Tools & Accessories
        'http://www.amazon.com/Best-Sellers-Beauty-Tools-Accessories/zgbs/beauty/11062741',

        # Makeup Brushes & Tools
        'http://www.amazon.com/Best-Sellers-Beauty-Makeup-Brushes-Tools/zgbs/beauty/11059391',

        # Cotton Balls & Swabs
        'http://www.amazon.com/Best-Sellers-Beauty-Cotton-Balls-Swabs/zgbs/beauty/3784921',

        # #####################

        # # Office Products
        # 'http://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products',

        # # Education Supplies & Craft Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Education-Supplies-Craft/zgbs/office-products/12899801',

        # # Mail Supplies & Shipping Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-Mail-Supplies-Shipping/zgbs/office-products/1068972',

        # # Office & School Supplies
        # 'http://www.amazon.com/Best-Sellers-Office-Products-School-Supplies/zgbs/office-products/1069242',

        # #####################
        
        # # Coffee, Tea & Espresso
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Tea-Espresso/zgbs/home-garden/915194',

        # # Coffee & Tea
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Tea/zgbs/home-garden/7083296011',

        # # Coffee Beverages
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Coffee-Beverages/zgbs/home-garden/16318031',

        # # Tea Beverages
        # 'http://www.amazon.com/Best-Sellers-Home-Kitchen-Tea-Beverages/zgbs/home-garden/16318401',

        # # Dry Dog Food
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dry-Dog-Food/zgbs/pet-supplies/2975360011',

        # # Dog Treats
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Treats/zgbs/pet-supplies/2975434011',

        # # Dry Cat Food
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Dry-Cat-Food/zgbs/pet-supplies/2975266011',

        # # Cat Treats
        # 'http://www.amazon.com/Best-Sellers-Pet-Supplies-Cat-Treats/zgbs/pet-supplies/2975309011',

        # # Baby & Toddler Feeding Supplies
        # 'http://www.amazon.com/Best-Sellers-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011',

        # # Pregnancy & Maternity Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Pregnancy-Maternity-Products/zgbs/baby-products/166804011',

        # # Baby Gear
        # 'http://www.amazon.com/Best-Sellers-Baby-Gear/zgbs/baby-products/166828011',

        # # Baby Health & Care Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Health-Care-Products/zgbs/baby-products/166856011',

        # # Baby Safety Products
        # 'http://www.amazon.com/Best-Sellers-Baby-Safety-Products/zgbs/baby-products/166863011',

        # # Cell Phone Accessories
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011',

        # # Cell Phone Batteries & Battery Packs
        # 'http://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Batteries-Battery-Packs/zgbs/electronics/2407758011',

        # # Bluetooth Cell Phone Headsets
        # 'http://www.amazon.com/Best-Sellers-Electronics-Bluetooth-Cell-Phone-Headsets/zgbs/electronics/2407776011',

        # # Wired Cell Phone Headsets
        # 'http://www.amazon.com/Best-Sellers-Electronics-Wired-Cell-Phone-Headsets/zgbs/electronics/2407777011',

        # #####################

        # 'http://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games',
        # 'http://www.amazon.com/Best-Sellers-Music-CDs-Vinyl/zgbs/music/5174',
        # 'http://www.amazon.com/best-sellers-video-games/zgbs/videogames',
        # 'http://www.amazon.com/best-sellers-video-games/zgbs/books',

        # #####################

        # 'http://www.amazon.com/gp/bestsellers/pc/541966/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Data-Storage/zgbs/electronics/1292110011/',
        # 'http://www.amazon.com/Best-Sellers-Electronics-Laptop-Accessories/zgbs/electronics/3011391011/',
        # 'http://www.amazon.com/Best-Sellers-Toys-Games-Dolls-Accessories/zgbs/toys-and-games/166118011/',

        # #####################

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
        
        # 'http://www.amazon.com/gp/bestsellers/books/',
        # 'http://www.amazon.com/gp/bestsellers/wireless/',
    ]

    process = CrawlerProcess(get_project_settings())
    process.crawl('amazon_bestseller', start_urls=start_urls)
    # process.crawl('amazon_bestseller_sub', start_urls=start_urls)
    process.start()
