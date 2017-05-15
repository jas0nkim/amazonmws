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
    # 'https://www.amazon.com/s/ref=sr_nr_p_85_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cn%3A7072324011%2Ck%3Aoffice%2Cp_85%3A2470955011&bbn=7072324011&keywords=office&ie=UTF8&qid=1478533948&rnid=2470954011',

    #  Clothing, Shoes & Jewelry : Women : Handbags & Wallets : Prime Eligible : Exclude Add-on : $0-$100 : "office"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&keywords=office&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A15743631%2Ck%3Aoffice%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&qid=1478554246&bbn=15743631&low-price=0&high-price=100&x=12&y=3',

    # Clothing, Shoes & Jewelry : Men : Shoes : Prime Eligible : Exclude Add-on : $0-$75 : "winter"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&keywords=winter&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A679255011%2Ck%3Awinter%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&qid=1478615150&bbn=679255011&low-price=0&high-price=75&x=13&y=7',

    #  Clothing, Shoes & Jewelry : Men : Shoes : Slippers : Exclude Add-on : Prime Eligible : "weather"
    # 'https://www.amazon.com/s/ref=sr_ex_n_24?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679324011%2Ck%3Aweather%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_85%3A2470955011&bbn=679255011&keywords=weather&ie=UTF8&qid=1478629425',

    # Clothing, Shoes & Jewelry : Men : Shoes : Fashion Sneakers : Prime Eligible : Exclude Add-on : $0-$75 : "winter"
    # 'https://www.amazon.com/s/ref=sr_ex_n_8?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679312011%2Ck%3Awinter%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A-7500&bbn=679255011&keywords=winter&ie=UTF8&qid=1478616083',

    # Clothing, Shoes & Jewelry : Cashmere Classics : Amazon.com : Prime Eligible : Exclude Add-on : $0-100
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_4?rnid=2661611011&lo=fashion&rh=n%3A7141123011%2Cn%3A15245710011%2Cp_6%3AATVPDKIKX0DER%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011&sort=date-desc-rank&qid=1478684630&bbn=15245710011&low-price=0&high-price=100&x=6&y=12',

    # Clothing, Shoes & Jewelry : Women : Accessories : Prime Eligible : Exclude Add-on : $0-$50
    # 'https://www.amazon.com/s/ref=sr_st_featured-rank?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A2474936011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A-5000&qid=1478685120&bbn=7147440011&sort=featured-rank',

    # Clothing, Shoes & Jewelry : Men : Accessories : Neckties : Exclude Add-on : Prime Eligible : 4 Stars & Up : $0-$50
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_4?rnid=2661611011&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A2474937011%2Cn%3A2474955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_85%3A2470955011%2Cp_72%3A2661618011&qid=1480965735&bbn=2474955011&low-price=0&high-price=50&x=10&y=13',

    # Clothing, Shoes & Jewelry : Women : Handbags & Wallets : Prime Eligible : 4 Stars & Up : Exclude Add-on : $0-$250 : 10% Off or More : "handbags for women"
    # 'https://www.amazon.com/s/ref=sr_nr_p_8_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A15743631%2Ck%3Ahandbags+for+women%2Cp_85%3A2470955011%2Cp_72%3A2661618011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A-25000%2Cp_8%3A2661604011&bbn=15743631&sort=featured-rank&keywords=handbags+for+women&ie=UTF8&qid=1484233799&rnid=2661603011',

    # Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$50 : "evening party dress"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&keywords=evening+party+dress&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Aevening+party+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484327478&bbn=7147440011&low-price=0&high-price=50&x=10&y=11',

    #  Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$50 : "evening party cocktail"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_5?rnid=2661611011&keywords=evening+party+cocktail&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Aevening+party+cocktail%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484333316&bbn=7147440011&low-price=0&high-price=50&x=11&y=8',

    #  Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$100 : "long sleeve tops"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=long+sleeve+tops&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Along+sleeve+tops%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Cp_36%3A-5000&qid=1484600515&bbn=7147440011&low-price=&high-price=100&x=10&y=9',

    # Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$50 : "underwear babydoll sleepwear"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_4?rnid=2661611011&keywords=underwear+babydoll+sleepwear&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Aunderwear+babydoll+sleepwear%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484654663&bbn=7147440011&low-price=&high-price=50&x=11&y=15',

    #  Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : "lingerie lace dress"
    # 'https://www.amazon.com/s/ref=sr_ex_p_36_0?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Alingerie+lace+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=1040660&keywords=lingerie+lace+dress&ie=UTF8&qid=1484664321',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : "lularoe leggings"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Alularoe+leggings%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=1040660&keywords=lularoe+leggings&ie=UTF8&qid=1484669817&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Handbags & Wallets : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$100 : "handbag shoulder tote messenger"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=handbag+shoulder+tote+messenger&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A15743631%2Ck%3Ahandbag+shoulder+tote+messenger%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Cp_36%3A-5000&qid=1484677347&bbn=15743631&low-price=&high-price=100&x=16&y=12',

    # Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$50 : "sexy women swimwear bikini"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&keywords=sexy+women+swimwear+bikini&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Asexy+women+swimwear+bikini%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484753305&bbn=7147440011&low-price=&high-price=50&x=13&y=13',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$150 : "evening party dress"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_36_5?rnid=2661611011&keywords=evening+party+dress&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Aevening+party+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484843721&bbn=1040660&low-price=&high-price=150&x=12&y=7',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$150 : "cocktail short mini dress"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_5?rnid=2661611011&keywords=cocktail+short+mini+dress&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Acocktail+short+mini+dress%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&qid=1484847703&bbn=1040660&low-price=&high-price=150&x=8&y=13',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : "spring multicolored leggings"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Aspring+multicolored+leggings%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=1040660&keywords=spring+multicolored+leggings&ie=UTF8&qid=1489166734&rnid=2661617011',

    #  Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : "swimsuit swimwear bathing monokini" 
    # 'https://www.amazon.com/s/ref=sr_ex_n_2?rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Ck%3Aswimsuit+swimwear+bathing+monokini&bbn=7147440011&keywords=swimsuit+swimwear+bathing+monokini&ie=UTF8&qid=1489167325',

    # Clothing, Shoes & Jewelry : Women : Clothing : Leggings : Prime Eligible : Exclude Add-on : 3 Stars & Up : "spring collection"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1258967011%2Ck%3Aspring+collection%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=1258967011&keywords=spring+collection&ie=UTF8&qid=1490580711&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Prime Eligible : Exclude Add-on : 3 Stars & Up : "strapless backless self-adhesive gel"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Ck%3Astrapless+backless+self-adhesive+gel%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=7147440011&keywords=strapless+backless+self-adhesive+gel&ie=UTF8&qid=1490581958&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Swimsuits & Cover Ups : Prime Eligible : Exclude Add-on : 3 Stars & Up : "push up padded"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1046622%2Ck%3Apush+up+padded%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=1046622&keywords=push+up+padded&ie=UTF8&qid=1490616221&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Swimsuits & Cover Ups : Prime Eligible : Exclude Add-on : 3 Stars & Up : "bandage bikini set"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1046622%2Ck%3Abandage+bikini+set%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=1046622&keywords=bandage+bikini+set&ie=UTF8&qid=1490647951&rnid=2661617011',

    # Beauty & Personal Care : Hair Care : Hair Accessories : Headbands : Prime Eligible : Exclude Add-on : 4 Stars & Up : "dress headpiece"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A3760911%2Cn%3A11057241%2Cn%3A11057971%2Cn%3A11058051%2Ck%3Adress+headpiece%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A1248873011&keywords=dress+headpiece&ie=UTF8&qid=1490745824&rnid=1248871011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 3 Stars & Up : "neoprene body shaper"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Aneoprene+body+shaper%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=1040660&keywords=neoprene+body+shaper&ie=UTF8&qid=1491443959&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$30 : "blouse shirt tops"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=blouse+shirt+tops&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Ablouse+shirt+tops%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Cp_36%3A-4000&qid=1491447873&bbn=1040660&low-price=&high-price=30&x=16&y=14',

    # Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$100 : "dress cocktail party" - Apr 6 2017
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=dress+cocktail+party&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Adress+cocktail+party%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Cp_36%3A-7500&qid=1491480058&bbn=1040660&low-price=&high-price=100&x=11&y=13',

    #  Clothing, Shoes & Jewelry : Men : Clothing : Prime Eligible : Exclude Add-on : 4 Stars & Up : "casual slim fit"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Ck%3Acasual+slim+fit%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=1040658&keywords=casual+slim+fit&ie=UTF8&qid=1491846501&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Men : Accessories : Wallets, Card Cases & Money Organizers : Wallets : Prime Eligible : Exclude Add-on : 4 Stars & Up : "credit card holder"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_72_0?fst=p90x%3A1%2Cas%3Aoff&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A2474937011%2Cn%3A7072333011%2Cn%3A2475895011%2Ck%3Acredit+card+holder%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=2475895011&keywords=credit+card+holder&ie=UTF8&qid=1491941318&rnid=2661617011',

    #  Clothing, Shoes & Jewelry : Men : Shoes : Prime Eligible : Exclude Add-on : 4 Stars & Up : $0-$100 : "running shoes"
    # 'https://www.amazon.com/s/ref=sr_nr_p_36_0?rnid=2661611011&keywords=running+shoes&fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A679255011%2Ck%3Arunning+shoes%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011%2Cp_36%3A-5000&qid=1491952297&bbn=7141123011&low-price=&high-price=100&x=7&y=10',

    #  Clothing, Shoes & Jewelry : Women : Clothing : Prime Eligible : Exclude Add-on : Under $25 : 4 Stars & Up : "casual tops t-shirt"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Ck%3Acasual+tops+t-shirt%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A2661612011%2Cp_72%3A2661618011&bbn=1040660&keywords=casual+tops+t-shirt&ie=UTF8&qid=1492036219&rnid=2661617011',

    #  Clothing, Shoes & Jewelry : Prime Eligible : Exclude Add-on : 4 Stars & Up : "ray ban sunglasses"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=p90x%3A1%2Cas%3Aoff&rh=n%3A7141123011%2Ck%3Aray+ban+sunglasses%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661618011&bbn=7141123011&keywords=ray+ban+sunglasses&ie=UTF8&qid=1492036514&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Prime Eligible : Exclude Add-on : $50 to $100 : 4 Stars & Up : "ray ban sunglasses"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=p90x%3A1%2Cas%3Aoff&rh=n%3A7141123011%2Ck%3Aray+ban+sunglasses%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A2661614011%2Cp_72%3A2661618011&bbn=7141123011&keywords=ray+ban+sunglasses&ie=UTF8&qid=1492108795&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Leggings : Prime Eligible : Exclude Add-on : "lularoe leggings" 
    # 'https://www.amazon.com/gp/search/ref=sr_ex_n_3?fst=p90x%3A1&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1258967011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Ck%3Alularoe+leggings&bbn=1040660&keywords=lularoe+leggings&ie=UTF8&qid=1492278563',

    # Clothing, Shoes & Jewelry : Women : Clothing : Dresses : Prime Eligible : Exclude Add-on : Under $25 : 4 Stars & Up : "dress cocktail party"
    # 'https://www.amazon.com/gp/search/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Ck%3Adress+cocktail+party%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A2661612011%2Cp_72%3A2661618011&bbn=1045024&keywords=dress+cocktail+party&ie=UTF8&qid=1492354389&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Tops & Tees : Prime Eligible : Exclude Add-on : Under $25 : 4 Stars & Up : "fashion women summer"
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_0?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Ck%3Afashion+women+summer%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_36%3A2661612011%2Cp_72%3A2661618011&bbn=2368343011&keywords=fashion+women+summer&ie=UTF8&qid=1493235783&rnid=2661617011',

    # Clothing, Shoes & Jewelry : Women : Clothing : Lingerie, Sleep & Lounge : Lingerie : Accessories : Adhesive Bras : Prime Eligible : Exclude Add-on : 3 Stars & Up
    # 'https://www.amazon.com/s/ref=sr_nr_p_72_1?fst=as%3Aoff&rh=n%3A7141123011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A9522931011%2Cn%3A14333511%2Cn%3A2364767011%2Cn%3A2364768011%2Cp_85%3A2470955011%2Cp_n_is-min-purchase-required%3A5016683011%2Cp_72%3A2661619011&bbn=2364768011&ie=UTF8&qid=1493286873&rnid=2661617011',

    # mother's day special
    'https://www.amazon.com/b/ref=gbpg_ftr_m-7_c8ab_category_Wallets?ie=UTF8&node=16183817011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-7&pf_rd_r=AJFSDFEHSBB355ZBYNMX&pf_rd_t=101&pf_rd_p=514cb08d-a5f6-48fd-80f0-e556844cc8ab&pf_rd_i=16183817011&gb_f_mothersday17-style=dealTypes:EVENT_DEAL,category:Dresses%252CPurses%252CShoes%252CSunglasses%252CWallets',
]

__premium_ebay_store_ids = [1, 5, 6, 7]
__max_amazon_price = None
__min_amazon_price = None
__max_page = 20

def main(argv):
    ebay_store_id = 1
    force_crawl = False
    try:
        opts, args = getopt.getopt(argv, "hfe:", ["ebaystoreid=", "forcecrawl" ])
    except getopt.GetoptError:
        print 'keywordsearches.py [-f] -e <1|2|3|4|...ebaystoreid>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'keywordsearches.py [-f] -e <1|2|3|4|...ebaystoreid>'
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
            max_page=max_page,
            force_crawl=force_crawl,
            dont_list_ebay=True)
        process.start()
    else:
        logger.error('No amazon items found')
        return False

    return True


if __name__ == "__main__":
    main(sys.argv[1:])
