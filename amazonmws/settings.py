import logging

# Application

APP_ENV = "stage"
# APP_ENV = "prod"

APP_LOG_LEVEL = logging.DEBUG if APP_ENV == 'stage' else logging.DEBUG

APP_MYSQL_HOST = "localhost"
APP_MYSQL_DATABASE = "amazonmws"
APP_MYSQL_USERNAME = "atewriteuser"
APP_MYSQL_PASSWORD = "20itSiT15"

APP_LOG_SERVER_HOST = "192.168.0.14"
APP_LOG_SERVER_PORT = 12201

APP_DEFAULT_EMAIL = "redflagitems@gmail.com"

APP_HOST = 'http://localhost:8080' if APP_ENV == 'stage' else 'http://localhost:8080'

APP_DEFAULT_WEBDRIVERWAIT_SEC = 10
APP_EBAY_NOTIFICATION_ENDPOINT_URL = "/ebay/notification/listener"

PAYPAL_ACCOUNT = 'oroojass-facilitator@hotmail.com' if APP_ENV == 'stage' else 'oroojass@hotmail.com'

# -*- coding: utf-8 -*-

# Scrapy settings for amazonmws project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'amazonmws'

SPIDER_MODULES = ['amazonmws.spiders']
NEWSPIDER_MODULE = 'amazonmws.spiders'

AMAZON_ITEM_LINK_PATTERN = r'^https?://www.amazon.com/([^/]+)/([^/]+)/([A-Z0-9]{10})(/.*$)?'
AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM = r'\._([^_]+)_\.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO = '._SX522_.'
AMAZON_ITEM_LINK_FORMAT = "http://www.amazon.com/dp/%s"
AMAZON_ITEM_OFFER_LISTING_LINK_FORMAT = "http://www.amazon.com/gp/offer-listing/%s?ie=UTF8&condition=new"

AMAZON_SELLER_ID = "A2I4JVBHOAUINI" if APP_ENV == "stage" else "A2I4JVBHOAUINI"
# AMAZON_MARKETPLACE_ID = "A2EUQ1WTGCTBG2" # CA
AMAZON_MARKETPLACE_ID = "ATVPDKIKX0DER" # US


