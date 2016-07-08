import os
import logging

import yaml

# Application
APP_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
CONFIG_PATH = os.path.join(ROOT_PATH, 'config')
SCRAPER_PATH = os.path.join(ROOT_PATH, 'scrapers')
LOCK_PATH = os.path.join(ROOT_PATH, 'locks')
TEMP_PATH = os.path.join(ROOT_PATH, 'tmp')

__app_config = None

with open(os.path.join(CONFIG_PATH, 'app.yaml'), 'r') as stream:
    __app_config = yaml.load(stream)

APP_ENV = __app_config["env"]
APP_HOST = __app_config["host"]["main"]
APP_HOST_ORDERING = __app_config["host"]["ordering"]
APP_PORT_SOAP = __app_config["port"]["soap"]
APP_PORT_RESTFUL = __app_config["port"]["restful"]

APP_MYSQL_HOST = __app_config["mysql"]["host"]
APP_MYSQL_PORT = __app_config["mysql"]["port"]
APP_MYSQL_DATABASE = __app_config["mysql"]["database"]
APP_MYSQL_USERNAME = __app_config["mysql"]["username"]
APP_MYSQL_PASSWORD = __app_config["mysql"]["password"]

APP_RABBITMQ_HOST = __app_config["rabbitmq"]["host"]
APP_RABBITMQ_PORT = __app_config["rabbitmq"]["port"]
APP_RABBITMQ_VHOST = __app_config["rabbitmq"]["vhost"]
APP_RABBITMQ_USERNAME = __app_config["rabbitmq"]["username"]
APP_RABBITMQ_PASSWORD = __app_config["rabbitmq"]["password"]

APP_LOG_SERVER_HOST = __app_config["log_server"]["host"]
APP_LOG_SERVER_PORT = __app_config["log_server"]["port"]

APP_CRAWLERA_HOST = __app_config["crawlera"]["host"]
APP_CRAWLERA_PORT = __app_config["crawlera"]["port"]
APP_CRAWLERA_API_KEY = __app_config["crawlera"]["api_key"]

APP_EBAY_NOTIFICATION_ENDPOINT_URL = __app_config["ebay"]["notification_endpoint_url"]

APP_LOG_LEVEL = logging.DEBUG if APP_ENV == 'stage' else logging.ERROR

# need to be replaced to ebay_store.email
# APP_DEFAULT_EMAIL = "redflagitems@gmail.com"

APP_DEFAULT_WEBDRIVERWAIT_SEC = 7

APP_HTTP_CONNECT_RETRY_TIMES = 7

APP_EBAY_LISTING_MARGIN_PERCENTAGE = 3
APP_EBAY_LISTING_MARGIN_MIN_DOLLAR = 0.00
APP_EBAY_LISTING_MARGIN_MAX_DOLLAR = 2.50
APP_EBAY_LISTING_USE_SALEXTAX_TABLE = False

STAGE_PAYPAL_ACCOUNT = 'oroojass-facilitator@hotmail.com'


# TOR / prioxy
PRIVOXY_LISTENER_PORT = 8118 # communicate with TOR via a local proxy (privoxy)
TOR_CLIENT_IP = '127.0.0.1'
TOR_CLIENT_PORT = 9050
TOR_CLIENT_PORT_TYPE = 'socks5'
TOR_CONTROLPORT_LISTENER_PORT = 9051
TOR_PASSWORD = '99aTmOzR079'
TOR_DEFAULT_SLEEP = 3

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT_LIST = [
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    # 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    # 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    # 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    # 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    # 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
    # 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',

    # chrome browser - version 40 and up
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    
    # chrome browser - version 36 and 37
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',

    # safari browser - version 7 and up
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
]

USER_AGENT_LIST_MOBILE = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4',
]

BOT_NAME = 'amazonmws'

SPIDER_MODULES = ['amazonmws.spiders']
NEWSPIDER_MODULE = 'amazonmws.spiders'

AMAZON_ITEM_LINK_PATTERN = r'^https?://www.amazon.com/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'
AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM = r'\._([^_]+)_\.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY = '._SL1500_.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY = '._SX522_.'
AMAZON_ITEM_LINK_FORMAT = "http://www.amazon.com/dp/%s"
AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT = "http://www.amazon.com/gp/offer-listing/%s?ie=UTF8&condition=new&startIndex=%d"
AMAZON_ORDER_LINK_FORMAT = "https://www.amazon.com/gp/your-account/order-history/?search=%s"
AMAZON_ORDER_ID_PATTERN = r'^[0-9]{3}\-[0-9]{7}\-[0-9]{7}$'

