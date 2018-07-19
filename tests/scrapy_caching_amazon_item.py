import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

os.environ['DJANGO_SETTINGS_MODULE'] = 'rfi.settings'

import django
django.setup()

###################################

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.model_managers import *


_item = {'_cached': False,
 '_redirected_asins': {},
 'asin': u'B00ANGZE20',
 'avg_rating': 4.5,
 'brand_name': u'Maidenform',
 'category': u'Clothing, Shoes & Jewelry : Women : Clothing : Lingerie, Sleep & Lounge : Lingerie : Panties : Boy Shorts',
 'description': u'<div id="productDescription" class="a-section a-spacing-small">\n        \n\n\n\n\n\n  \n    \n  \n\n\n        \n        \n     \n\t       \n     \n\n     \n                              \n     \n       \t       \n        \n        <!-- show up to 2 reviews by default --> \n        \n        \t\n        \t\n        \t\t\n        \t\t\t<p>These microfiber panties are so silky soft, you might think you are in a dream. Features a stretch fit that moves with you.\n\t\t\t\t    \t\n\t\t\t\t\t</p>\n        \t\t\n        \t\t\n        \t\n        \n        \t\n        \t\n        \t\t\n        \t\t\t<p>These microfiber panties are so silky soft, you might think you are in a dream. Features a stretch fit that moves with you.\n\t\t\t\t    \t\n\t\t\t\t\t</p>\n        \t\t\n        \t\t\n        \t\n        \n                \n        \n        \n      \n      \n    \n    </div>',
 'features': u'<div id="feature-bullets" class="a-section a-spacing-medium a-spacing-top-small"><ul class="a-vertical a-spacing-none"><li><span class="a-list-item"> \n\t\t\t\t\t\t\tBody: 80% Polyamide/20% Elastane\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\tImported\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\tHand Wash\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\t1" high\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\t8" wide\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\tLuxuriously soft and sheen fabric caresses the body\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item"> \n\t\t\t\t\t\t\tHidden features that smooth and support\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t</span></li><li><span class="a-list-item">Rear definition and lift</span></li><li><span class="a-list-item">Wide waist band for ultimate comfort</span></li></ul></div>',
 'has_sizechart': True,
 'is_addon': False,
 'is_fba': False,
 'is_pantry': False,
 'market_price': 0.0,
 'merchant_id': None,
 'merchant_name': None,
 'meta_description': u'Buy Maidenform Womens Dream Boyshort Panty, On The Prowl, 7 and other Boy Shorts at Amazon.com. Our wide selection is elegible for free shipping and free returns.',
 'meta_keywords': u"Maidenform Womens Dream Boyshort Panty, On The Prowl, 7,Maidenform Women's IA - Panties,40774,calvin klein panties,calvin klein underwear women,calvin klein underwear women set,calvin klein underwear women thong,ck underwear women,ex officio women's underwear,felina panties,jockey underwear for women,natori panties,pink victoria secret panties,spanx panties,tommy hilfiger underwear women,vanity fair panties,victoria secret panties,victoria secret panties for women,victorias secret panties,victoria's secret panties,victoria's secret underwear women,b.tempt'd,b.tempt'd boyshort,b.tempt'd cheeky,b.tempt'd hipster,b.tempt'd lace panty,b.tempt'd panty,b.tempt'd senuous panty,b.tempt'd sexy panties,b.tempt'd tanga,b.tempt'd tanga panty,b.tempt'd thong,be tempted,be tempted boyshort,be tempted cheeky,be tempted hipster,be tempted lace panty,be tempted panty,be tempted senuous panty,be tempted sexy panties,be tempted tanga,be tempted tanga panty,be tempted thong,betsey johnson,betsey johnson boyshort,betsey johnson cheeky,betsey johnson hipster,betsey johnson lace panty,betsey johnson panty,betsey johnson senuous panty,betsey johnson sexy panties,betsey johnson tanga,betsey johnson tanga panty,betsey johnson thong,jezebel,jezebel boyshort,jezebel cheeky,jezebel hipster,jezebel lace panty,jezebel panty,jezebel senuous panty,jezebel sexy panties,jezebel tanga,jezebel tanga panty,jezebel thong,lily of france,lily of france boyshort,lily of france cheeky,lily of france hipster,lily of france lace panty,lily of france panty,lily of france senuous panty,lily of france sexy panties,lily of france tanga,lily of france tanga panty,lily of france thong,lily of france,natori,natori boyshort,natori cheeky,natori hipster,natori lace panty,natori panty,natori senuous panty,natori sexy panties,natori tanga,natori tanga panty,natori thong,vasserette,vasserette boyshort,vasserette cheeky,vasserette hipster,vasserette lace panty,vasserette panty,vasserette senuous panty,vasserette sexy panties,vasserette tanga,vasserette tanga panty,vasserette thong,warners,warners boyshort,warners cheeky,warners hipster,warners lace panty,warners panty,warners senuous panty,warners sexy panties,warners tanga,warners tanga panty,warners thong,sexy panties,sexy lace panties,sexy panty,sexy thong panty,underwear women,calvin klein underwear women,vibrating panties,crotchless panties,panties for women,jockey underwear for women,sexy panties,women's underwear,womens panties,period panties,sexy underwear for women,vanity fair panties,cotton underwear women,plus size panties,seamless panties,boy shorts underwear for women,satin panties,sissy panties,ladies underwear panties,panties for women pack,women panties,lace panties,vibrant panties,cotton panties,padded panties,plus size underwear for women,cheeky panties,boyshort panties,incontinence underwear for women,mens panties,underwear for women,crotchless panties for sex,sexy panties for women,underwear women cotton,warners panties,victoria secret panties,sheer panties,women's panties,victoria's secret panties,silk panties,girls panties,panties for men,thong panties,hipster panties,thinx period panties,just my size panties,g string3 underwear women,maternity panties,nylon panties,wacoal panties,bikini panties,open crotch panties,thermal underwear women,ladies panties,underwear women sexy,string bikini panties,hanes underwear women,tummy control panties,panties plus size,plus size crotchless panties,slim panties 360,lace panties for women,high waist panties,cotton panties women,funny underwear for women,panties for girls,toddler panties,vibrator panties,camel toe panties,ck underwear women,ranger panties,cute panties,100 cotton underwear women,sissy pouch panties,sexy panties for women for sex,see through panties,olga panties for women,gaff panties,bras and panties sets,bikini underwear women,pink panties,ex officio women's underwear,bride panties,crotchless panties plus size,padded underwear for women,black underwear women,lace underwear women,calvin klein panties,women's underwear cotton,womans panties,black panties,woman panties,edible panties,plus size sexy panties,barely there panties,pearl panties,tanga panties,lingerie panties,funny panties,remote control panties,satin panties for women,silk panties for women,panties pack,ruffle panties,cotton bikini panties,cute underwear for women,victoria's secret underwear women,high waisted panties for women,calvin klein underwear women set,no show underwear women,dkny underwear women,tommy hilfiger underwear women,bikini panties for women,sexy underwear for women for sex,victorias secret panties,plus size panties for women,moisture wicking underwear women,used panties,granny panties,workout underwear for women,vassarette panties,disposable panties,underwear womens,long underwear women,mesh panties,laser cut panties,underwear womens sexy,maternity underwear panties,microfiber panties,hanes bikini underwear women,dildo panties,lace boyshort panties,boyshort panties for women,organic cotton underwear women,open back panties,floral panties,cat panties,underwear women plus size,seamless underwear women,new you underwear for women,plus size underwear for women sexy,panties for women pack sexy,silk underwear women,post partum underwear for women,high waisted underwear for women,sissy panties for men,no show panties,white panties,male panties,compression underwear women,bridal underwear for women,plus size boy shorts panties,underwear women pack,backless panties,cotton panties for women pack,womens panties plus size,plus size lace panties,spanx panties,womens cotton panties,control top panties,natori panties,warners panties no muffin top,felina panties,victoria secret panties for women,latex panties,shaping panties,striped panties,menstrual panties,pink victoria secret panties,vibrating panties with remote,ladies underwear panties cotton,olga panties,spandex panties,running underwear women,women's underwear pack,man panties,hi cut panties for women,string bikini underwear women,womens panties pack,no line panties,hanes underwear for women,girl panties,black lace panties,remote control vibrating panties,men's panties,slim panties,disposable underwear women,red panties,dog panties,toddler girl panties,calvin klein underwear women thong,ethika underwear for women,girdle panties,sexy underwear women,postpartum underwear for women,self expressions,self expressions boyshort,self expressions cheeky,self expressions hipster,self expressions lace panty,self expressions panty,self expressions senuous panty,self expressions sexy panties,self expressions tanga,self expressions tanga panty,self expressions thong,shades,nude,complexion,makeup,prom dresses,dresses for women party,maxi dresses for women,womens dresses,plus size dresses,summer dresses for women,jewelry for women,bridesmaid dresses,mother of the bride dresses,heels,white dresses for women,formal dresses for women,prom dress,sexy dresses for women,women dresses,girls dresses,vintage dresses,dresses for women,skirts for women,party dresses for women,casual dresses for women,black dresses for women,high heels,sundresses for women,club dresses,prom dresses long,wedding dresses,dresses,black heels,summer dresses,summer dresses,dresses for juniors,dresses for girls,jewelry,promise rings for her,prom dresses 2017 long,skirts,summer dress,long prom dresses,short prom dresses,plus size prom dresses,club dresses sexy,womens summer dresses,long skirts for women,two piece prom dress,maxi skirts for women,promise rings,mermaid prom dress,prom dresses short,prom,plus size summer dresses,womens skirts,prom shoes,skirts for women knee length,summer dresses for juniors,sexy club dresses,black prom dress,maxi skirts,bed skirts queen size,african skirts for women,long skirts,women skirts,promise rings for couples,plus size skirts,plus size club dresses,women summer dresses,promise ring,promise rings for him,pencil skirts for women,club dresses for women,bed skirts,club wear,skirts for women long length,strapless dress,long summer dresses for women,high waisted skirts,sexy club dresses for women,sexy summer dresses for women,jean skirts for women,summer dresses for women plus size,skirts for juniors,bed skirts king size,pencil skirts,black skirts for women,white summer dress,girls summer dresses,prometheus,women's summer dresses,poodle skirts for girls,summer dress for women,casual summer dresses for women,tennis skirts for women,bed skirts full size,club wear women sexy,white summer dresses for women,300 writing prompts,skirts for girls,summer dresses for girls,plus size summer dresses for women,summer dresses for women on sale,women club dresses,womens club dresses,strapless dresses for women,dress for women casual summer dresses,cute summer dresses,short summer dresses for women,plus size club dresses sexy,womens club wear,white club dresses sexy,sexy club wear for women,plus size club wear for women,club dresses plus size,summer dresses for teens,club wear for women,strapless dresses,white strapless dress,black club dresses for women,bodycon club dresses,black strapless dress,nightclub dresses,white club dresses for women,black club dresses,white club dresses,short sets women club wear,strapless dresses for juniors,club wear plus size,red strapless dress,plus size strapless dress,club wear women sexy jumpsuit,plus size club wear",
 'meta_title': u'Maidenform Womens Dream Boyshort Panty, On The Prowl, 7 at Amazon Women\u2019s Clothing store: Boy Shorts Panties',
 'parent_asin': 'B00ANGZ5MO',
 'price': 0.0,
 'quantity': 1000,
 'review_count': 580,
 'specifications': None,
 'status': True,
 'title': u'Maidenform Womens Dream Boyshort Panty',
 'url': u'https://www.amazon.com/dp/B00ANGZE20/?th=1&psc=1',
 'variation_asins': [u'B003BNZ3DW',
                     u'B00ANGZCYU',
                     u'B06ZZ738N9',
                     u'B071Y7PCZ2',
                     u'B071D8WNHW',
                     u'B071XPJQBB',
                     u'B06ZY2NFNH',
                     u'B0746NDCCB',
                     u'B00D05JXNW',
                     u'B00D05JYBI',
                     u'B006U6D6MC',
                     u'B06ZZHM3C6',
                     u'B071Y83M34',
                     u'B00D05JWRY',
                     u'B007MWG2QU',
                     u'B07FD3YT46',
                     u'B071XPJMFQ',
                     u'B07FD3YT45',
                     u'B01LZXJ4QH',
                     u'B06ZZHM47Z',
                     u'B077HM6FYD',
                     u'B07FDDY6XC',
                     u'B071CQ79TN',
                     u'B077HWX548',
                     u'B07BPD5H2K',
                     u'B07C92GCMG',
                     u'B077HV6GPV',
                     u'B0746NVFZM',
                     u'B07FD2PKBY',
                     u'B01M097N18',
                     u'B0777W6LVB',
                     u'B06ZZ73DNQ',
                     u'B00QA5EEDI',
                     u'B07FD3ZWMY',
                     u'B00S2GENZC',
                     u'B077HRVHYM',
                     u'B0777W6LVR',
                     u'B006U6D5EG',
                     u'B004NRBXNO',
                     u'B003BNZ3GE',
                     u'B004L9Q6KE',
                     u'B071CQ79SR',
                     u'B07FD7Y8NQ',
                     u'B077HP1TC9',
                     u'B07BPBKSBC',
                     u'B00ANGZE20',
                     u'B07FDF43QC',
                     u'B071Y7L4R2',
                     u'B06ZYC61MY',
                     u'B003BNZ3FK',
                     u'B06ZZRLRS1',
                     u'B00D05JW6U',
                     u'B003BNZ3FA',
                     u'B003H82XM0',
                     u'B01M1J5IGQ',
                     u'B0746NMG4K',
                     u'B07FD3QF8S',
                     u'B003BNZ3EQ',
                     u'B07FKMK41F',
                     u'B003BNZ3EG',
                     u'B01LXZ8D4R',
                     u'B003BNZ3F0',
                     u'B07FKFKQN1',
                     u'B077HYLPXB',
                     u'B077HTCZVS',
                     u'B00S2GEMTO',
                     u'B06ZYC6354',
                     u'B07FD9M68B',
                     u'B006U6D5PA',
                     u'B077HPV7T1',
                     u'B00I8OHIKK',
                     u'B07CHZQ726',
                     u'B06ZZS4R15',
                     u'B00S2GEPFK',
                     u'B077HWWMZZ',
                     u'B077HZNGBZ',
                     u'B004NR9TE4',
                     u'B00DN5VQJS',
                     u'B06ZYMQZVN',
                     u'B073F8F7J3',
                     u'B004L9TN5O',
                     u'B06ZYMQXNN',
                     u'B077HTRVMG',
                     u'B077HR7F4S',
                     u'B01LYMNQ1M',
                     u'B06ZYXL83K',
                     u'B07FKK3K6H',
                     u'B01BMWOFOQ',
                     u'B0777XLY43',
                     u'B003BNZ3HI',
                     u'B004O5G1VY',
                     u'B003BNZ3HS',
                     u'B0746NVGDZ',
                     u'B01M1J6L1Y',
                     u'B07FKGJCLQ',
                     u'B071R7D8LN',
                     u'B07FD5MNL9',
                     u'B007MWG1LG',
                     u'B07C95H883',
                     u'B071Y7YR5P',
                     u'B06ZXS4TJD',
                     u'B071R7DCRY',
                     u'B0746NSLXF',
                     u'B0777Y5HKN',
                     u'B07FD2V1XF',
                     u'B077HYT38Y',
                     u'B077HN2ZQW',
                     u'B003BNZ3H8',
                     u'B01LYATO4U',
                     u'B077HT9HN1',
                     u'B003BNZ3GO',
                     u'B071R7DDKZ',
                     u'B007MWG0IU',
                     u'B00DN5VQJ8',
                     u'B00ANGZE0W',
                     u'B071XPJN6L',
                     u'B0746NMHCS',
                     u'B077HS1CP4',
                     u'B071R7DDKW',
                     u'B007MWG3RS',
                     u'B06ZYC64PK',
                     u'B003BNZ3GY',
                     u'B077HPWGK7',
                     u'B01M0WOSR6',
                     u'B0777XJV3M',
                     u'B073F7MKYT',
                     u'B07FD44WTR',
                     u'B071Y7ZFRR',
                     u'B071CF86YY',
                     u'B004O5LS58',
                     u'B00DN5VQHA',
                     u'B004O5E3AA',
                     u'B077J1R3CG',
                     u'B004L9K9W0',
                     u'B006U6D636',
                     u'B01LXZ8EVL',
                     u'B0746NX9RR',
                     u'B07FKFVL1G',
                     u'B00ANGZCTA',
                     u'B01M1JGGAQ',
                     u'B0746NC8J1',
                     u'B003BNZ4Q8',
                     u'B00DN5VQKM',
                     u'B003BNZ3E6',
                     u'B071CZQNPC',
                     u'B071CFPN9G',
                     u'B07FD2VGP5',
                     u'B004L9Q6NQ',
                     u'B00S2GELPY',
                     u'B06ZYC64KV',
                     u'B077HPGRKZ',
                     u'B00EVL13AK',
                     u'B07FD5MQZG',
                     u'B0746PG34K',
                     u'B071Y7L4MJ',
                     u'B06ZYXL6MV',
                     u'B06ZZHM1RY',
                     u'B07FD48W1N',
                     u'B077HLM9RQ',
                     u'B004ARUSA6',
                     u'B00IDZWOZI'],
 'variation_specifics': '{"Color": "On the Prowl", "Size": "7"}'}


