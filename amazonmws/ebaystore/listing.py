import sys, os, traceback

sys.path.append('%s/../../' % os.path.dirname(__file__))

import json
import uuid
import datetime
import operator
import uuid

from decimal import Decimal

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, UnlistedAmazonItem

import settings


class FromAmazonToEbay(object):

    amazon_item = None
    quantity = 1

    def __init__(self, amazon_item, quantity=100):
        self.amazon_item = amazon_item
        self.quantity = quantity
        pass

    def list(self):
        category_id = self.__find_ebay_category_id()

        if category_id < 0:
            return

        listing_price = self.__calculate_profitable_price()

        if listing_price < 0:
            return

        item_pictures = self.__get_item_pictures()

        item_obj = self.__generate_ebay_add_item_obj(category_id, listing_price, item_pictures)
        
        verified = self.__verify_add_item(item_obj)
        
        if verified:
            self.__add_item(item_obj, category_id, listing_price)


        # print "Category ID: " + str(category_id)

        return

    def __generate_ebay_add_item_obj(self, category_id, listing_price, item_pictures):

        # picture urls
        picture_urls = []

        for item_picture in item_pictures:
            if item_picture.converted_picture_url:
                picture_urls.append(item_picture.converted_picture_url)
            else:
                picture_urls.append(item_picture.original_picture_url)

        print "*****"
        print self.amazon_item.description
        print "*****"

        item = settings.EBAY_ADD_ITEM_TEMPLATE
        item['MessageID'] = uuid.uuid4()
        item['Item']['Title'] = self.amazon_item.title
        item['Item']['Description'] = "<![CDATA[\n" + self.amazon_item.description + "\n]]>"
        item['Item']['Title'] = self.amazon_item.title
        item['Item']['PrimaryCategory']['CategoryID'] = category_id
        item['Item']['PictureDetails']['PictureURL'] = picture_urls
        item['Item']['StartPrice'] = listing_price
        item['Item']['Quantity'] = self.quantity

        return item

    def __get_item_pictures(self):
        return StormStore.find(AmazonItemPicture, AmazonItemPicture.amazon_item_id == self.amazon_item.id)


    def __find_ebay_category_id(self):
        desired_category_id = -1

        try:
            api = Finding(debug=False, warnings=True)

            api_request = {
                'keywords': self.amazon_item.title,
                'itemFilter': [
                    # {
                    #     'name': 'Condition',
                    #     'value': 'Used'
                    # },
                    {
                        'name': 'LocatedIn',
                        'value': 'US'
                    },
                ],
                'sortOrder': 'BestMatch',
                'paginationInput': {
                    'entriesPerPage': 50,
                    'pageNumber': 1,
                },
            }

            api.execute('findItemsAdvanced', api_request)
            # print api

            category_set = {}

            if api.response.content:
                data = json.loads(api.response.json())

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):

                    # print json.dumps(data, indent=4, sort_keys=True)

                    if int(data['searchResult']['_count']) > 0:
                        for searched_item in data['searchResult']['item']:
                            try:
                                searched_category_id = searched_item['primaryCategory']['categoryId']

                                category_set[searched_category_id] = category_set[searched_category_id] + 1 if searched_category_id in category_set else 1
                            
                            except KeyError as err:
                                print 'Category id key not found'
                                continue

            else:
                print "ERROR NO RESPONSE CONTENT"

            if len(category_set) < 1:
                print "Unable to find ebay category for this item: " + self.amazon_item.title

            else:
                # get most searched caregory id
                desired_category_id = max(category_set.iteritems(), key=operator.itemgetter(1))[0]

        except ConnectionError as e:
            print e
            print e.response.dict()

        if desired_category_id < 0:
            # store in seperate database
            self.__log_as_unlisted(u'Unable to find primary category at ebay')

        return desired_category_id

    def __calculate_profitable_price(self, margin_percentage=3):
        """i.e. with 3 percent margin
            
            ((cost * 1.09 + .20) * 1.029 + .30) * 1.03

            - * 1.09: 9 percent final value fee charged by ebay
            - + .20: 20 cent listing fee charged by ebay
            - * 1.029: 2.9 percent transaction fee charged by paypal
            - + .30: 30 cent transaction fee by paypal
            - and my 3 percent margin
        """
        
        profitable_price = -1

        try:
            profitable_price = Decimal(((float(self.amazon_item.price) * 1.10 + 0.30) * 1.029 + 0.30) * (1.00 + float(margin_percentage) / 100)).quantize(Decimal('1.00'))

        except Exception as err:
            self.__log_as_unlisted(u"Unable tp calculate profitable price")

        return profitable_price


    def __verify_add_item(self, item_obj):
        ret = False

        try:
            api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")
            api.execute('VerifyAddFixedPriceItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                # print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    ret = True
                else:
                    self.__log_as_unlisted(api.response.json())

        except ConnectionError as e:
            print e
            print e.response.dict()
            self.__log_as_unlisted(unicode(e.response.dict()))

        return ret

    def __add_item(self, item_obj, category_id, price):
        ret = False

        try:
            api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")
            api.execute('AddFixedPriceItem', item_obj)

            if api.response.content:
                data = json.loads(api.response.json())

                print json.dumps(data, indent=4, sort_keys=True)

                if ('ack' in data and data['ack'] == "Success") or ('Ack' in data and data['Ack'] == "Success"):
                    
                    ret = True
                    self.__store_ebay_item(data['ItemID'], category_id, price)

                else:
                    self.__log_as_unlisted(api.response.json())


        except ConnectionError as e:
            print e
            print e.response.dict()
            self.__log_as_unlisted(e)

        return ret

    def __store_ebay_item(self, ebay_item_id, category_id, price):
        try:
            ebay_item = EbayItem()
            ebay_item.amazon_item_id = self.amazon_item.id
            ebay_item.asin = self.amazon_item.asin
            ebay_item.ebid = ebay_item_id
            ebay_item.ebay_category_id = category_id
            ebay_item.ebay_category_id = category_id
            ebay_item.eb_price = price
            ebay_item.quantity = self.quantity
            ebay_item.status = EbayItem.STATUS_ACTIVE
            ebay_item.created_at = datetime.datetime.now()
            ebay_item.updated_at = datetime.datetime.now()

            StormStore.add(ebay_item)
            StormStore.commit()

        except StormError as err:
            print 'EbayItem db insertion error:', err
            StormStore.rollback()
            self.__log_as_unlisted(u"Listed at ebay, but unable to store information in ebay_items table")

    def __log_as_unlisted(self, reason):
        try:
            unlisted = UnlistedAmazonItem()
            unlisted.amazon_item_id = self.amazon_item.id
            unlisted.asin = self.amazon_item.asin
            unlisted.reason = reason
            unlisted.status = UnlistedAmazonItem.STATUS_UNLISTED
            unlisted.created_at = datetime.datetime.now()
            unlisted.updated_at = datetime.datetime.now()

            StormStore.add(unlisted)
            StormStore.commit()

        except StormError as err:
            print 'UnlistedAmazonItem db insertion error:', err
            StormStore.rollback()


class ListingHandler(object):

    scraper_id = None

    def __init__(self, scraper_id=None):
        self.scraper_id = scraper_id

    def run(self):
        items = self.__filter_items()

        for item in items:
            to_ebay = FromAmazonToEbay(item)
            to_ebay.list()

            # break

        return True

    def __filter_items(self):
        """filter amazon item by:
            - amazon active item
            - item which has not listed at ebay store
            - scraper (if applicable)

            return type: list
        """

        result = []

        try:
            if self.scraper_id:
                filtered_items = StormStore.find(AmazonItem,
                    ScraperAmazonItem.amazon_item_id == AmazonItem.id,
                    ScraperAmazonItem.scraper_id == self.scraper_id,
                    AmazonItem.status == AmazonItem.STATUS_ACTIVE)
            
            else:
                filtered_items = StormStore.find(AmazonItem, AmazonItem.status == AmazonItem.STATUS_ACTIVE)

        except StormError as err:
            print 'Unable to filter amazon items:', err

        # workaround solution - stupid but storm doesn't support outer join...
        # what it supposes to do - i.e.
        #   SELECT * FROM pets AS p 
        #       LEFT OUTER JOIN lost-pets AS lp
        #       ON p.name = lp.name
        #       WHERE lp.id IS NULL
        #       
        # ref: http://stackoverflow.com/a/369861
        num_new_items = 0

        for item in filtered_items:
            already_exists = False
            try:
                already_exists = StormStore.find(EbayItem, EbayItem.amazon_item_id == item.id).one()
            
            except StormError as err:
                print "Error on finding item in ebay_items table"

            if not already_exists:
                # print 'New item!'
                num_new_items += 1
                result.append(item)

        print "New items: " + str(num_new_items)

        return result


if __name__ == "__main__":
    handler = ListingHandler(Scraper.amazon_halloween_accessories)
    handler.run()