AMAZON_SELLER_ID = "A2I4JVBHOAUINI" if APP_ENV == "stage" else "A2I4JVBHOAUINI"
# AMAZON_MARKETPLACE_ID = "A2EUQ1WTGCTBG2" # CA
AMAZON_MARKETPLACE_ID = "ATVPDKIKX0DER" # US

AMAZON_MINIMUM_QUANTITY_FOR_LISTING = 10

EBAY_ITEM_DEFAULT_QUANTITY = 1
EBAY_ITEM_LINK_FORMAT = "http://www.sandbox.ebay.com/itm/%s" if APP_ENV == "stage" else "http://www.ebay.com/itm/%s"


#
######### ebay api related settings #########
#
__ebay_api_config = None

with open(os.path.join(CONFIG_PATH, 'ebay.yaml'), 'r') as stream:
    __ebay_api_config = yaml.load(stream)

EBAY_API_DEBUG = True if APP_ENV == 'stage' else False
EBAY_API_WARNINGS = True if APP_ENV == 'stage' else False

EBAY_TRADING_API_DOMAIN = "api.sandbox.ebay.com" if APP_ENV == "stage" else "api.ebay.com"

EBAY_API_APPID = __ebay_api_config[EBAY_TRADING_API_DOMAIN]["appid"]
EBAY_API_CERTID = __ebay_api_config[EBAY_TRADING_API_DOMAIN]["certid"]
EBAY_API_DEVID = __ebay_api_config[EBAY_TRADING_API_DOMAIN]["devid"]

EBAY_UPLOAD_SITE_HOSTED_PICTURE = {
    "MessageID": "",
    "ExternalPictureURL": "",


    # "ExtensionInDays": 90, # !!This call is restricted to applications that have been granted permission. Contact the eBay Developers Program to request premission!!
     
    # "PictureWatermark": "",
}

EBAY_ADD_ITEM_TEMPLATE = {
    "MessageID": "",
    "Item": {
        "SKU": "",
        "Title": "",
        "Description": "", # CDATA format with html 
                        # i.g 
                        # <![CDATA[
                        # abcde
                        # 12345
                        # ]]>
        "PrimaryCategory": {
            "CategoryID": "",
        },
        # "PictureDetails": {
        #     "PictureURL": [
        #         "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        #         "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        #     ],
        # },
        "PictureDetails": {
            "PictureURL": []
        },
        # "StartPrice": 19.99,
        "StartPrice": 0.99,
        "Quantity": EBAY_ITEM_DEFAULT_QUANTITY,
        "PayPalEmailAddress": "",
        "UseTaxTable": False,
        "ReturnPolicy": {
            "Description": "The buyer has 30 days to return the item (the buyer pays shipping fees). The item will be refunded. 10% restocking fee may apply.",
            "RefundOption": "MoneyBackOrExchange",
            "RestockingFeeValueOption": "Percent_10",
            "ReturnsAcceptedOption": "ReturnsAccepted",
            "ReturnsWithinOption": "Days_30",
            "ShippingCostPaidByOption": "Buyer",
        },
        # "ProductListingDetails": {
        #     "BrandMPN": {
        #         "Brand": "",
        #         "MPN": "",
        #     },
        #     "UPC": "",
        # },
        # "ItemSpecifics": {
        #     "NameValueList": []
        # },

        "AutoPay": False if APP_ENV == 'stage' else True,
        "CategoryBasedAttributesPrefill": True,
        "CategoryMappingAllowed": True,
        "ConditionID": 1000,
        "Country": "US",
        "Currency": "USD",
        "DispatchTimeMax": 1,
        "HitCounter": "HiddenStyle", # could be changed later
        "IncludeRecommendations": True,
        "InventoryTrackingMethod": "ItemID",
        "ListingDuration": "GTC", # Good 'Til Cancelled
        "ListingType": "FixedPriceItem",
        "Location": "Nationwide, United States",
        "PaymentMethods": "PayPal",
        "PostCheckoutExperienceEnabled": True,
        "BuyerRequirementDetails": {
            "ShipToRegistrationCountry": True,
        },
        # "SellerProfiles": SellerProfilesType # need to revisit
        "ShippingDetails": {
            "ExcludeShipToLocation": [
                "Alaska/Hawaii",
                "US Protectorates",
                "APO/FPO",
                "PO Box",
            ],
            "GlobalShipping": False,
            "ShippingType": "Flat",
            "ShippingServiceOptions": [
                {
                    "ShippingServicePriority": 1,
                    "ShippingService": "UPSGround",
                    "FreeShipping": True,
                    "ShippingServiceAdditionalCost": 0.00,
                },
                {
                    "ShippingServicePriority": 2,
                    "ShippingService": "UPS3rdDay",
                    "ShippingServiceCost": 3.99,
                    "ShippingServiceAdditionalCost": 0.00,
                },
                {
                    "ShippingServicePriority": 2,
                    "ShippingService": "UPSNextDay",
                    "ShippingServiceCost": 7.99,
                    "ShippingServiceAdditionalCost": 0.00,
                },
            ],
        },
        "ShipToLocations": "US",
        "Site": "US",
        # "Storefront": StorefrontType # need to revisit
        # "ThirdPartyCheckout": boolean # need to revisit
        # "ThirdPartyCheckoutIntegration": boolean # need to revisit
        # "Variations": VariationsType # need to revisit
    },
}