def __is_valid_item(item):
    # check if variation, and valid
    if item.get('variation_specifics', None):
        parent_asin = item.get('parent_asin') if item.get('parent_asin') else item.get('asin')
        asin = item.get('asin')
        if parent_asin == asin:
            # a variation cannot have same parent_asin and asin
            return False
    return True


def __handle_redirected_asins(redirected_asins):
    """ make OOS if any redrected asin (not the same as end-point/final asin)
    """
    if len(redirected_asins) > 0:
        for r_asin in redirected_asins.values():
            a_item = AmazonItemModelManager.fetch_one(asin=r_asin)
            if not a_item:
                continue
            AmazonItemModelManager.oos(item=a_item)

def __cache_amazon_item(item):
    __handle_redirected_asins(redirected_asins=item.get('_redirected_asins', {}))

    amazon_item = AmazonItemModelManager.fetch_one(asin=item.get('asin', ''))
    if amazon_item == None: # create item
        if not item.get('status'): # do nothing
            # do not create new entry for any invalid data (i.e. 404 pages)
            return False
        AmazonItemModelManager.create(asin=item.get('asin'),
            parent_asin=item.get('parent_asin') if item.get('parent_asin') else item.get('asin'),
            url=item.get('url'),
            category=item.get('category'),
            title=item.get('title'),
            price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
            market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
            quantity=item.get('quantity'),
            features=item.get('features'),
            description=item.get('description'),
            specifications=item.get('specifications'),
            variation_specifics=item.get('variation_specifics'),
            review_count=item.get('review_count'),
            avg_rating=item.get('avg_rating'),
            is_fba=item.get('is_fba'),
            is_addon=item.get('is_addon'),
            is_pantry=item.get('is_pantry'),
            has_sizechart=item.get('has_sizechart'),
            international_shipping=False,
            merchant_id=item.get('merchant_id'),
            merchant_name=item.get('merchant_name'),
            brand_name=item.get('brand_name'),
            meta_title=item.get('meta_title'),
            meta_description=item.get('meta_description'),
            meta_keywords=item.get('meta_keywords'),
            status=item.get('status'))
        print("[ASIN:{}] created in db".format(item.get('asin')))
    else: # update item
        if not item.get('status'):
            AmazonItemModelManager.inactive(amazon_item)
            return True
        AmazonItemModelManager.update(item=amazon_item,
            parent_asin=item.get('parent_asin') if item.get('parent_asin', None) else item.get('asin'),
            url=item.get('url'),
            category=item.get('category'),
            title=item.get('title'),
            price=amazonmws_utils.number_to_dcmlprice(item.get('price')),
            market_price=amazonmws_utils.number_to_dcmlprice(item.get('market_price')),
            quantity=item.get('quantity'),
            features=item.get('features'),
            description=item.get('description'),
            specifications=item.get('specifications'),
            variation_specifics=item.get('variation_specifics'),
            review_count=item.get('review_count'),
            avg_rating=item.get('avg_rating'),
            is_fba=item.get('is_fba'),
            is_addon=item.get('is_addon'),
            is_pantry=item.get('is_pantry'),
            has_sizechart=item.get('has_sizechart'),
            international_shipping=False,
            merchant_id=item.get('merchant_id'),
            merchant_name=item.get('merchant_name'),
            brand_name=item.get('brand_name'),
            meta_title=item.get('meta_title'),
            meta_description=item.get('meta_description'),
            meta_keywords=item.get('meta_keywords'),
            status=item.get('status'))
        print("[ASIN:{}] updated in db".format(item.get('asin')))
    return True


def process_item(item):
    if item.get('_cached', False):
        print("[ASIN:{}] _cached - no database saving".format(item.get('asin')))
        # this item is cached. do not save into db
        return item
    if not __is_valid_item(item):
        print("[ASIN:{}] NOT valid item - status will be False".format(item.get('asin')))
        item['status'] = False
    __cache_amazon_item(item)
    return item


if __name__ == "__main__":
    process_item(item=_item)
