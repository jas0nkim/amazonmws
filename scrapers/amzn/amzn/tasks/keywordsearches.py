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
    'https://www.amazon.com/s/ref=sr_nr_pf_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Asweater+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&bbn=1040660&keywords=sweater+dress&low-price=0&rnid=2661611011&high-price=25&ie=UTF8&qid=1474812425&ajr=0',
]

__ebay_store_id = 1

__max_amazon_price = None
__min_amazon_price = None


def main(argv):
    is_premium = False
    try:
        opts, args = getopt.getopt(argv, "hs:", ["service=", ])
    except getopt.GetoptError:
        print 'keywordsearches.py -s <basic|premium>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'keywordsearches.py -s <basic|premium>'
            sys.exit()
        elif opt in ("-s", "--service") and arg == 'premium':
            is_premium = True
    run(premium=is_premium)


def run(premium):

    task_id = uuid.uuid4()
    ebay_store_id = __ebay_store_id

    if scrape_amazon(premium=premium, task_id=task_id, ebay_store_id=ebay_store_id):
        list_to_ebay(task_id=task_id, ebay_store_id=ebay_store_id)

def scrape_amazon(premium, task_id, ebay_store_id):
    # configure_logging(install_root_handler=False)
    # set_root_graylogger()

    start_urls = __start_urls
    max_amazon_price = __max_amazon_price
    min_amazon_price = __min_amazon_price

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
            max_amazon_price=max_amazon_price,
            min_amazon_price=min_amazon_price)
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
        amazon_items = AmazonItemModelManager.fetch(parent_asin=p_asin)
        ebay_item = EbayItemModelManager.fetch_one(ebay_store_id=ebay_store_id, asin=p_asin)
        succeed, maxed_out = handler.run_each(amazon_items=amazon_items, ebay_item=ebay_item)
        if maxed_out:
            logger.info("[%s] STOP LISTING - REACHED EBAY ITEM LIST LIMITATION" % ebay_store.username)
            break


if __name__ == "__main__":
    main(sys.argv[1:])