EBAY_REVISE_ITEM_TEMPLATE = {
    "MessageID": "",
    "Item": {
        "ItemID": "",
        #
        # optional
        # 
        # "Title": "",
        # "Description": "",
        # "StartPrice": 0.99,
        # "Quantity": EBAY_ITEM_DEFAULT_QUANTITY,
        # "PictureDetails": {
        #     "PictureURL": []
        # },
        # "PrimaryCategory": {
        #     "CategoryID": ""
        # },
    },
}

# EBAY_REVISE_ITEM_TEMPLATE = {
#     "MessageID": "",
#     "Item": {
#         "ItemID": "",
#         "Title": "",
#         "Description": "", # CDATA format with html 
#                         # i.g 
#                         # <![CDATA[
#                         # abcde
#                         # 12345
#                         # ]]>
#         "PrimaryCategory": {
#             "CategoryID": "",
#         },
#         # "PictureDetails": {
#         #     "PictureURL": [
#         #         "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
#         #         "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
#         #     ],
#         # },
#         "PictureDetails": {
#             "PictureURL": []
#         },
#         "StartPrice": 0.99,
#         "Quantity": EBAY_ITEM_DEFAULT_QUANTITY,
#         "PayPalEmailAddress": "",
#         "UseTaxTable": False,

#         "AutoPay": False if APP_ENV == 'stage' else True,
#         "CategoryBasedAttributesPrefill": True,
#         "CategoryMappingAllowed": True,
#         "ConditionID": 1000,
#         "Country": "US",
#         "DescriptionReviseMode": "Replace",
#         "DispatchTimeMax": 2,
#         "HitCounter": "HiddenStyle", # could be changed later
#         "IncludeRecommendations": True,
#         "InventoryTrackingMethod": "ItemID",
#         "ListingDuration": "GTC", # Good 'Til Cancelled
#         "ListingType": "FixedPriceItem",
#         "LiveAuction": False,
#         "Location": "Nationwide, United States",
#         "PaymentMethods": "PayPal",
#         "PostCheckoutExperienceEnabled": True,
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
#         # "SellerInventoryID": string # need to revisit
#         # "SellerProfiles": SellerProfilesType # need to revisit
#         "ShippingDetails": {
#             "ExcludeShipToLocation": [
#                 "Alaska/Hawaii",
#                 "US Protectorates",
#                 "APO/FPO",
#                 "PO Box",
#             ],
#             "GlobalShipping": False,
#             "ShippingType": "Flat",
#             "ShippingServiceOptions": [
#                 {
#                     "ShippingServicePriority": 1,
#                     "ShippingService": "UPSGround",
#                     "FreeShipping": True,
#                     "ShippingServiceAdditionalCost": 0.00,
#                 },
#                 {
#                     "ShippingServicePriority": 2,
#                     "ShippingService": "UPS3rdDay",
#                     "ShippingServiceCost": 3.99,
#                     "ShippingServiceAdditionalCost": 0.00,
#                 },
#                 {
#                     "ShippingServicePriority": 2,
#                     "ShippingService": "UPSNextDay",
#                     "ShippingServiceCost": 7.99,
#                     "ShippingServiceAdditionalCost": 0.00,
#                 },
#             ],
#         },
#         "ShipToLocations": "US",
#         # "Storefront": StorefrontType # need to revisit
#         # "ThirdPartyCheckout": boolean # need to revisit
#         # "ThirdPartyCheckoutIntegration": boolean # need to revisit
#         # "Variations": VariationsType # need to revisit
#     },
# }


