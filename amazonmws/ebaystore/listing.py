import sys, os, traceback
import json
import uuid
import datetime
import operator

sys.path.append('%s/../../' % os.path.dirname(__file__))

from storm.exceptions import StormError

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from amazonmws.models import StormStore, AmazonItem, AmazonItemPicture, Scraper, ScraperAmazonItem, EbayItem, UnlistedAmazonItem


class FromAmazonToEbay(object):

    amazon_item = None

    def __init__(self, amazon_item):
        self.amazon_item = amazon_item
        pass

    def list(self):
        category_id = self.__find_ebay_category_id()

        if category_id < 0:
            # store in seperate database
            self.__log_as_unlisted('Unable to find primary category at ebay')
            return

        else:
            print "Category ID: " + str(category_id)

        return


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

                print json.dumps(data, indent=4, sort_keys=True)

                if data['ack'] == "Success":

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

        return desired_category_id


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

            break

        return True

    def __filter_items(self):
        """filter amazon item by:
            - amazon active item
            - item which has not listed at ebay store
            - scraper (if applicable)

            return type: storm.store.ResultSet or empty list
        """

        filtered_items = []

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
                # print 'New item!'
                num_new_items += 1
                continue

            if already_exists:
                filtered_items.remove(item)

        print "New items: " + str(num_new_items)

        return filtered_items


if __name__ == "__main__":
    handler = ListingHandler(Scraper.amazon_halloween_accessories)
    handler.run()
