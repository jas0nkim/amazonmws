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
    #  Electronics : Computers & Accessories : Laptop Accessories : Batteries : Prime Eligible : Exclude Add-on : Dell or HP : "laptop battery"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_89_0?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A3011391011%2Cn%3A720576%2Ck%3Alaptop+battery%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_89%3ADell%7CHP&keywords=laptop+battery&ie=UTF8&qid=1472678826&rnid=2528832011',

    # Prime Eligible : "Diabetic Test Strips"
    # 'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3ADiabetic+Test+Strips%2Cp_85%3A2470955011&keywords=Diabetic+Test+Strips&ie=UTF8&qid=1472737439&rnid=2470954011',

    # Prime Eligible : "Electric Toothbrushes"
    # 'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3AElectric+Toothbrushes%2Cp_85%3A2470955011&keywords=Electric+Toothbrushes&ie=UTF8&qid=1472743909&rnid=2470954011',

    # Prime Eligible : "Dental Floss Flossers"
    # 'https://www.amazon.com/s/ref=sr_st_review-rank?keywords=Dental+Floss+Flossers&fst=as%3Aoff&rh=i%3Aaps%2Ck%3ADental+Floss+Flossers%2Cp_85%3A2470955011&qid=1472834272&sort=review-rank',

    # Prime Eligible : "Hair Removal Creams Sprays"
    # 'https://www.amazon.com/s/ref=sr_st_review-rank?keywords=Hair+Removal+Creams+Sprays&fst=as%3Aoff&rh=i%3Aaps%2Ck%3AHair+Removal+Creams+Sprays%2Cp_85%3A2470955011&qid=1472836266&sort=review-rank',

    # Prime Eligible : "Packing Shipping Labels Tags"
    # 'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3APacking+Shipping+Labels+Tags%2Cp_85%3A2470955011&keywords=Packing+Shipping+Labels+Tags&ie=UTF8&qid=1472841732&rnid=2470954011',

    # Electronics : Computers & Accessories : Computer Accessories & Peripherals : Memory Card Accessories : Memory Card Readers : Prime Eligible : "Memory Card USB Adapters"
    # 'https://www.amazon.com/s/ref=sr_pg_3?fst=as%3Aoff&rh=n%3A172282%2Cn%3A541966%2Cn%3A172456%2Cn%3A11548957011%2Cn%3A516872%2Ck%3AMemory+Card+USB+Adapters%2Cp_85%3A2470955011&page=3&keywords=Memory+Card+USB+Adapters&ie=UTF8&qid=1472843068&spIA=B01EJACUWC,B005IMFX2K,B00YFQ7M88,B009DI6BQ2,B01AP44RKE,B016CYV6AU',

    # Prime Eligible : "Halloween Decorations"
    # 'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3AHalloween+Decorations%2Cp_85%3A2470955011&keywords=Halloween+Decorations&ie=UTF8&qid=1472846257&rnid=2470954011',

    # Cell Phones & Accessories : Cases, Holsters & Clips : Cases : Prime Eligible : Exclude Add-on : "iphone 7 case"
    # 'https://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407760011%2Cn%3A3081461011%2Ck%3Aiphone+7+case%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&keywords=iphone+7+case&ie=UTF8&qid=1473641411&rnid=5016682011',

    # Prime Eligible : "bluetooth headphones"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Abluetooth+headphones%2Cp_85%3A2470955011&keywords=bluetooth+headphones&ie=UTF8&qid=1473641483&rnid=2470954011',

    # Cell Phones & Accessories : Cases, Holsters & Clips : Cases : Prime Eligible : Exclude Add-on : Cell Phone Compatibility: 4 selected : "iphone 7 plus case"  
    # 'https://www.amazon.com/s/ref=sr_nr_p_n_feature_nine_bro_2?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A2407760011%2Cn%3A3081461011%2Ck%3Aiphone+7+plus+case%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_n_feature_nine_browse-bin%3A15284134011%7C15284135011%7C10030582011%7C10030581011&keywords=iphone+7+plus+case&ie=UTF8&qid=1473682245&rnid=2488708011',

    # Toys & Games : Prime Eligible : Toys Age Range: 3 selected : New : Girls : Exclude Add-on : "halloween costumes for girls"  
    # 'https://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A165793011%2Ck%3Ahalloween+costumes+for+girls%2Cp_85%3A2470955011%2Cp_n_age_range%3A165813011%7C165890011%7C165936011%2Cp_n_condition-type%3A6461716011%2Cp_n_feature_four_browse-bin%3A3480744011%2Cp_n_is-min-purchase-required%3A5016683011&sort=relevanceblender&keywords=halloween+costumes+for+girls&ie=UTF8&qid=1474728488&rnid=5016682011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : Under $25 : "sweater dress"  
    # 'https://www.amazon.com/s/ref=sr_nr_pf_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Asweater+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1040660&keywords=sweater+dress&low-price=0&rnid=2661611011&high-price=25&ie=UTF8&qid=1474812425&ajr=0',

    # Clothing, Shoes & Jewelry : Women : Shoes : Boots : Prime Eligible : Exclude Add-on : $0-$40 : 4 Stars & Up : "ankle boots"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=k%3Aankle+boots%2Cn%3A7141123011%2Cn%3A7147440011%2Cn%3A679337011%2Cn%3A679380011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A-4000%2Cp_72%3A2661618011&bbn=679380011&keywords=ankle+boots&ie=UTF8&qid=1474836280&rnid=2661617011',

    # Prime Eligible : 3 Stars & Up : New : "costume for kids"
    # 'https://www.amazon.com/s/ref=sr_nr_p_n_condition-type_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Acostume+for+kids%2Cp_85%3A2470955011%2Cp_72%3A2661619011%2Cp_n_condition-type%3A6461716011&keywords=costume+for+kids&ie=UTF8&qid=1474925243&rnid=6461714011',

    #  Toys & Games : Games : Prime Eligible : Exclude Add-on : 3 Stars & Up : "pokemon cards"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A165793011%2Cn%3A166220011%2Ck%3Apokemon+cards%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A1248964011&keywords=pokemon+cards&ie=UTF8&qid=1475241125&rnid=1248961011',

    # Toys & Games : Holiday Toy List Birth to 24 months : Birth to 24 Months : 4 Stars & Up : Prime Eligible : Exclude Add-on
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A165793011%2Cn%3A%212334111011%2Cn%3A%212334173011%2Cn%3A15539863011%2Cp_n_age_range%3A165813011%2Cp_72%3A1248963011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=15539863011&ie=UTF8&qid=1477666630&rnid=5016682011',

    #  Clothing, Shoes & Jewelry : Women : Clothing : Fashion Hoodies & Sweatshirts : Prime Eligible : Exclude Add-on : "women sweaters"
    # 'https://www.amazon.com/s/ref=sr_ex_n_5?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1258603011%2Ck%3Awomen+sweaters%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1040660&keywords=women+sweaters&ie=UTF8&qid=1477674659',

    # Clothing, Shoes & Jewelry : Women : Accessories : Scarves & Wraps : Prime Eligible : Exclude Add-on : "women scarves"
    # 'https://www.amazon.com/s/ref=sr_nr_p_n_is-min-purchase-_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cn%3A7072324011%2Ck%3Awomen+scarves%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=7141123011&keywords=women+scarves&ie=UTF8&qid=1478179127&rnid=5016682011',

    # Clothing, Shoes & Jewelry : Women : Shoes : Boots : Prime Eligible : Exclude Add-on : $0-$75
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_5?rnid=2661611011&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A679337011%2Cn%3A679380011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&sort=review-rank&qid=1478344467&bbn=679380011&low-price=0&high-price=75&x=13&y=17'

    #  Clothing, Shoes & Jewelry : Women : Accessories : Sunglasses & Eyewear Accessories : Prime Eligible : Exclude Add-on : $0-$100
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cn%3A7072321011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&sort=review-rank&qid=1478347706&bbn=7072321011&low-price=0&high-price=100&x=11&y=12'

    # Clothing, Shoes & Jewelry : Women : Accessories : Belts : Prime Eligible : Exclude Add-on : $0-$75
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cn%3A2474940011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&sort=review-rank&qid=1478445395&bbn=2474940011&low-price=0&high-price=75&x=16&y=14',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : $0-$100 : "office"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_5?rnid=2661611011&keywords=office&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Aoffice%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&qid=1478445619&bbn=1040660&low-price=0&high-price=100&x=17&y=15',

    # Clothing, Shoes & Jewelry : Women : Accessories : Prime Eligible : Exclude Add-on : $0-$100 : "office"  
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=office&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Ck%3Aoffice%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A-7500&qid=1478488509&bbn=2474936011&low-price=0&high-price=100&x=14&y=6',

    # Clothing, Shoes & Jewelry : Women : Accessories : Scarves & Wraps : Prime Eligible : "office"
    'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cn%3A7072324011%2Ck%3Aoffice%2Cp_85%3A2470955011&bbn=7072324011&keywords=office&ie=UTF8&qid=1478533948&rnid=2470954011',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__max_amazon_price = None
