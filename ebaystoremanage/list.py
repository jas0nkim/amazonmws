import sys, os, traceback
import json

from ebaysdk.trading import Connection as Trading
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

from storm.exceptions import StormError

from common import dump
from models import StormStore, EbayProductCategory

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

def verifyAddItem():
    """http://www.utilities-online.info/xmltojson/#.UXli2it4avc
    """

    try:
        api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")

        myitem = {
            "Item": {
                "Title": "Harry Potter and the Philosopher's Stone",
                "Description": "This is the first book in the Harry Potter series. In excellent condition!",
                "PrimaryCategory": {"CategoryID": "377"},
                "StartPrice": "1.0",
                "CategoryMappingAllowed": "true",
                "Country": "US",
                "ConditionID": "3000",
                "Currency": "USD",
                "DispatchTimeMax": "3",
                "ListingDuration": "Days_7",
                "ListingType": "Chinese",
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": "oroojass@hotmail.com",
                "PictureDetails": {"PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007"},
                "PostalCode": "95125",
                "Quantity": "1",
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30",
                    "Description": "If you are not satisfied, return the book for refund.",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "ShippingDetails": {
                    "ShippingType": "Flat",
                    "ShippingServiceOptions": {
                        "ShippingServicePriority": "1",
                        "ShippingService": "USPSMedia",
                        "ShippingServiceCost": "2.50"
                    }
                },
                "Site": "US"
            }
        }

        api.execute('VerifyAddItem', myitem)
        dump(api)

    except ConnectionError as e:
        print e
        print e.response.dict()


def getCategories():

    try:
        api = Trading(debug=False, warnings=True, domain="api.sandbox.ebay.com")

        options1 = { 
            "CategorySiteID": 0, 
            "LevelLimit": 1, 
            "DetailLevel": "ReturnAll",
        }

        api.execute('GetCategories', options1)
        dump(api, True)

        # options2 = {
        #     "CategorySiteID": 0, 
        #     "CategoryParent": "220", # Toys & Hobbies
        #     # "LevelLimit": 1, 
        #     "DetailLevel": "ReturnAll",
        # }

        # api.execute('GetCategories', options2)
        # dump(api, True)

        # options3 = { 
        #     "CategorySiteID": 0, 
        #     "CategoryParent": "1249", # Video Games & Consoles
        #     # "LevelLimit": 1, 
        #     "DetailLevel": "ReturnAll",
        # }

        # api.execute('GetCategories', options3)
        # dump(api, True)

    except ConnectionError as e:
        print e
        print e.response.dict()

def findProduct():

    try:
        api = Finding(debug=False, warnings=True)

        api_request = {
            'keywords': u'GRAMMY Foundation',
            'itemFilter': [
                {
                    'name': 'Condition',
                    'value': 'Used'
                },
                # {
                #     'name': 'LocatedIn',
                #     'value': 'GB'
                # },
            ],
            'affiliate': { 'trackingId': 1 },
            'sortOrder': 'CountryDescending',
        }

        response = api.execute('findItemsAdvanced', api_request)

        dump(api, True)

    except ConnectionError as e:
        print e
        print e.response.dict()


def storeEbayCategories(category_parent_id):

    try:
        api = Trading(debug=False, warnings=True, domain="api.sandbox.ebay.com")

        options = {
            "CategorySiteID": 0, # US site
            "CategoryParent": str(category_parent_id),
            "DetailLevel": "ReturnAll",
        }

        api.execute('GetCategories', options)
        dump(api, True)

        if api.response.content:
            data = json.loads(api.response.json())

            if data['Ack'] == "Success":

                count_stored = 0

                for category in data['CategoryArray']['Category']:

                    already_exists = True

                    try:

                        # check if the item already exists in database
                        already_exists = StormStore.find(EbayProductCategory, EbayProductCategory.category_id == int(category['CategoryID'])).one()
                    
                    except StormError as err:
                        print err
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        continue


                    if not already_exists:
                        # store in db
                        
                        try:

                            ebay_prod_category = EbayProductCategory()
                            ebay_prod_category.category_id = int(category['CategoryID'])
                            ebay_prod_category.category_level = int(category['CategoryLevel'])
                            ebay_prod_category.category_name = category['CategoryName']
                            ebay_prod_category.category_parent_id = int(category['CategoryParentID'])
                            ebay_prod_category.auto_pay_enabled = True if category['AutoPayEnabled'] == "true" else False
                            ebay_prod_category.best_offer_enabled = True if category['BestOfferEnabled'] == "true" else False
                            ebay_prod_category.leaf_category = True if 'LeafCategory' in category else False

                            StormStore.add(ebay_prod_category)
                            count_stored += 1

                        except StormError as err:
                            print err
                            print '-'*60
                            traceback.print_exc(file=sys.stdout)
                            print '-'*60
                            continue

                    else:
                        print category['CategoryName'] + " already exists in db"
                        continue

                if count_stored > 0:
                    StormStore.commit()

    except ConnectionError as e:
        print e
        print e.response.dict()

if __name__ == "__main__":
    storeEbayCategories(220) # Toys & Hobbies
    storeEbayCategories(2984) # Baby
    # getCategories()
    # findProduct()