EBAY_ITEM_DEFAULT_QUANTITY = 2
EBAY_ITEM_LINK_FORMAT = "http://www.sandbox.ebay.com/itm/%s" if APP_ENV == "stage" else "http://www.ebay.com/itm/%s"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazonmws (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazonmws.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'amazonmws.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'amazonmws.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


#
######### ebay api related settings #########
#

EBAY_TRADING_API_DOMAIN = "api.sandbox.ebay.com" if APP_ENV == "stage" else "api.ebay.com"

EBAY_ITEM_DESCRIPTION_CSS = """
<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
<style>
    * {
        font-size: small;
    }
    .panel-rfi {
        border-color: #ca361c;
    }
    .panel-rfi > .panel-heading {
        color: #fff;
        background-color: #ca361c;
        border-color: #ca361c;
        font-weight: 500;
        line-height: 1.1
    }
    .panel-rfi > .panel-heading + .panel-collapse > .panel-body {
        border-top-color: #ca361c;
    }
    .panel-rfi > .panel-heading .badge {
        color: #f5f5f5;
        background-color: #ca361c;
        font-weight: 500;
        line-height: 1.1
    }
    .panel-rfi > .panel-footer + .panel-collapse > .panel-body {
        border-bottom-color: #ca361c;
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

EBAY_UPLOAD_SITE_HOSTED_PICTURE = {
    "ExternalPictureURL": "",


    # "ExtensionInDays": 90, # !!This call is restricted to applications that have been granted permission. Contact the eBay Developers Program to request premission!!
     
    # "PictureWatermark": "",
}

EBAY_ADD_ITEM_TEMPLATE = {
    "MessageID": "",
    "Item": {
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


        "AutoPay": True,
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
        "PayPalEmailAddress": PAYPAL_ACCOUNT,
        "PostCheckoutExperienceEnabled": True,
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
            "ExcludeShipToLocation": [
                "Alaska/Hawaii",
                "US Protectorates",
                "APO/FPO",
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
                    "ShippingService": "UPS2ndDay",
                    "ShippingServiceCost": 1.99,
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

EBAY_ADD_ITEM_TEMPLATE['Item']['AutoPay'] = False if APP_ENV == 'stage' else True


EBAY_REVISE_ITEM_TEMPLATE = {
    "MessageID": "",
    "Item": {
        "ItemID": "",
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
        "StartPrice": 0.99,
        "Quantity": EBAY_ITEM_DEFAULT_QUANTITY,


        "AutoPay": True,
        "CategoryBasedAttributesPrefill": True,
        "CategoryMappingAllowed": True,
        "ConditionID": 1000,
        "Country": "US",
        "DescriptionReviseMode": "Replace",
        "DispatchTimeMax": 2,
        "HitCounter": "HiddenStyle", # could be changed later
        "IncludeRecommendations": True,
        "InventoryTrackingMethod": "ItemID",
        "ListingDuration": "GTC", # Good 'Til Cancelled
        "ListingType": "FixedPriceItem",
        "LiveAuction": False,
        "Location": "Nationwide, United States",
        "PaymentMethods": "PayPal",
        "PayPalEmailAddress": PAYPAL_ACCOUNT,
        "PostCheckoutExperienceEnabled": True,
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
        # "SellerInventoryID": string # need to revisit
        # "SellerProfiles": SellerProfilesType # need to revisit
        "ShippingDetails": {
            "ExcludeShipToLocation": [
                "Alaska/Hawaii",
                "US Protectorates",
                "APO/FPO",
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
                    "ShippingService": "UPS2ndDay",
                    "ShippingServiceCost": 1.99,
                    "ShippingServiceAdditionalCost": 0.00,
                },
            ],
        },
        "ShipToLocations": "US",
        # "Storefront": StorefrontType # need to revisit
        # "ThirdPartyCheckout": boolean # need to revisit
        # "ThirdPartyCheckoutIntegration": boolean # need to revisit
        # "Variations": VariationsType # need to revisit
    },
}

EBAY_REVISE_ITEM_TEMPLATE['Item']['AutoPay'] = False if APP_ENV == 'stage' else True


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
        "AlertEnable": "Enable",
        "AlertEmail": "mailto://" + APP_DEFAULT_EMAIL,
        "ApplicationEnable": "Enable",
        "ApplicationURL": APP_HOST + APP_EBAY_NOTIFICATION_ENDPOINT_URL,
        "DeviceType": "Platform",
    },
}

EBAY_STORE_DEFAULT_POLICY_SHIPPING = """<p>All of our products come with free Standard Shipping. Handling time on our orders is between 1-2 business days. We will ship your item out using the most efficient carrier to your area (USPS, UPS, FedEx, Lasership, etc.). Once it has been shipped out, you should be receiving it within 2 - 6 business days depends on selected delivery service on checkout. Currently, we only ship to physical addresses located within the 48 contiguous states of America. APO/FPO addresses, Alaska and Hawaii are outside of our shipping zone.</p>"""

EBAY_STORE_DEFAULT_POLICY_PAYMENT = """<p>We only accept Paypal. Credit Card Payment Acceptable through PayPal.</p>"""

EBAY_STORE_DEFAULT_POLICY_RETURN = """<p>We fully guarantee all of our items. All items are Brand new and unused. 14 days refunds - we accept returns with defective or being pre-authorized. 10 percent restocking fee may apply.  Please contact us to get an authorization and returning address before sending the item back. Please leave a note with your eBay ID along with the returned item. Buyers pay shipping fees at their own cost to return products for exchange or refund. We will be responsible for the postage of replacements sending out.</p>"""