EBAY_END_ITEM_TEMPLATE = {
    "MessageID": "",
    "ItemID": "",
    "EndingReason": "",
}

EBAY_REVISE_INVENTORY_STATUS_TEMPLATE = {
    "MessageID": "",
    "InventoryStatus": {
        "ItemID": "",
        "Quantity": "",
        "StartPrice": "",
    },
}

EBAY_USER_PREFERENCE_TEMPLATE = {
    "MessageID": "",
    "OutOfStockControlPreference": True,
}

EBAY_NOTIFICATION_PREFERENCE_TEMPLATE = {
    "MessageID": "",
    "ApplicationDeliveryPreferences": {
        "AlertEmail": "",
        "AlertEnable": "Enable",
        "ApplicationEnable": "Enable",
        "ApplicationURL": "http://%s:%d%s" % (APP_HOST_ORDERING, 
            APP_PORT_SOAP, 
            APP_EBAY_NOTIFICATION_ENDPOINT_URL),
        "DeliveryURLDetails": {
            "DeliveryURL": "http://%s:%d%s" % (APP_HOST_ORDERING, 
                APP_PORT_SOAP, 
                APP_EBAY_NOTIFICATION_ENDPOINT_URL),
            "DeliveryURLName": "default",
            "Status": "Enable",
        },
        "DeviceType": "Platform",
    },
    "UserDeliveryPreferenceArray": {
        "NotificationEnable": [
            {
                "EventEnable": "Enable",
                "EventType": "ItemSold",
            },
            {
                "EventEnable": "Enable",
                "EventType": "FixedPriceTransaction",
            },
            {
                "EventEnable": "Enable",
                "EventType": "AuctionCheckoutComplete",
            },
            {
                "EventEnable": "Enable",
                "EventType": "EndOfAuction",
            },
            {
                "EventEnable": "Enable",
                "EventType": "ItemClosed",
            },
            {
                "EventEnable": "Enable",
                "EventType": "ItemUnsold",
            },
        ],
    },
    "DeliveryURLName": "default",
}

EBAY_SHIPMENT_TEMPLATE = {
    "MessageID": "",
    "ItemID": "",
    "TransactionID": "",
    "OrderID": "",
    "FeedbackInfo": {
        "CommentText": "",
        "CommentType": "Positive",
        "TargetUser": "",
    },
    "Shipment": {
        "ShipmentTrackingDetails": {
            "ShipmentTrackingNumber": "",
            "ShippingCarrierUsed": "", # only allowed: letters (a-z, A-Z), numbers (0-9), space, and dash (-)
        },
    },
}

EBAY_MEMBER_MESSAGE_TEMPLATE = {
    "MessageID": "",
    "ItemID": "",
    "MemberMessage": {
        "Subject": "",
        "Body": "",
        "QuestionType": "",
        "RecipientID": "",
    },
}

EBAY_ADVANCED_FIND_ITEMS_TEMPLATE = {
    "keywords": "",
    "descriptionSearch": True,
    "itemFilter": [
        # {
        #     "name": "Condition",
        #     "value": "Used"
        # },
        {
            "name": "LocatedIn",
            "value": "US"
        },
    ],
    "sortOrder": "BestMatch",
    "paginationInput": {
        "entriesPerPage": 50,
        "pageNumber": 1,
    },
}

EBAY_GET_SUGGESTED_CATEGORIES_TEMPLATE = {
    "MessageID": "",
    "Query": "",
}

EBAY_GET_SELLER_LIST_TEMPLATE = {
    "MessageID": "",
    "GranularityLevel": "Coarse",
    "Pagination": {
        "EntriesPerPage": 200,
        "PageNumber": 1,
    },
}

EBAY_GET_SELLER_LIST_TEMPLATE = {
    "MessageID": "",
    "GranularityLevel": "Coarse",
    "Pagination": {
        "EntriesPerPage": 200,
        "PageNumber": 1,
    },
}

EBAY_GET_ITEM = {
    "MessageID": "",
    "ItemID": "",
}

EBAY_GET_CATEGORIES_TEMPLATE = {
    "MessageID": "",
    "CategorySiteID": 0,
    # "LevelLimit": 0,
    # OR
    # "CategoryParent": "",
    "DetailLevel": "ReturnAll",
}

EBAY_GET_ORDERS = {
    "MessageID": "",
    "CreateTimeFrom": "",
    "CreateTimeTo": "",
    "Pagination" : {
        "EntriesPerPage": 100,
        "PageNumber": 1,
    },
    "DetailLevel": "ReturnAll",
}

