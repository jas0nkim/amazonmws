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
        # 	  "PictureURL": [
        # 	      "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        # 	      "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007",
        # 	  ],
        # },
        "PictureDetails": {
        	"PictureURL": []
        },
        # "StartPrice": 19.99,
        "StartPrice": 0.99,
        # "Quantity": 100,
        "Quantity": 100,


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
