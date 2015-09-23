import sys, os, traceback
import json
import uuid

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

        myitem1 = {
            "Item": {
                "Title": "Harry Potter and the Philosopher's Stone",
                "Description": "This is the first book in the Harry Potter series. In excellent condition!",
                "PrimaryCategory": {"CategoryID": "180023"},
                "StartPrice": "1.00",
                "CategoryMappingAllowed": "true",
                "Country": "US",
                "ConditionID": "3000",
                "Currency": "USD",
                "DispatchTimeMax": "3",
                "ListingDuration": "Days_7",
                "ListingType": "Chinese",
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": "oroojass-facilitator@hotmail.com",
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

        myitem2 = {
            "Item": {
                "Title": "TEST TITLE",
                "Description": "TEST Description",
                "PrimaryCategory": {
                    "CategoryID": "180023",
                },
                "PictureDetails": {
                    "PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
                    "PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
                },
                "StartPrice": 19.99,


                # "AutoPay": True,
                "CategoryBasedAttributesPrefill": True,
                "CategoryMappingAllowed": True,
                "ConditionID": 1000,
                "Country": "US",
                "Currency": "USD",
                "DispatchTimeMax": 2,
                "HitCounter": "HiddenStyle", # could be changed later
                "IncludeRecommendations": True,
                "InventoryTrackingMethod": "ItemID",
                "ListingDuration": "GTC", # Good 'Til Cancelled
                "ListingType": "FixedPriceItem",
                "Location": "Nationwide, United States",
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": "oroojass-facilitator@hotmail.com",
                "PostCheckoutExperienceEnabled": True,
                "Quantity": 100,
                "BuyerRequirementDetails": {
                    "ShipToRegistrationCountry": True,
                },
                "ReturnPolicy": {
                    "Description": "The buyer has 14 days to return the item (the buyer pays shipping fees). The item will be refunded. 10% restocking fee may apply.",
                    "RefundOption": "MoneyBackOrExchange",
                    "RestockingFeeValueOption": "Percent_10",
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "ReturnsWithinOption": "Days_14",
                    "ShippingCostPaidByOption": "Buyer",
                },
                # "SellerProfiles": SellerProfilesType # need to revisit
                "ShippingDetails": {
                    "ExcludeShipToLocation": "Alaska/Hawaii",
                    "ExcludeShipToLocation": "US Protectorates",
                    "ExcludeShipToLocation": "APO/FPO",
                    "ExcludeShipToLocation": "PO Box",
                    "GlobalShipping": False,
                    "ShippingType": "Flat",
                    "ShippingServiceOptions": {
                        "ShippingServicePriority": 1,
                        "ShippingService": "UPSGround",
                        "FreeShipping": True,
                        "ShippingServiceAdditionalCost": 0.00,
                    },

                },
                "ShipToLocations": "US",
                "Site": "US",
                # "Storefront": StorefrontType # need to revisit
                # "ThirdPartyCheckout": boolean # need to revisit
                # "ThirdPartyCheckoutIntegration": boolean # need to revisit
                # "Variations": VariationsType # need to revisit
            },
            "MessageID": uuid.uuid4(),
        }

        # api.execute('VerifyAddItem', myitem1)
        # api.execute('VerifyAddItem', myitem2)
        api.execute('VerifyAddFixedPriceItem', myitem2)
        dump(api, True)

    except ConnectionError as e:
        print e
        print e.response.dict()

def addItem():

    try:
        api = Trading(debug=True, warnings=True, domain="api.sandbox.ebay.com")

        # myitem = {
        #     "Item": {
        #         "Title": "TEST TITLE",
        #         "Description": "TEST Description",
        #         "PictureDetails": {
        #             "PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        #             "PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        #         },
        #         "StartPrice": 19.99,


        #         "AutoPay": True,
        #         "CategoryBasedAttributesPrefill": True,
        #         "CategoryMappingAllowed": True,
        #         "ConditionID": 1000,
        #         "Country": "US",
        #         "Currency": "USD",
        #         "DispatchTimeMax": 2,
        #         "HitCounter": "HiddenStyle",
        #         "IncludeRecommendations": True,
        #         "InventoryTrackingMethod": "ItemID",
        #         "ListingDuration": "GTC", # Good 'Til Cancelled
        #         "ListingType": "FixedPriceItem",
        #         "Location": "Nationwide, United States",
        #         "PaymentMethods": "PayPal",
        #         "PayPalEmailAddress": "oroojass-facilitator@hotmail.com",
        #         "PostCheckoutExperienceEnabled": True,
        #         "PrimaryCategory": {
        #             "CategoryID": "180023",
        #         },
        #         "Quantity": 100,
        #         "BuyerRequirementDetails": {
        #             "ShipToRegistrationCountry": True,
        #         },
        #         "ReturnPolicy": {
        #             "Description": "The buyer has 14 days to return the item (the buyer pays shipping fees). The item will be refunded. 10% restocking fee may apply.",
        #             "RefundOption": "MoneyBackOrExchange",
        #             "RestockingFeeValueOption": "Percent_10",
        #             "ReturnsAcceptedOption": "ReturnsAccepted",
        #             "ReturnsWithinOption": "Days_14",
        #             "ShippingCostPaidByOption": "Buyer",
        #         },
        #         # "SellerProfiles": SellerProfilesType # need to revisit
        #         "ShippingDetails": {
        #             "ExcludeShipToLocation": "Alaska/Hawaii",
        #             "ExcludeShipToLocation": "US Protectorates",
        #             "ExcludeShipToLocation": "APO/FPO",
        #             "ExcludeShipToLocation": "PO Box",
        #             "GlobalShipping": False,
        #             "ShippingServiceOptions": {
        #                 "ShippingServicePriority": 1,
        #                 "FreeShipping": True,
        #             },
        #             "ShippingType": "Flat",

        #         },
        #         "ShipToLocations": "US",
        #         "Site": "US",
        #         # "Storefront": StorefrontType # need to revisit
        #         # "ThirdPartyCheckout": boolean # need to revisit
        #         # "ThirdPartyCheckoutIntegration": boolean # need to revisit
        #         # "Variations": VariationsType # need to revisit
        #         "MessageID": uuid.uuid4(),
        #     }
        # }

        api.execute('AddFixedPriceItem', myitem)
        dump(api, True)

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

def findProduct(keywords):
    """use FindItemsAdvanced call and find ebay category id from the result
    """
    try:
        api = Finding(debug=False, warnings=True)

        api_request = {
            'keywords': keywords,
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
            # 'affiliate': { 'trackingId': 1 },
            # 'sortOrder': 'CountryDescending',
            'paginationInput': {
                'entriesPerPage': 10,
                'pageNumber': 1,
            },
        }

        response = api.execute('findItemsAdvanced', api_request)
        dump(api, True)

        # if api.response.content:
        #     data = json.loads(api.response.json())




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
    verifyAddItem()
    # storeEbayCategories(220) # Toys & Hobbies
    # storeEbayCategories(2984) # Baby
    # getCategories() # get top level categories on ebay
    # findProduct("Cards Against Humanity")