__min_amazon_price = None
__max_page = 10

def main(argv):
    ebay_store_id = 1
    try:
        opts, args = getopt.getopt(argv, "he:", ["ebaystoreid=", ])
    except getopt.GetoptError:
        print 'keywordsearches.py -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'keywordsearches.py -e <1|2|3|4|...ebaystoreid>'
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
    max_amazon_price = __max_amazon_price
    min_amazon_price = __min_amazon_price
    max_page = __max_page

    # scrape amazon items (variations)
    if len(start_urls) > 0:
        scrapy_settings = get_project_settings()
        scrapy_settings.set('REFERER_ENABLED', False)
        process = CrawlerProcess(scrapy_settings)
        process.crawl('amazon_keyword_search',
            start_urls=start_urls,
            task_id=task_id,
            ebay_store_id=ebay_store_id,
            premium=premium,
            list_new=True,
            max_amazon_price=max_amazon_price,
            min_amazon_price=min_amazon_price,
            max_page=max_page)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True

def list_to_ebay(task_id, ebay_store_id):
    # list to ebay store
    ebay_store = EbayStoreModelManager.fetch_one(id=ebay_store_id)
    handler = ListingHandler(ebay_store)

    # get distinct parent_asin
    parent_asins = list(set([ t.parent_asin for t in amazonmws_utils.queryset_iterator(AmazonScrapeTaskModelManager.fetch(task_id=task_id, ebay_store_id=ebay_store_id)) ]))

    # find all amazon items (asin) have same parent_asin
    for p_asin in parent_asins:
        amazon_items = AmazonItemModelManager.fetch_its_variations(parent_asin=p_asin)
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=p_asin)
        succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