EBAY_STORE_DEFAULT_POLICY_SHIPPING = """<p>All of our products come with free Standard Shipping. Handling time on our orders is 1 business day. We will ship your item out using the most efficient carrier to your area (USPS, UPS, FedEx, Lasership, etc.). Once it has been shipped out, you should be receiving it within 2 - 6 business days depends on selected delivery service on checkout. Currently, we only ship to physical addresses located within the 48 contiguous states of America. APO/FPO addresses, Alaska and Hawaii are outside of our shipping zone.</p>"""

EBAY_STORE_DEFAULT_POLICY_PAYMENT = """<p>We only accept Paypal. Credit Card Payment Acceptable through PayPal.</p>"""

EBAY_STORE_DEFAULT_POLICY_RETURN = """<p>We fully guarantee all of our items. All items are Brand new and unused. 30 days refunds - we accept returns with defective or being pre-authorized. 10 percent restocking fee may apply.  Please contact us to get an authorization and returning address before sending the item back. Please leave a note with your eBay ID along with the returned item. Buyers pay shipping fees at their own cost to return products for exchange or refund. We will be responsible for the postage of replacements sending out.</p>"""

EBAY_ITEM_DESCRIPTION_CSS = """
<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.6/flatly/bootstrap.min.css">
<style>
    a {
        color: inherit !important;
        text-decoration: none !important;
    }
    a:link,
    a:visited,
    a:hover,
    a:active,
    a:focus {
        color: inherit !important;
        text-decoration: none !important;
    }
    @media (min-width: 992px) {
        .container-fluid {
            padding-right: 0px;
            padding-left: 0px;
            margin-right: auto;
            margin-left: auto;
        }
    }
</style>
"""

EBAY_ITEM_DESCRIPTION_JS = """
<script language="JavaScript1.2">
function disabletext(e){
return false
}
function reEnable(){
return true
}
//if the browser is IE4+
document.onselectstart=new Function ("return false")
//if the browser is NS6
if (window.sidebar){
document.onmousedown=disabletext
document.onclick=reEnable
}
</script>
<script language="javascript">
function clickIE4(){
if (event.button==2){
alert(message);
return false;
}
}
function clickNS4(e){
if (document.layers||document.getElementById&&!document.all){
if (e.which==2||e.which==3){
alert(message);
return false;
}
}
}
if (document.layers){
document.captureEvents(Event.MOUSEDOWN);
document.onmousedown=clickNS4;
}
else if (document.all&&!document.getElementById){
document.onmousedown=clickIE4;
}
document.oncontextmenu=new Function("return false;")
</script>
<script>
var anchors = document.getElementsByTagName('a');
var i;
for (i=0;i<anchors.length;i++) {
anchors[i].removeAttribute('href');
}
</script>
"""

__default_description_template = """<div class="container-fluid">
    {% if title and title != ""  %}
    <h3 style="margin-top: 5px; margin-bottom: 21px;">
        {{ title }}
    </h3>
    {% endif %}
    {% if description and description != ""  %}
    <div class="panel panel-primary">
        <div class="panel-heading">Description</div>
        <div class="panel-body">
            {{ description }}
        </div>
    </div>
    {% endif %}
    {% if features and features != ""  %}
    <div class="panel panel-primary">
        <div class="panel-heading">Features</div>
        <div class="panel-body">
            {{ features }}
        </div>
    </div>
    {% endif %}
    {% if policy_shipping and policy_shipping != ""  %}
    <div class="panel panel-default">
        <div class="panel-heading">Shipping information</div>
        <div class="panel-body">
            {{ policy_shipping }}
        </div>
    </div>
    {% endif %}
    {% if policy_payment and policy_payment != ""  %}
    <div class="panel panel-default">
        <div class="panel-heading">Payment information</div>
        <div class="panel-body">
            {{ policy_payment }}
        </div>
    </div>
    {% endif %}
    {% if policy_return and policy_return != ""  %}
    <div class="panel panel-default">
        <div class="panel-heading">Return policy</div>
        <div class="panel-body">
            {{ policy_return }}
        </div>
    </div>
    {% endif %}
</div>
"""

EBAY_STORE_DEFAULT_ITEM_DESCRIPTION_TEMPLATE = """%s
%s
%s""" % (EBAY_ITEM_DESCRIPTION_CSS, __default_description_template, EBAY_ITEM_DESCRIPTION_JS)
