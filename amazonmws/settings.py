# Application

APP_ENV = "stage"
# APP_ENV = "prod"

APP_MYSQL_HOST = "localhost"
APP_MYSQL_DATABASE = "amazonmws"
APP_MYSQL_USERNAME = "atewriteuser"
APP_MYSQL_PASSWORD = "20itSiT15"

APP_LOG_SERVER_HOST = ""
APP_LOG_SERVER_PORT = 12201

PAYPAL_EMAIL = 'oroojass-facilitator@hotmail.com' if APP_ENV == 'stage' else 'oroojass@hotmail.com'

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
AMAZON_ITEM_LINK_PREFIX = 'http://www.amazon.com/gp/product/'

AMAZON_SELLER_ID = "A2I4JVBHOAUINI" if APP_ENV == "stage" else "A2I4JVBHOAUINI"
# AMAZON_MARKETPLACE_ID = "A2EUQ1WTGCTBG2" # CA
AMAZON_MARKETPLACE_ID = "ATVPDKIKX0DER" # US


EBAY_ITEM_DEFAULT_QUANTITY = 2
EBAY_ITEM_LINK_PREFIX = 'http://cgi.sandbox.ebay.com/ws/eBayISAPI.dll?ViewItem&item=' if APP_ENV == "stage" else 'http://cgi.ebay.com/ws/eBayISAPI.dll?ViewItem&item='

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
        "PayPalEmailAddress": PAYPAL_EMAIL,
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
                "PO Box",
            ],
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
        "PayPalEmailAddress": PAYPAL_EMAIL,
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
                "PO Box",
            ],
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