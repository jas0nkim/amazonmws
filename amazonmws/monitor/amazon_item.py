import sys, os, traceback

sys.path.append('%s/../../' % os.path.dirname(__file__))

import uuid
import datetime

from decimal import Decimal
from boto.mws.connection import MWSConnection

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import utils
from amazonmws import settings as am_settings
from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, EbayListingError, ItemPriceHistory

from amazonmws.ebaystore import settings as eb_settings
from amazonmws.ebaystore.listing import OnError, calculate_profitable_price

class PriceMonitor(object):

    asin_price_list = []
    # e.g. [
    #   (u'00ABCDE', Decimal('23.99')),
    #   (u'00ABCDF', Decimal('13.99')),
    #   (u'00ABCDG': Decimal('43.99')),
    # ]
    conn = None

    curr_amazon_item = None
    curr_ebay_item = None

    def __init__(self, asin_price_list):
        self.conn = MWSConnection(SellerId=am_settings.AMAZON_SELLER_ID)
        self.asin_price_list = asin_price_list

        print "*"*10
        print "ASIN-PRICE list"
        print asin_price_list
        print "*"*10

    def run(self):

        asin_list = [i[0] for i in self.asin_price_list]

        print "*"*10
        print "ASIN only list"
        print asin_list
        print "*"*10

        response = self.conn.get_competitive_pricing_for_asin(MarketplaceId=am_settings.AMAZON_MARKETPLACE_ID, ASINList=asin_list)
        
        if response.GetCompetitivePricingForASINResult:
            for result in response.GetCompetitivePricingForASINResult:
                if result.Error != None: # skip if any error on response
                    continue
                
                curr_asin = result.Product.Identifiers.MarketplaceASIN.ASIN

                print curr_asin

                for compatitive_prices in result.Product.CompetitivePricing:
                    for compatitive_price in compatitive_prices.CompetitivePrices.CompetitivePrice:
                        if compatitive_price['condition'] != 'New': # skip not NEW products
                            continue

                        # most recent price
                        price_via_api = Decimal(float(compatitive_price.Price.LandedPrice)).quantize(Decimal('1.00'))

                        # the price from list of tuples
                        prince_in_db = [item for item in self.asin_price_list if item[0] == curr_asin][0][1]

                        print "Price via api VS Price in db"
                        print price_via_api
                        print "VS"
                        print prince_in_db
                        print "*"*10

                        # compare prices from amazon and my db
                        if price_via_api != prince_in_db:
                            self.__update_price(curr_asin, price_via_api)

                        self.__reset_curr_objs()
                        break

    def __reset_curr_objs(self):
        self.curr_amazon_item = None
        self.curr_ebay_item = None

    def __set_curr_objs(self, asin):
        self.curr_amazon_item = StormStore.find(AmazonItem, AmazonItem.asin == asin).one()

        try:
            self.curr_ebay_item = StormStore.find(EbayItem, EbayItem.amazon_item_id == self.curr_amazon_item.id).one()
        except StormError as err:
            print 'No ebay_item entry yet.', err
            self.curr_ebay_item = None

    def __update_price(self, asin, amazon_price):
        self.__set_curr_objs(asin)

        if self.curr_ebay_item:

            ebay_price = calculate_profitable_price(amazon_price)

            revised = self.__revise_ebay_item(ebay_price)

            if revised:
                try:
                    self.curr_amazon_item.price = amazon_price
                    StormStore.add(self.curr_amazon_item)

                    self.curr_ebay_item.eb_price = ebay_price
                    StormStore.add(self.curr_ebay_item)
                    
                    price_history = AmazonItemPriceHistory()
                    price_history.amazon_item_id = self.curr_amazon_item.id
                    price_history.asin = self.curr_amazon_item.asin
                    price_history.ebay_item_id = self.curr_ebay_item.id
                    price_history.ebid = self.curr_ebay_item.id
                    price_history.am_price = self.curr_amazon_item.price
                    price_history.eb_price = self.curr_ebay_item.eb_price
                    price_history.created_at = datetime.datetime.now()
                    price_history.updated_at = datetime.datetime.now()                    
                    StormStore.add(self.price_history)

                    StormStore.commit()

                    print "*"*10 + "PRICE UPDATED" + "*"*10
                    print new_price
                    print "*"*10

                except StormError as err:
                    print 'Error on updating new prices in amazon_items and ebay_items tables:', err
                    self.__log_on_error(u'Price has been revised at ebay, but error occurred updating new prices in amazon_items and ebay_items tables')
        else:
            try:
                price_history = AmazonItemPriceHistory()
                price_history.amazon_item_id = self.curr_amazon_item.id
                price_history.asin = self.curr_amazon_item.asin
                price_history.am_price = self.curr_amazon_item.price
                price_history.created_at = datetime.datetime.now()
                price_history.updated_at = datetime.datetime.now()
                StormStore.add(self.price_history)

                StormStore.commit()

            except StormError as err:
                print 'Error on updating new prices in amazon_items table:', err
                self.__log_on_error(u'Error occurred updating new prices in amazon_items table - item which has not listed on ebay yet')


    def __revise_ebay_item(self, new_price):

        ret = False

        item_obj = self.__generate_ebay_revise_item_obj(new_price)
        is_verified = self.__verify_revise_item(item_obj)

        if is_verified:

            item_obj['Item']['VerifyOnly'] = False

            try:
                api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")
                api.execute('ReviseItem', item_obj)

                if api.response.content:
                    data = json.loads(api.response.json())

                    # print json.dumps(data, indent=4, sort_keys=True)

                    if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                        ret = True

                    else:
                        self.__log_on_error(unicode(api.response.json()), u'ReviseItem')

            except ConnectionError as e:
                print e
                print e.response.dict()
                self.__log_on_error(unicode(e.response.dict()), u'ReviseItem')

            return ret

    def __verify_revise_item(self, item_obj):
        ret = False

        try:
            api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")
            api.execute('ReviseItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True

                else:
                    self.__log_on_error(unicode(api.response.json()), u'ReviseItem')

        except ConnectionError as e:
            print e
            print e.response.dict()
            self.__log_on_error(unicode(e.response.dict()), u'ReviseItem')

        return ret

    def __generate_ebay_revise_item_obj(self, new_price, verify_only=True):

        picture_urls = []

        try:
            item_pictures = StormStore.find(AmazonItemPicture, AmazonItemPicture.amazon_item_id == self.curr_amazon_item.id)

            picture_urls = [item_picture.ebay_picture_url for item_picture in item_pictures]

        except StormError as err:
            print 'Error on fetching from AmazonItemPicture:', err
            self.__log_on_error(u'No item pictures found in amazon_item_pictures table')

        item = eb_settings.EBAY_REVISE_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['ItemID'] = self.curr_ebay_item.ebid
        item['Item']['Title'] = self.curr_amazon_item.title
        item['Item']['Description'] = "<![CDATA[\n" +  eb_settings.EBAY_ITEM_DESCRIPTION_CSS + self.curr_amazon_item.description + eb_settings.EBAY_ITEM_DESCRIPTION_JS + "\n]]>"
        item['Item']['Title'] = self.curr_amazon_item.title
        item['Item']['PrimaryCategory']['CategoryID'] = self.curr_ebay_item.ebay_category_id
        if len(picture_urls) > 0:
            item['Item']['PictureDetails']['PictureURL'] = picture_urls
        item['Item']['StartPrice']['#text'] = new_price
        item['Item']['BuyItNowPrice']['#text'] = new_price
        item['Item']['VerifyOnly'] = verify_only

        return item

    def __log_on_error(self, reason, related_ebay_api=u''):
        OnError(self.curr_amazon_item,
            EbayListingError.TYPE_ERROR_ON_REVISE,
            reason,
            related_ebay_api,
            self.curr_ebay_item)


if __name__ == "__main__":
    
    amazon_items = StormStore.find(AmazonItem, AmazonItem.status == AmazonItem.STATUS_ACTIVE)

    if amazon_items.count() > 0:

        # ref: http://docs.developer.amazonservices.com/en_DE/products/Products_GetCompetitivePricingForASIN.html
        max_items = 20
        i = 0

        while max_items * i < amazon_items.count():
            start = max_items * i

            i += 1
            end = max_items * i

            asin_price_list = tuple((item.asin, item.price) for item in amazon_items[start:end])

            monitor = PriceMonitor(asin_price_list)
            monitor.run()

