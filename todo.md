# Plans

### Week of 2018-06-10 - 2018-06-23
    - multiple quantity listing / multiple quantity ordering
    - business idea
        - group purchase for discount
        - option for the group purchase (if meet the time line, you may get group purchase price)
    - develop ebay sdk Inventory API
        https://developer.ebay.com/api-docs/sell/inventory/static/overview.html
    - db table:
        - ebay_inventory_locations
            - merchant_location_key
            - address_country (US)
            - status
        - ebay_inventory_items
            - sku (prefix AZN- + ASIN)
            - ship_to_location_availability_quantity
            - [ condition (NEW) ]
            - title
            - description
            - aspects (includes: Brand, MPN, UPC)
            - image_urls (use Amazon urls - no UploadSiteHostedPictures)
            - inventory_item_group_keys (array)
        - ebay_inventory_item_groups
            - inventory_item_group_key
            - description
            - common_aspects
            - image_urls
            - variant_skus (array)
            - aspects_image_varies_by (array)
            - varies_by_specifications (name, values)
        - ebay_offers
            - offer_id
            - listing_id
            - available_quantity
            - ebay_category_id
            - payment_policy_id
            - return_policy_id
            - fulfillment_policy_id
            - merchant_location_key
            - original_retail_price
            - original_retail_price_currency
            - price
            - price_currency
            - quantity_limit_per_buyer
            - store_category_names (array)
            - sku
            - marketplace_id
            - listing_format (FIXED_PRICE)
            - is_published
        - [ ebay_offer_listings ]
            - listing_id
            - ebay_offer_id
            - inventory_item_group_key
    - build django models for new tables
    - build SDK for InventoryLocation
        - createInventoryLocation
        - getInventoryLocations
        - (enableInventoryLocation, disableInventoryLocation, deleteInventoryLocation)
    - build SDK for InventoryItem, InventoryItemGroup, Offer

### Week of 2018-05-27 - 2018-06-02
    - eBay API - prepare PBSE (Product-Based Shopping Experience)
        https://developer.ebay.com/api-docs/sell/static/inventory/pbse_playbook_intro.html

### Week of 2018-05-13 - 2018-05-19
    - multiple quantity listing / multiple quantity ordering
    - improve sales report
        - how may items sales/canceled

### Week of 2018-03-25 - 2018-03-31
    - fix scraping issue - not very accurate
        - 1. update packages
        - 2. test and find errors

### Week of 2018-01-21 - 2018-01-27
    - handle/fix ebay trading api errors
    - list more items
    - contact FBA vendors
        - 1. find list of fasion FBA vendors
        - 2. request email
        - 3. get list manually first -> eventually setup an electronic ordering tool
        http://docs.developer.amazonservices.com/en_CA/fba_outbound/FBAOutbound_CreateFulfillmentOrder.html

### Week of 2018-01-07 - 2018-01-13

- update db server
    1. setup new linode for db server
    2. shutdown all servers
    3. backup/dump current db
    4. restore the dump to the new linode db server
    5. change config for new db server ip address/connection
    6. testing with ateordr1 server
    7. run ateapp1 and ateapp2 servers
- contact FBA vendors
    - 1. find list of fasion FBA vendors
    - 2. request email
    - 3. get list manually first -> eventually setup an electronic ordering tool
    http://docs.developer.amazonservices.com/en_CA/fba_outbound/FBAOutbound_CreateFulfillmentOrder.html

### Week of 2017-12-03 - 2017-12-09

- TrustPilot (https://uk.trustpilot.com/) - online shop review site

### Week of 2017-11-19 - 2017-11-25

- upgrade linode server
    - old ($145 /month):
        ateapp-server : Linode 8GB (ubuntu 14.04) - $40 /month
        ateordr-server : Linode 4GB (ubuntu 14.04) - $20 /month
        atedb-server : Linode 12GB (ubuntu 14.04) - $80 /month
        ateaff-server : Linode 1GB (ubuntu 16.04) - $5 /month
    - new - plan 1 ($185 /month):
        ateapp1-server : Linode 8GB (ubuntu 16.04) - $40 /month
        ateapp2-server : Linode 8GB (ubuntu 16.04) - $40 /month
        ateordr-server : Linode 4GB (ubuntu 16.04) - $20 /month
        atedb-server : Linode 8GB (ubuntu 16.04)
                + 300GB Block Storage (for mysql data)
                + 150GB Block Storage (for db backup)
                - $40 /month + $30 /month + $15 /month
    - new - plan 2 ($180 /month):
        ateapp1-server : Linode 8GB (ubuntu 16.04) - $40 /month
        ateapp2-server : Linode 8GB (ubuntu 16.04) - $40 /month
        ateordr1-server : Linode 4GB (ubuntu 16.04) - $20 /month
        atedb1-server : Linode 24GB (ubuntu 16.04 & MySQL 5.7) - $80 /month


        https://www.linode.com/docs/platform/how-to-use-block-storage-with-your-linode

        https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04


### Week of 2017-10-29 - 2017-11-11

- upgrade dropshipping business
    - change resourcing
        - Amazon -> Vendors
    - change selling channel
        - eBay -> own website (shopify)


### Week of 2017-07-23 - 2017-07-29

- Develop Amazon MWS application
    - get product information
        - title
        - description
        - price
        - quantity
        - pictures
        - and so on...
    - get inventory
    - order
    - cancel
    - track
    - return


### Week of 2017-07-09 - 2017-07-15

- Empire Flippers (https://empireflippers.com) - Buy & Sell Website businesses (dropshipping sites as well)
- Amazon Affiliate Program (integrate with automationj ordering - instead of ebates.com)
    - join Amazon Affiliate Program (new amazon account affiliate only)
    - setup a separate webserver (Linode 1GB - $5 per month), and create an affiliate link from there

### Week of 2017-07-02 - 2017-07-08

- New store (w/ Shopify) plan (updated)
    - Affliate (sharing affliate)
    - scrape amazon items, walmart items, ...
    - communication data
    - quality description
    - shopify or woocommerce

- New store (w/ Shopify) plan (alternative)
    - selling Amazon product legally - via FBA Multi-channel
    - eyelashes
    - approach Amazon FBA sellers (clothing)

### Week of 2017-06-25 - 2017-07-01

- New store (w/ Shopify) plan
    - URVIFASHION.com
    - mission statement
        - fast shipping
        - quality products
        - accurate product description
        - high interaction with customers
    - 1st phase
        - products
            - 1000-3000 products
        - marketing
            - email marketing (ebay customers)
        - sales
            - average sold price ($30 per item), margin 15% ($4.50 per item)
            - 5-15 items per day (150-450 items per month)
            - profit ($657-$2025 per month)
        - team members
            - 1 people (myself)
    - 2nd phase
        - products
            - 5000-10000 products
        - marketing
            - email marketing + facebook+instagram marketing
        - sales
            - average sold price ($30 per item), margin 15% ($4.50 per item)
            - 25-50 items per day (750-1500 items per month)
            - profit ($3375-$6750 per month)
        - team members
            - 2 people
                - myself
                - email/comment customer support

### Week of 2017-06-25 - 2017-07-01

- diffbot.com (scrapinghub alternative)

### Week of 2017-05-14 - 2017-05-27

- best sellers (automationj) - top 100
    - on screen columns (options last 1 year, last 3 months, last 1 month)
        - rank
        - item title (amazon title, ebay item link, amazon item link)
        - brand
        - category (amazon category)
        - total sold (, and sold ebay provides as well)
        - number of sold in last 3 months
        - number of sold in last 1 months
        - listed on ebay since
        - total returns (return rates)
        - total cancels (cancel rates)

### Week of 2017-05-07 - 2017-05-13

- integrate Shopify
    - features
        - listing new products (with variations, pictures)
            - product_type: the last level (leaf) of its amazon category
            - vendor: brand
            - tags: category tree
            - collections - SmartCollection - implement later
        - google analysis
        - modify existing products (with variations, pictures)
        - repricing existing products (with variations, pictures)
        - add Apps
            - product review (shopify)
                - https://help.shopify.com/manual/apps/apps-by-shopify/product-reviews
            - reward point (sweet tooth - https://www.sweettoothrewards.com)
                - https://www.shopify.ca/blog/117007237-how-to-start-a-loyalty-program-that-keeps-customers-coming-back
        - pricing...
            - less price than eBay's (5%)
    - marketing
        - email marketing to all ebay customers
        - instagram (facebook)
            - ads best sellers (most sold items)
        - pinterest
            - ads best sellers (most sold items)
    - Wish.com - shopify has Wish app on their sales channel. let shopify manage Wish for now...
- ** Bigger Plan **
    - build a platform (infrastructure) for dropshipping products from Korea to US (North America)
        - Manufactures/OEMs in Korea
        - Prep business in Korea (for FBA)
        - Sellers in US/Canada
        - connect all together within Software/Platform
    - Prep products for FBA
    - learn more about dropship from dropship community
        - dropshipping canada - http://dropshippingcanada.ca/
        - dropship life style

### Week of 2017-04-23 - 2017-04-29

- integrate Shopify
    - Wish.com - shopify has Wish app on their sales channel. let shopify manage Wish for now...
- ** Bigger Plan **
    - build a platform (infrastructure) for dropshipping products from Korea to US (North America)
        - Manufactures/OEMs in Korea
        - Prep business in Korea (for FBA)
        - Sellers in US/Canada
        - connect all together within Software/Platform
    - Prep products for FBA
    - learn more about dropship from dropship community
        - dropshipping canada - http://dropshippingcanada.ca/
        - dropship life style

### Week of 2017-04-09 - 2017-04-22

- update python dependencies
- integrate Ebates.com
- integrate Shopify
    - Wish.com - shopify has Wish app on their sales channel. let shopify manage Wish for now...
- (postponed) mobile ordering automation
    - automationj: Extensions for Firefox for Android
    - port existing chrome extension to a FireFix extentsion for Android
    - ordering page only

### Week of 2017-03-19 - 2017-03-25

- dropkickit - http://www.dropkickit.com/
- dropshiplifestyle
- dropshipping Canada - http://dropshippingcanada.ca/

- excel date format conversion for paypal csv
    - DATE = TEXT(DATE(RIGHT(A2, 4),LEFT(A2, SEARCH("/", A2) - 1),MID(A2, SEARCH("/", A2)+1, LEN(A2)-SEARCH("/", A2)-5)), "dd/mm/yyyy")
        - or change date format from LibreOffice Calc
    - DESC-GROSS ="["&E2&"] "&D2&" - "&L2&" - (Trans ID: "&J2&" - Ref ID: "&R2&")"
        - ="["&D2&"] "&C2&" - "&K2&" - (Trans ID: "&I2&" - Ref ID: "&Q2&")"
    - DESC-FEE ="["&E2&"] PayPal fee - (Trans ID: "&J2&" - Ref ID: "&R2&")"
        - ="["&D2&"] PayPal fee - (Trans ID: "&I2&" - Ref ID: "&Q2&")"

### Week of 2017-03-05 - 2017-03-11

- FBA Prep Service in Korea
- The Ultimate Online Store List
    - https://forums.soompi.com/en/topic/185075-the-ultimate-online-store-list/
- tqoon.com - 해외직판 지원서비스업체
- US sites you can buy Korean products (https://www.bustle.com/articles/103274-where-to-buy-korean-beauty-products-online-if-you-dont-live-anywhere-near-their-country-of)
    - Soko Glam (https://sokoglam.com)
        - https://www.bloomberg.com/news/articles/2015-08-11/beauty-without-borders-as-south-korean-products-sell-in-america
        - I love this website because it is so easy to navigate! Everything is laid out in such a crisp, clean fashion that you'll be able to find everything with ease. This website might not have the largest selection of products, but it does sell some of South Korea's cult favorites. It's completely worth the browse.
    - Yes Style (http://www.yesstyle.ca/en/home.html) - a yesasis.com company
        - https://forums.soompi.com/en/topic/189238-yesstyle-asian-clothes-on-ebay/
        - Talk about a selection! YesStyle.com hosts thousands of products and brands that will keep you online shopping for hours. You've been warned.
    - Peach & Lily (https://www.peachandlily.com/)
        - Looking for Korean skin care options? This is the site for you. The website categorizes each product to fit a specific skin care issue. It makes looking for products super simple and easy.
    - Memebox (https://us.memebox.com/)
        - Now, this website is just plain adorable. It's similar to Western beauty box brands such as Birchbox and Ipsy, but with all Korean products. It's a great way to test out samples before you commit to ordering full size — which you can do right on their website as well.
    - Sasa (http://us.sasa.com/SasaWeb/eng/sasa/home.jsp)
        - This is the first website that I have ever visited when I began my love-affiar with Korean beauty. It's not the easiest to navigate, but it has an amazing selection of products to choose from.
    - KollectionK (https://kollectionk.com/)
        - KolletionK is a great website for those looking for something a little more user-friendly. With loads of brands and products to choose from, you won't get frustrated looking for products on this website.

- retrieve & store shipping label for ebay order returns
    - https://developer.ebay.com/Devzone/post-order/post-order_v2_return-returnId_get_shipping_label__get.html

### Week of 2017-02-12 - 2017-02-18

- amazon order returns
    - db table:
        - amazon_order_returns
            - id
            - amazon_account_id
            - order_id
            - asin
            - return_id
            - ebay_return_id
            - quantity
            - refunded_amount
            - carrier
            - tracking_number
            - rma
            - status (initiated, shipping_label_issued, returned, refunded, closed_wo_refund, canceled)
            - returned_time
            - refunded_time
            - created_at
            - updated_at

### Week of 2017-02-19 - 2017-02-25

- ebay order returns
    - db table:
        - ebay_order_returns
            - id
            - ebay_store_id
            - return_id
            - transaction_id
            - item_id
            - quantity
            - buyer_username
            - est_refund_amount
            - act_refund_amount
            - reason
            - comments
            - carrier
            - tracking_number
            - rma
            - status
            - state
            - creation_time
            - raw_data
            - created_at
            - updated_at

- shipping label link format
    - https://www.amazon.com/returns/label/711548a9-1eb9-4fad-a232-c571d0040e0f?printerFriendly=1

### Week of 2017-01-22 - 2017-01-28

- continue aliexpress listing

### Week of 2017-01-15 - 2017-01-21

- fix run_reviser_wo_crawl.py
    - need to scrape before run reviser... ended bunch of good listings...
- fix popularity levels
    - change to 10 levels (from current 3 levels)
- continue aliexpress listing

### Week of 2017-01-01 - 2017-01-14

- fix ebay ReviseFixedPriceItemRequest errors
    - ERROR: ReviseFixedPriceItem: Class: RequestError, Severity: Error, Code: 21916603, Variation specifics cannot be changed Variation specifics cannot be changed in restricted revise, Class: RequestError, Severity: Error, Code: 21916587, Missing name in name-value list. Missing name in the variation specifics or variation specifics set.
        - end all ebay items have this error
    - ERROR: ReviseFixedPriceItem: Class: RequestError, Severity: Error, Code: 20004, A mixture of Self Hosted and EPS pictures are not allowed. A mixture of Self Hosted and EPS pictures are not allowed., Class: RequestError, Severity: Error, Code: 21916664, Variation Specifics Mismatch. Variation Specifics provided does not match with the variation specifics of the variations on the item., Class: RequestError, Severity: Error, Code: 21916587, Missing name in name-value list. Missing name in the variation specifics or variation specifics set.
        - ebay's fault. end all ebay items have this error
        - ref: http://ssc.channeladvisor.com/forums/sales-channels/marketplaces/ebay-error-message-mixture-self-hosted-and-eps-pictures-are-not-a
- fix repricing
    - sync ebay item first before repricing each items
    - apply individual repricing in case any ebay api error response occurres
- continue aliexpress listing

### Week of 2016-12-18 - 2016-12-31

- aliexpress listing
    0) db tables:
        - aliexpress_stores
            - id
            - store_id
            - store_name
            - company_id
            - owner_member_id
            - store_location
            - store_opened_since # date
            - deliveryguarantee_days
            - return_policy
            - is_topratedseller
            - has_buyerprotection
            - created_by
            - updated_by
        - aliexpress_store_feedbacks
            - id
            - store_id
            - feedback_score
            - feedback_percentage
        - aliexpress_store_feedbacks_detailed
            - id
            - store_id
            - itemasdescribed_score
            - itemasdescribed_ratings
            - itemasdescribed_percent
            - communication_score
            - communication_ratings
            - communication_percent
            - shippingspeed_score
            - shippingspeed_ratings
            - shippingspeed_percent
        - aliexpress_items
            - id
            - alxid
            - url
            - store_id
            - store_name
            - store_location
            - store_opened_since # date
            - category_id
            - category_name
            - category # category route i.e. ABCD > EFGH > IJKL
            - title
            - market_price # will be None if there are skus
            - price # will be None if there are skus
            - quantity # will be None if there are skus
            - specifications # json string
            - pictures # json string
            - review_count
            - review_rating
            - orders
            - status
            - created_by
            - updated_by
        - aliexpress_item_descriptions
            - id
            - alixid
            - description
            - created_by
            - updated_by
        - aliexpress_item_skus
            - id
            - alxid
            - sku # combination of actual two sku ids
            - market_price
            - price
            - quantity
            - specifics # json string - similar as amazon_items.variation_specifics
            - pictures # json string
            - bulk_price
            - bulk_order
            - raw_data # json string
            - status
            - created_by
            - updated_by
        - aliexpress_item_shippings
            - id
            - alxid
            - country_code
            - has_epacket
            - epacket_cost
            - epacket_estimated_delivery_time_min
            - epacket_estimated_delivery_time_max
            - epacket_tracking # boolean
            - all_options # json string
            - created_by
            - updated_by
        - aliexpress_item_apparels
            - id
            - alxid
            - size_chart # json string
            - created_at
            - updated_at
        - aliexpress_categories
            - id
            - category_id
            - category_name
            - parent_category_id
            - parent_category_name
            - root_category_id
            - root_category_name
            - is_leaf
            - created_at
            - updated_at
        - alx_to_ebay_category_maps (need to improve near future)
            - id
            - aliexpress_category # category route i.e. ABCD > EFGH > IJKL
            - ebay_category_id
            - ebay_category_name
            - created_at
            - updated_at
    1) aliexpress item/store scraping + listing to ebay
    2) aliexpress ordering automation
    3) update backend to support both Amazon and Aliexpress sourcing
- ordering frontend update
    - add charts on sales report screen (http://www.chartjs.org/)

### Week of 2016-12-04 - 2016-12-17

- improve eBay Store Categories - Fashion (Clothing, Shoes & Jewelry) focused for URVI only
    - Women's Fashion
        - Clothing
            - Dresses
            - Tops & Tees
            - ...
        - Shoes
        - Jewelry
        - ...
    - Men's Fashion
    - Girls' Fashion
    - Boys' Fasion
    - Other Fashions
    - Others

### Week of 2016-11-27 - 2016-12-03

- improve eBay Store Categories - Fashion (Clothing, Shoes & Jewelry) focused for URVI only
    - Women
        - Clothing
            - Dresses
            - Tops & Tees
            - ...
        - Shoes
        - Jewelry
        - ...
    - Men
    - Girls
    - Boys
    - Other Fashions
    - Others
- fix ebay item picture uploading function (ebay_pictures)
	- ebay cleans its EPS server
    - temp. solution made
        - eventually need to use image hashing technique to check placeholder image or not from the image url
- ebids/asins/status to remove (slow/error items)
"282205167541","B0029JI0KW","1"
"282193557662","B01HI7ES5K","1"
"282193557786","B01HMCXXLG","1"
"282193569665","B014XDLINC","1"
"282193571588","B01IQLHFBG","1"
"282193576701","B018G96SHU","1"
"282193579094","B019O66TR8","1"
"282193580571","B00O7A8Z2E","1"
"282193587057","B014UIGW9K","1"
"282193599826","B01GPQ7YCO","1"
"282193603889","B01AWQ69HY","1"
"282193603988","B01L322U1U","1"
"282201407758","B0006V4GLM","1"
"282201474107","B0006V4IC4","1"
"282201477386","B00W3G6NWS","1"
"282201592454","B01IMX2YRI","1"
"282201641245","B019QF1XW8","1"
"282201653146","B01KZNTJOE","1"
"282201653261","B00VIG23XC","1"
"282201662655","B01EWSJYKW","1"
"282201671615","B00NAPZV60","1"
"282201695596","B01LW71ZAQ","1"
"282201714050","B00DOOFLOO","1"
"282201746687","B01DTUEWQU","1"
"282201751815","B01JWANQH2","1"
"282201763639","B0035GEL7Y","1"
"282201765399","B0126UBCGM","1"
"282201770089","B012MZY81W","1"
"282201776313","B007ATNTT8","1"
"282201789418","B00XJJ07T8","1"
"282201801469","B01LN7YY0K","1"
"282201821166","B01DCKBAQC","1"
"282201845806","B00XBFI3AU","1"
"282201853654","B004I73P6C","1"
"282201864923","B00538HC0K","1"
"282201873631","B015PFMTVM","1"
"282201884094","B01H1A8F8A","1"
"282201900816","B00O4CQHS4","1"
"282201913524","B00S9KG340","1"
"282201914112","B00CVQOKNE","1"
"282201918184","B00O27ZVF6","1"
"282201920166","B014WKPRYM","1"
"282201954774","B014HDPCWQ","1"
"282201981987","B00A7NJBPU","1"
"282202006143","B015E03BSI","1"
"282202015703","B019K5594W","1"
"282202058335","B01DTUKVBA","1"
"282202087088","B00IW134DY","1"
"282204694639","B01B5DL8LA","1"
"282204697413","B0084ZYEI2","1"
"282204714611","B00UBA8AEC","1"
"282204737244","B00YRKRPTI","1"
"282204745482","B004I74GRE","1"
"282204818256","B01BG5LYH0","1"
"282204831265","B0045ZRI88","1"
"282204902546","B00GKGULI4","1"
"282204903178","B0161SS0WO","1"
"282204907437","B002QN88HQ","1"
"282204944348","B013YX3MYA","1"
"282204946191","B00KJJNTK0","1"
"282205033288","B01DUTWDPC","1"
"282205033751","B007X44124","1"
"282205076886","B0101E078O","1"
"282205081929","B00BXP2E00","1"
"282205083047","B00GGINWR8","1"
"282205095776","B004I74BYM","1"
"282205096171","B00IA1U9F2","1"
"282205147116","B015GFCAEM","1"
"282205147436","B002XEDRZQ","1"
"282205155988","B00S18Z8QO","1"
"282205185449","B00BMVIPRG","1"
"282205455258","B017J88EC6","1"
"282205593197","B00SIYY4V6","1"
"282205594524","B01A1FNU4Q","1"
"282205624461","B01CNF2ZWK","1"
"282205663966","B01CPSPF3Q","1"
"282205678612","B01FKHSZF4","1"
"282205679374","B00KR9SLRS","1"
"282205685420","B01CTFX1R2","1"
"282205696044","B011LP6S4Y","1"
"282205798948","B003VP3T36","1"
"282205841823","B012LEA2DW","1"
"282205890184","B004I74CJ6","1"
"282205919989","B015J7ESRY","1"
"282206013576","B004D6461Q","1"
"282206023916","B00FG9R4Q8","1"
"282206048458","B00KNWU7AS","1"
"282206051087","B017BMY3SE","1"
"282206053923","B00DRG836W","1"
"282236401318","B00UY0VIUC","1"
"282241031506","B00IST9K92","1"
"282241432957","B00IM40Z6U","1"
"282242593680","B00L3JDYI2","1"
"282242597698","B01KY9BTX8","1"
"282242599350","B01ABTIXGW","1"
"282242613769","B01DPSQFZW","1"
"282243473364","B00U3792OU","1"
"282243517263","B01IP6WQ4S","1"
"282243528011","B00EZI3PSM","1"
"282243550523","B00OYXPK40","1"
"282243553347","B00FKK7A4O","1"
"282243620122","B017SLX9HO","1"
"282243634930","B01M68KNB2","1"
"282245244779","B014V1G548","1"
"282246137889","B01M5J00FR","1"
"282246179861","B01MG2C505","1"
"282246516071","B01LWMJ51M","1"
"282246875114","B0195L0MH0","1"
"282246876636","B01FRGDOGI","1"
"282246881523","B01EM8H5IA","1"
"282246897181","B019X15G0A","1"
"282246902455","B01CPZR75I","1"
"282246903001","B01DWPWZWA","1"
"282246906695","B01BUMKBK0","1"
"282246947629","B01M9FSQTO","1"
"282246952594","B01CTY5PPO","1"
"282246983219","B01HFO3E7Y","1"
"282246986038","B01LY376LK","1"
"282246990086","B01HSMR064","1"
"282246990344","B01KZO7JQI","1"
"282246990680","B019K5988K","1"
"282246998559","B0188RY4PS","1"
"282246999604","B01EIQFVF0","1"
"282247024806","B01CPZR90Q","1"
"282247031832","B00GRWDJ94","1"
"282247032906","B01F600B5M","1"
"282247033014","B01DN1VEKC","1"
"282247040318","B01945CIBK","1"
"282247047122","B01HN4HYWM","1"
"282247063439","B018IS4B9Q","1"
"282247105928","B01CFIW9MG","1"
"282247106855","B01C7FNECQ","1"
"282247193382","B00MXBQMSS","1"
"282248081375","B01FYVIP7Y","1"
"282248082997","B01KO2X4SS","1"
"282248083382","B01GDN7QH2","1"
"282248083651","B018S30FJ6","1"
"282248085627","B00N3XC8KG","1"
"282248086815","B015ZTQ3OM","1"
"282248088923","B01GHN53Q4","1"
"282248090631","B016ZKWOV6","1"
"282248091012","B01ID3UKBO","1"
"282248097636","B01M160A77","1"
"282248098504","B01LYUBV5U","1"
"282248101265","B01H3K0PH2","1"
"282248101509","B01CFSJ4Y2","1"
"282248101752","B01LVZ1838","1"
"282248103707","B01K1C6JTM","1"
"282248117175","B01HCFF4ZG","1"
"282248118918","B0153MIWEU","1"
"282248122101","B01IPUBP8M","1"
"282248127168","B00T5V2Z8K","1"
"282248131822","B01APMPQYM","1"
"282248143005","B00LWQB5KU","1"
"282248149253","B01M0PVWQT","1"
"282248152688","B01CCO17MQ","1"
"282248154275","B01FAM9LYS","1"
"282248161801","B00OOROFJ2","1"
"282248170538","B01HCVNDPS","1"
"282248172149","B018XO2HHS","1"
"282248181965","B00571PY7Q","1"
"282248749321","B01LXHIGRV","1"
"282248759798","B01LQ817HO","1"
"282248846256","B01M0BRXN2","1"
"282248846509","B003IWYN9G","1"
"282248847428","B01LY3DVM4","1"
"282248855979","B015JQL012","1"
"282248860264","B01LZFWZXU","1"
"282248860516","B001XUS800","1"
"282248868894","B00XTQQ92A","1"
"282248875810","B008DBK67U","1"
"282248884459","B01LY7334G","1"
"282248885556","B00W0VRDDE","1"
"282248886298","B01LEEPHBC","1"
"282248887469","B00WYN85M6","1"
"282248888197","B011NTW44Q","1"
"282248888906","B01LBZLJ4S","1"
"282248889511","B00PYT42JM","1"
"282248909693","B00IEYW1SI","1"
"282248912432","B00UYXIRBC","1"
"282248929493","B01FOKV71Q","1"
"282248937091","B00HT1SLSQ","1"
"282248941387","B00XP4PF2Q","1"
"282248980397","B00XA104B6","1"
"282249012353","B00XTQR26M","1"
"282249019847","B0161ZUZL6","1"
"282249031126","B000R9WYZ8","1"
"282249052637","B00D4KHZ1U","1"
"282249057053","B00AJJIGGM","1"
"282249487448","B00WTDNO8Q","1"
"282249510733","B002NEGBFO","1"
"282249511612","B013GZ23W8","1"
"282249602936","B010MO5GOI","1"
"282249617336","B00R4QHJXY","1"
"282249617555","B0018SOJBE","1"
"282249618336","B01LE268OO","1"
"282249618679","B01J5155RM","1"
"282249625788","B011LO5GBQ","1"
"282249630321","B01IUTXS10","1"
"282249644683","B01LX5PG8D","1"
"282249650242","B01IRURV56","1"
"282249651936","B00HSZNP2U","1"
"282249652748","B015EG2AQG","1"
"282249654314","B00I8SAJD4","1"
"282249657624","B01INYEXRA","1"
"282249657742","B00605L7V0","1"
"282249658009","B00LGJHA02","1"
"282249658160","B00TT6R0YA","1"
"282249658211","B00PV0HPAM","1"
"282249658435","B00R426J0W","1"
"282249658497","B00NPXWX8Q","1"
"282249658826","B00EXV324I","1"
"282249658874","B01BPH5OKC","1"
"282249659178","B01FXEH07S","1"
"282249659708","B00MPYBCCE","1"
"282249659988","B00JFTWP2S","1"
"282249660112","B00KIMBVEE","1"
"282249665428","B01GYZIGD2","1"
"282249666191","B00E80R22C","1"
"282249666392","B00JEG0LSC","1"
"282249667448","B0018005N8","1"
"282249667851","B00L01K5DA","1"
"282249671055","B00KSJJ2L6","1"
"282249671608","B018SXMN2I","1"
"282249692466","B00HVFD72U","1"
"282249695933","B00B2IG7RY","1"
"282249697325","B01FX9VALA","1"
"282249698984","B01CQIXUSW","1"
"282249699922","B00QANGRDU","1"
"282249703384","B00XUX2WUU","1"
"282249704036","B00GOY9NA4","1"
"282249705115","B00WDPDH9G","1"
"282249720114","B01CQP5SG2","1"
"282249724567","B00TDKIPOQ","1"
"282249724740","B01INXPJGA","1"
"282249728869","B00HYZ4KY6","1"
"282250180353","B01LDAE9H0","1"
"282252437289","B01BU0NIGG","1"
"282252532250","B01DKX8UZU","1"

### Week of 2016-11-06 - 2016-11-26

- Aliexpress Drop Shipping
	1) build scraper
        - aliexpress_stores # obtain data by selenium... (ajax involved) - update this once a week
            - id
            - store_id
            - store_name
            - company_id
            - owner_member_id
            - store_location
            - store_opened_since # date
            - deliveryguarantee_days
            - return_policy
            - is_topratedseller
            - has_buyerprotection
            - created_by
            - updated_by
        - aliexpress_stores_feedbacks
            - id
            - store_id
            - feedback_score
            - feedback_percentage
        - aliexpress_stores_feedback_detailed
            - id
            - store_id
            - itemasdescribed_score
            - itemasdescribed_ratings
            - itemasdescribed_percent
            - communication_score
            - communication_ratings
            - communication_percent
            - shippingspeed_score
            - shippingspeed_ratings
            - shippingspeed_percent
        - aliexpress_items
            - id
            - alxid
            - url
            - store_id
            - store_name
            - store_location
            - store_opened_since # date
            - category_id
            - category_name
            - category # category route i.e. ABCD > EFGH > IJKL
            - title
            - market_price # will be None if there are skus
            - price # will be None if there are skus
            - quantity # will be None if there are skus
            - description
            - specifications # json string
            - review_count
            - review_rating
            - orders
            - pictures # json string
            - created_by
            - updated_by
        - aliexpress_item_skus
            - id
            - alxid
            - sku # combination of actual two sku ids
            - market_price
            - price
            - quantity
            - specifics # json string - similar as amazon_items.variation_specifics
            - pictures # json string
            - bulk_price
            - bulk_order
            - raw_data # json string
            - status
            - created_by
            - updated_by
        - aliexpress_item_shippings
            - id
            - alxid
            - country_code
            - has_epacket
            - epacket_cost
            - epacket_estimated_delivery_time_min
            - epacket_estimated_delivery_time_max
            - epacket_tracking # boolean
            - all_options # json string
            - created_by
            - updated_by
        - aliexpress_item_apparels
            - id
            - alxid
            - size_chart
            - created_at
            - updated_at
        - aliexpress_categories
            - id
            - category_id
            - category_name
            - parent_category_id
            - parent_category_name
            - root_category_id
            - root_category_name
            - is_leaf
            - created_at
            - updated_at
	2) alx_to_ebay_category_maps (rename a_to_e_category_maps to amz_to_ebay_category_maps)
    4) automate ordering, tracking number
	3) update backend to support both Amazon and Aliexpress sourcing
		- ebay_items.asin => ebay_items.sku (use AMZ_ and ALX_ prefixes)
- Aliexpress (lightinthebox.com) sourcing!!
	- check Seller feedbacks! very important!
	- Worldwide shipping!!
	- Amazon.com sourcing - US only
	- Amazon.co.uk sourcing - Euro only (need to research more)
	- Aliexpress sourcing - Worldwide
	- ref. links
		- https://alidropship.com/
		- https://www.youtube.com/channel/UCO8h6PHW7OC6zP6pHi1NvKQ
		- https://www.oberlo.com/blog/why-you-should-care-about-aliexpress-dropshipping/
		- https://www.shopify.com/blog/117607173-the-definitive-guide-to-dropshipping-with-aliexpress
	- ePacket (delivery method)
		- http://www.chinapostaltracking.com/ems/ebay-epacket-eub/
		- check out which countries are available for the ePacket
	- some Aliexpress sellers keep their most popular products in US warehouses!
	- How To Select Dropshipping Suppliers on AliExpress
		- https://www.oberlo.com/blog/dropshipping-suppliers
- remove all current international shipping items from the ebay listings
    '281952922953',
    '282193597713',
    '282201421567',
    '282201534605',
    '282201610986',
    '282201614819',
    '282201629283',
    '282201775032',
    '282201801281',
    '282202008039',
    '282202075810',
    '282204856897',
    '282244751335',
    '282244751375',
    '282244751549',
    '282244751740',
    '282244751779',
    '282244751879',
    '282244751932',
    '282244752066',
    '282244752347',
    '282244752561',
    '282244752648',
    '282244752735',
    '282244752784',
    '282244752806',
    '282244753069',
    '282244753392',
    '282244753440',
    '282244753507',
    '282244753578',
    '282244753704',
    '282244753949',
    '282244754477',
    '282244754701',
    '282244754808',
    '282244755274',
    '282244756314',
    '282244756556',
    '282244756744',
    '282244757700',
    '282244758090',
    '282244758201',
    '282244758258',
    '282244758646',
    '282244759296',
    '282244759434',
    '282244759618',
    '282244759693',
    '282244759915',
    '282244760584',
    '282244760912',
    '282244761031',
    '282244761242',
    '282244761850',
    '282244761988',
    '282244762248',
    '282244762289',
    '282244762314',
    '282244762448',
    '282244762482',
    '282244762550',
    '282244762582',
    '282244762615',
    '282244762680',
    '282244762738',
    '282244762790',
    '282244763100',
    '282244763221',
    '282244763285',
    '282244763375',
    '282244763476',
    '282244763585',
    '282244763938',
    '282244764116',
    '282244764161',
    '282244764182',
    '282244764219',
    '282244764654',
    '282244764929',
    '282244765161',
    '282244765197',
    '282244765510',
    '282244765624',
    '282244765712',
    '282244765750',
    '282244766095',
    '282244766335',
    '282244766393',
    '282244766511',
    '282244766669',
    '282244766919',
    '282244767931',
    '282249888173', 
- pip update core packages (i.e scrapy=1.2.1)
- Fix women's shoes listing
- Improve frontend automation screen
	- mobile web browser - Yandex android browser supports extensions (which shares Opera Add-ons)
		- opera addon for developers
		- https://dev.opera.com/extensions/
		- https://dev.opera.com/extensions/apis/
	- delete order button
	- handle gift receipt on multiple item orders
	- Report screen
		- daily earning
		- weekly earning
		- monthly earning
	- show ALERT if ASIN doesn't match btw amazon.com site and ordered data
	- show ALERT (or STOP ordering) if the cost is too high
		- get amazon cost from db (amazon_items), and show warning in advanced if the cost is too high
	- simplify tracking/feedback process
		- track/feedback all at once buttton
- Fix a_to_e_category_maps
	- rewrite mapping function
		- Levenshtein Distance (https://pypi.python.org/pypi/python-Levenshtein/0.12.0)
		- Machine learning
	- eBay Category: Books > Catalogs
	- all 'book' related categories
- FIX!! All ModelManagers...
	- replace QuerySet.update_or_create() to obj.save()
- check out Aliexpress sourcing
- sync ebay items (variations) from ebay.com to db
	- GetMultipleItems (max 20 items per each api call)
	- update db tables ebay_items / ebay_item_variations based on ebay.com info
- repricer/reviser update (continued...)
	- phase 2:
		- updates ebay item's title/description only if amazon source updated
- convert to multi-variation items
	- save insertion fee (approx. US$150 /month)
- remove Tor/Privoxy (Scrapy Middleware)
- build amazon item based caching schedule (frequency) algorithm
- Need a screen for mornitoring (item) source contents quality
- review ReplyManager (replymanager.com)
- review ProxyMesh (proxymesh.com) as a secondary proxy service
- review StoreFeeder (www.storefeeder.com)
- convert to Python 3 - future proof
	- Scrapy now officially supports Python 3.3+
	- https://docs.python.org/3/whatsnew/3.0.html
	- https://docs.python.org/3/howto/pyporting.html
- IDEA: chrome extension feature
	- Connect FBA Sellers and eBay Top Sellers
		- benefit to eBay Sellers
			- Dropship items from FBA
		- benefit to FBA Sellers
			- Sell your item at many different channels
	- if a user visit amazon site, crawl/scrape the site and store in db.
		- then update ebay item as well... - much more accurate price / inventory
- write reviser wo crawl script
- Fix reviser (normal) - too many ebay api errors
- FIX!!!
	- EbayItemVariationUtils.build_item_specifics_for_multi_variations() returning None somehow... MUST BE FIXED!!!
- Add search result link on ebay product description
	- http://www.ebay.com/sch/m.html?_ssn=urvicompany&_sacat=234235&_nkw=LEGGINGS
		- _ssn: ebay user id
		- _sacat: ebay category id
		- _nkw: keywords
- need to review popularity functions... still not very accurate...
- improve multi-variation lister
	- do not listing variation if has NO pictures

### Week of 2016-10-23 - 2016-11-05

- global shipping via AmazonGlobal!
	- AmazonGlobal shipping rates
		- https://www.amazon.com/gp/help/customer/display.html?nodeId=201118710
		- TODO: need to more specify shipping fees for each countries
			- i.e. Russia - significantly expansive than other countries
	- https://www.amazon.com/International-Shipping-Direct/b?node=230659011
	- available countries
		- https://www.amazon.com/gp/help/customer/display.html?nodeId=201074230
	- https://www.amazon.com/gp/help/customer/display.html?nodeId=201117930
	- use keywordsearch script
	- add flag on spider - international_shipping
	- update amazon_items.international_shipping any amazon items scraped by this spider
	- db tables
		- amazon_items (add column)
			- international_shipping: boolean
		- ebay_stores (add column)
			- policy_shipping_international
- check size chart on amazon item page
	- db tables
		- amazon_items (add column)
			- has_sizechart: boolean
- Fix Ebay API ERROR:
	- 21919420 - For multiple-variation listings, GTIN values are specified at the variation level.
	- [urvicompany|ASIN:B01I50V8FW|EBID:282193557588] u'ReviseFixedPriceItem: Class: RequestError, Severity: Error, Code: 20004, A mixture of Self Hosted and EPS pictures are not allowed. A mixture of Self Hosted and EPS pictures are not allowed.'
	- [urvicompany|ASIN:B00SXTL3A6|EBID:282193557380] u'ReviseInventoryStatus: Class: RequestError, Severity: Error, Code: 21916799, SKU Mismatch SKU does not exist in Non-ManageBySKU item specified by ItemID.'
- FIX ebay listing!!! lister/reviser!!
- Fix size chart on ebay listing - showing ebay items which is not apparel... 
	- http://www.ebay.com/itm/282008811297
	- must check 'size chart' button/link exists on each amazon item
		i.e. https://www.amazon.com/dp/B01MAVZU23
	- fix amazon_item_apparels table entries
	- fix amazon_apparels spider and amazon_apparel_parser.py
- write production db backup script - should run from local machine
	- http://stackoverflow.com/questions/19664893/linux-shell-script-for-database-backup
- Improve auto-ordering and other web tools
	- improve Orders/Trackings/Feedbacks screen
		- improve fetch orders performance
			- api get_unplaced_orders - refactor this function
			- paginated fetching
		- show related amazon account beside each order made (tracking/feedback screen)
		- simplify tracking/feedback process
			- track/feedback all at once buttton
	- show ALERT if ASIN doesn't match btw amazon.com site and ordered data
	- show ALERT (or STOP ordering) if the cost is too high
		- get amazon cost from db (amazon_items), and show warning in advanced if the cost is too high
	- mobile web browser - Yandex android browser supports extensions (which shares Opera Add-ons)
		- opera addon for developers
		- https://dev.opera.com/extensions/
		- https://dev.opera.com/extensions/apis/
- FIX: gift receipt on multiple item orders
- FIX!
	- Error, Code: 20004, A mixture of Self Hosted and EPS pictures are not allowed. A mixture of Self Hosted and EPS pictures are not allowed.,
	- Class: RequestError, Severity: Error, Code: 21916582, Duplicate VariationSpecifics trait value. Duplicate VariationSpecifics trait value in the VariationSpecificsSet container.,
	- Class: RequestError, Severity: Error, Code: 21916664, Variation Specifics Mismatch. Variation Specifics provided does not match with the variation specifics of the variations on the item.
- fix/improve ebay ListingHandler - especially variations
- need to review popularity functions... still too much crawling...
- repricer/reviser update (continued...)
	- phase 2:
		- updates ebay item's title/description only if amazon source updated
- FIX!! All ModelManagers...
	- replace QuerySet.update_or_create() to obj.save()
- build amazon item based caching schedule (frequency) algorithm
- pip update core packages (i.e scrapy=1.2.0)
- IDEA: chrome extension feature
	- if a user visit amazon site, crawl/scrape the site and store in db.
		- then update ebay item as well... - much more accurate price / inventory
- Marketing
	- select target category - clothing (still the hotest category at eBay)
	- understanding Terapeak research graphes
		- http://www.terapeak.ca/blog/2013/05/29/terapeak-how-to-understanding-common-selling-terms-in-search-results
	- email marketing
- Need a screen for mornitoring (item) source contents quanlity
- Add search result link on ebay product description
	- http://www.ebay.com/sch/m.html?_ssn=urvicompany&_nkw=LEGGINGS
		- _ssn: ebay user id
		- _nkw: keywords
- remove Tor/Privoxy (Scrapy Middleware)
- improve multi-variation lister
	- do not listing variation if has NO pictures
- review ReplyManager (replymanager.com)
- review ProxyMesh (proxymesh.com) as a secondary proxy service
- review StoreFeeder (www.storefeeder.com)
- convert to Python 3 - future proof
	- Scrapy now officially supports Python 3.3+
	- https://docs.python.org/3/whatsnew/3.0.html
	- https://docs.python.org/3/howto/pyporting.html
- combine all new variations to add
	- on closing crawler/spider - pipeline close_spider() function
- store ebay pictures - too much calling UploadSiteHostedPictures... wasting ebay api quota and time...
	- db tables
		- ebay_pictures (new)
			source_picture_url
			picture_url
			base_url
			full_url
			created_at
			updated_at
		- ebay_picture_set_members (new)
			ebay_picture_id
			member_url
			picture_height
			picture_width
			created_at
			updated_at
- repricer/reviser update (continued...)
	- phase 1:
		- monitor amazon item changes with having db tables (keep storing entries):
			amazon_item_prices
			amazon_item_market_prices
			amazon_item_quantites
			amazon_item_titles
			amazon_item_descriptions
			amazon_item_features
		- keep storing entries to
			ebay_item_last_revise_attempted
		- ebay store id based reviser

### Week of 2016-10-16 - 2016-10-22

- need to add a column: ebay_item_variations.ebay_store_id
- scrapy pipeline EbayItemRevisePipeline
	- if variations, should not upload to ebay until all variations has been scraped and stored in db
- convert to Python 3 - future proof
	- Scrapy now officially supports Python 3.3+
	- https://docs.python.org/3/whatsnew/3.0.html
	- https://docs.python.org/3/howto/pyporting.html
- FIX!! All ModelManagers...
	- replace QuerySet.update_or_create() to obj.save()
- build amazon item based caching schedule (frequency) algorithm
- write production db backup script - should run from local machine
	- http://stackoverflow.com/questions/19664893/linux-shell-script-for-database-backup
- active repricer/reviser
	- monitor price changes at amazon
	- store prices in db
	- FIND PATTERN AND BUILD ALGORITHM!!!
	- db table:
		- amazon_item_prices (new table - only create new entry if price changed from previous data)
			- asin
			- parent_asin
			- price
			- created_at
			- updated_at
		- amazon_item_market_prices (new table - only create new entry if market price changed from previous data)
			- asin
			- parent_asin
			- market_price
			- created_at
			- updated_at
		- amazon_item_quantites (new table - only create new entry if quantity changed from previous data)
			- asin
			- parent_asin
			- quantity
			- created_at
			- updated_at
- simplify repricer/reviser
	- run repricer each ebay_store_id based
	- this is possible since we are now using cached amazon item sources
	- use ListingHandler.revise_item() for the new repricer
	- also updates ebay item's title/description only if amazon source updated
	- db table:
		- amazon_item_titles (new table - only create new entry if title changed from previous data)
			- asin
			- parent_asin
			- title
			- created_at
			- updated_at
		- amazon_item_descriptions (new table - only create new entry if description changed from previous data)
			- asin
			- parent_asin
			- description
			- created_at
			- updated_at
		- amazon_item_features (new table - only create new entry if features changed from previous data)
			- asin
			- parent_asin
			- features
			- created_at
			- updated_at
		- ebay_item_last_revise_attempted (new table - update updated_at field each time reprice runs)
			- ebay_store_id
			- ebid
			- ebay_item_variation_id
			- asin
			- parent_asin
			- created_at
			- updated_at
		- ebay_item_repriced_histories (probably remove...)
- need to review popularity functions... still too much crawling...
- FIX Caching
	- problem with current caching
		1. too much hard drive space used
		2. some bytecode/utf8 unicoded sting cannot be stored in mysql
			- http://stackoverflow.com/questions/2108824/mysql-incorrect-string-value-error-when-save-unicode-string-in-django
			- http://stackoverflow.com/a/11597447
	- how to solve?
		- remove amazon_item_cached_html_pages table
		- use amazon_items table itself as a cache table
		- AmazonItemCrawlControlMiddleware (downloader middleware)
			- once crawler hits an asin, which its amazon_items entry recently updated, generate HtmlResponse obj with 
				url - generate with asin
				body - empty
				flags - 'cached_amazon_item'
		- build AmazonItem (scrapy item) at item parser
			- build AmazonItem (scrapy item) from db
			- with flag '_cached'
		- do not save '_cached' AmazonItem into db (at db.py pipeline)
		- remove CacheAmazonItemMiddleware
- FIX variations
	- any removed variations from amazon.com should be applied to my ebay items as well.
	 	- check asin_variation_values (refer AmazonItemParser.__extract_variation_asins()), and find any removed asins
	 	- any removed asin should be inactived - amazon_items.status = 0
	 	- either:
	 		- remove entry from ebay_item_variations
	 		- or make oos - quantity = 0
	- any newly added variations from amazon.com should be applied to my ebay items as well
- make a function to query amazon item variations and ebay item variations (checking status, fba, and so on..)
- FIX: gift receipt on multiple item orders
- keep mornitoring CRAWLERA QUOTA, and amazon_item_cached_html_pages table
- pip update core packages (i.e scrapy=1.2.0)
- IDEA: chrome extension feature
	- if a user visit amazon site, crawl/scrape the site and store in db.
		- then update ebay item as well... - much more accurate price / inventory
- Improve auto-ordering and other web tools
	- show ALERT (or STOP ordering) if the cost is too high
		- get amazon cost from db (amazon_items), and show warning in advanced if the cost is too high
	- improve Orders/Trackings/Feedbacks screen
		- simplify tracking/feedback process
			- track/feedback all at once buttton
		- improve fetch orders performance
			- api get_unplaced_orders - refactor this function
			- paginated fetching
	- mobile web browser - Yandex android browser supports extensions (which shares Opera Add-ons)
		- opera addon for developers
		- https://dev.opera.com/extensions/
		- https://dev.opera.com/extensions/apis/
- Marketing
	- select target category - clothing (still the hotest category at eBay)
	- understanding Terapeak research graphes
		- http://www.terapeak.ca/blog/2013/05/29/terapeak-how-to-understanding-common-selling-terms-in-search-results
	- email marketing
- Need a screen for mornitoring (item) source contents quanlity
- Add search result link on ebay product description
	- http://www.ebay.com/sch/m.html?_ssn=urvicompany&_nkw=LEGGINGS
		- _ssn: ebay user id
		- _nkw: keywords
- remove Tor/Privoxy (Scrapy Middleware)
- improve multi-variation lister
	- do not listing variation if has NO pictures
- review ReplyManager (replymanager.com)
- review ProxyMesh (proxymesh.com) as a secondary proxy service
- review StoreFeeder (www.storefeeder.com)

### Week of 2016-10-02 - 2016-10-15

- Fix multi-item order: record number # 8270 (3-item order)
- Caching seems not working... need to review...
- pip update core packages (i.e scrapy=1.2.0)
- Fix/change repricing (popularities)
	- too many crawling now... exceeding CRAWLERA QUOTA!
	- need to cache HTML into db for each amazon item url
	- use the caching db for RepricingFrequencyControllerMiddleware and CachedAmazonItemMiddleware
	- scrapy.http.HtmlResponse
	- db table:
		- amazon_item_cached_html_pages (new table)
			- asin (not a parent_asin)
			- request_url
			- response_url
			- body
			- created_at
			- updated_at
- FIX: gift receipt on multiple item orders
- Need a screen for mornitoring (item) source contents quanlity
- Add search result link on ebay product description
	- http://www.ebay.com/sch/m.html?_ssn=urvicompany&_nkw=LEGGINGS
		- _ssn: ebay user id
		- _nkw: keywords
- remove Tor/Privoxy (Scrapy Middleware)
- improve multi-variation lister
	- do not listing variation if has NO pictures
- review ReplyManager (replymanager.com)
- review ProxyMesh (proxymesh.com) as a secondary proxy service
- review StoreFeeder (www.storefeeder.com)
- Amazon apparel item size chart
	- i.e.
		https://www.amazon.com/gp/product/ajax-handlers/apparel-sizing-chart.html/?asin=B0064Y3ON6&isUDP=1
	- by parent_asin
	- db tables:
		- amazon_item_apparels (new table)
			- parent_asin
			- size_chart
			- created_at
			- updated_at
- FIX: too many Null description amazon items. need to re-crawl/scrape items
- Improvoe auto-ordering and other web tools
	- improve auto-ordering
		- order has more than 1 item
		- apply coupon if exists
		- update cancelled item (status)
		- db tables:
			- amazon_orders (add/remove columns)
				- asin (remove column)
				- savings (add column - money format usually negative number - i.e. coupon saving)
			- amazon_order_items (new table)
				- id
				- order_id
				- asin
				- is_variation
				- created_at
				- updated_at
				- amazon_order_id (foreign key of amazon_orders table)
		- write migration script (fill amazon_order_items table)
	- improve Orders/Trackings/Feedbacks screen
		- simplify tracking/feedback process
			- track/feedback all at once buttton
		- improve fetch orders performance
			- paginated fetching
	- mobile web browser - Yandex android browser supports extensions (which shares Opera Add-ons)
		- opera addon for developers
		- https://dev.opera.com/extensions/
		- https://dev.opera.com/extensions/apis/
- Marketing
	- select target category - clothing (still the hotest category at eBay)
	- understanding Terapeak research graphes
		- http://www.terapeak.ca/blog/2013/05/29/terapeak-how-to-understanding-common-selling-terms-in-search-results
	- email marketing
- DO NOT WASTE CRAWLERA QUOTA!
	- effective listing - do not crawl/scrape again if the data already exists in db and not older than 3 days
	- effective repricer script - based on (clicks/watches/solds values in ebay_item_stats)
		- listing performance screen (with ebay_item_stats table)
		- based on number of views:
			- popular items - 10% (crawl every 8 hours)
			- normal items - 40% (crawl 16 hours)
			- slow items - 50% (crawl 48 hours)
		- compare old vs new (i.e. repricing 10000 items)
			- old way: 100% (crawl 3 times in 2 days)
				- 30000 crawl in 2 days.
			- new way:
				- popular items: 1000 x 3 x 2 = 6000 crawl in 2 days
				- normal items: 4000 x 3 = 12000 crawl in 2 days
				- slow items: 5000 x 1 = 5000 crawl in 2 days
				- total: 6000 + 12000 + 5000 = 21000 crawl in 2 days (SAVING 30% CRAWLERA QUOTA)
			- * follow new way if ebay item been listed more than 7 days
			- * follow old way (treat as normal item in new way) if ebay item been listed less than 7 days
			- db tables:
				- ebay_item_stats (add a column)
					- ebay_store_id
				- ebay_item_popularities (brand new)
					- id
					- ebay_store_id
					- ebid
					- popularity (i.e. 1 - popular, 2 - normal, 3 - slow)
					- created_at
					- updated_at
					- * needs a script to insert entries in ebay_item_popularities table (run once a day)
				- ebay_item_repriced_histories (brand new)
					- id
					- ebay_store_id
					- ebid
					- ebay_item_variation_id (default 0)
					- asin
					- parent_asin (default null)
					- eb_price
					- quantity
					- created_at
					- updated_at
					- * repricer script inserts entries each time
				- * repricer scrapy script (or middleware) should check both tables ebay_item_popularities and ebay_item_reprice_history to decide repricing the item or not (repricer_sold does not follow this rule)
				- * write seperate scripts for each popular/normal/slow items because of lock files (or add a command flag i.e. -p slow/-p normal/-p popular)
- fix reprice on app server - seems not running...
- improve repricer
	- do not query base on parent_asins. query and crawl directly asin based

### Week of 2016-09-11 - 2016-09-17 and 2016-09-25 - 2016-10-01

- need to rewrite repricer - should not based on parent_asins... crawl directly individual child asins...
- need to handle amazon packaging type variation - Product Packaging: Frustration-Free Packaging / Standard Packaging
- DO NOT WASTE CRAWLERA QUOTA!
	- effective listing - do not crawl/scrape again if the data already exists in db and not older than 3 days
	- effective repricer script - based on (clicks/watches/solds values in ebay_item_stats)
		- listing performance screen (with ebay_item_stats table)
		- popular items (30% - crawl 3 times in 1 day) / normal items (40% - crawl 3 times in 2 days) / slow items (30% - crawl 1 time in 2 days)
- modify end listing script
- pip update core packages (i.e ebaysdk==2.1.4, scrapy=1.1.3)
- bug fix: AddFixedPriceItem: Class: RequestError, Severity: Error, Code: 20004, A mixture of Self Hosted and EPS pictures are not allowed
	- convert variation pictures to EPS pictures
- improve best seller listing script
- convert variation names for shoes - US Shoe Size (Women's), US Shoe Size (Men's)
- handle ebay item (ebid) which has been already ended, but its amazon item (asin) still alive and has been changed to something else.
	- delete from db...
- db garbage collector script
	- delete inactive ebay items older than 3 months
	- delete entries in error db tables which older than 1 months

### Week of 2016-09-11 - 2016-09-17 and 2016-09-18 - 2016-09-24

- remove(or oos) items which does not have good images... (cannot upload via api - impossible to manage with software)
- pip update core packages (i.e ebaysdk==2.1.4)
- ebay api GetCategoryFeatures - find whether ebay categories allow variations or not
	- required db updates:
		- ebay_category_features (new)
			- id
			- ebay_category_id
			- ebay_category_name
			- brand_mpn_identifier_enabled (boolean) # postponed - remove this column for now...
			- upc_enabled (varchar 100)
			- variations_enabled (boolean)
- variations (clothes, shoes, and so on - lots of posibilities)
	- handling creating ebay listing
		- scraping from Amazon.com
			- 1. find parent_asin from html source and store at amazon_items.parent_asin (if exists, the item has variations)
				- if there is no parent asin (no variations), parent_asin will be the asin itself
			- 2. crawl/scrape all available amazon twisters - need to improve
			- 3. scrape each variation specifics and store
		- task table - store parent_asin in amazon_scrape_tasks as well
		- listing item to eBay.com
			- 1. get distinct parent_asin from task list
			- 2. find all amazon items (asin) have same parent_asin
			- 3. if there are more than one amazon item (asin), build variation objects for child asins
			- 4. item pictures - find common pictures (by url), and list as common, and rest of them will be listed as variation pictures
			- 5. item title - get common words across amazon variation titles
	- handling repricing ebay listing
		- 1. get distinct asin (not parent_asin) and scrape amazon item urls
		- 2. get ebay_item object from the asin (lookup 'both' ebay_items and ebay_item_variations table)
		- 3. since ReviseInventoryStatus accept asin as SKU, current script still be applicable
	- handling ordering
		- always check Variation and Variation.SKU to see whether the order has been related with specific variation
		- everything else, should be the same...
	- HOTFIX: revising existing ebay listing - (IMPOSSIBLE!! - ebay not allow convert from non-multi-sku items to multi-skue items...)
		- 1. get all ebid (status != 0) - store in a list
		- 2. perform while loop.. (not for loop)
		- 3. get next ebid from the list, and find a related amazon item from amazon_items (not from amazon_item_variations)
		- 4. find out whether the amazon item has variations, by compairing asin/parent_asin values
			- a) if no variations, go to next ebid on the list
			- b.1) if has variations, find the best impression scored ebay item among the variations from database (ebay_item_stats)
			- b.2) modify the best impression scored ebay item with having all variations, and end/inactive all other ebay items, and remove ebids from the list
			- b.3) go to next ebid on the list
	- required db updates:
		- amazon_items (modify)
			- parent_asin
			- variation_specifics
		- amazon_scrape_tasks (modify)
			- parent_asin
		- ebay_item_variations (new)
			- id
			- ebay_item_id
			- ebid
			- asin
			- specifics # json string
			- price
			- quantity

### Week of 2016-09-04 - 2016-09-10

- make/test mobile friendly ebay items (http://www.i-ways.net/mobile-friendly/en-us/)
- fix ebay item features - remove hidden/unwanted contents
- set ebay store categories and implement items into the category
	- based on amazon category
	- escape special characters (i.e. &) for category name before submit
	- max custom category name length (30)
	- db table - ebay_store_categories
		- id
		- ebay_store_id
		- category_id - long unsigned
		- parent_category_id - long unsigned (default -999)
		- name - varchar (100)
		- order - int
		- created_at
		- updated_at

- set expedited shipping free (3 day shipping)
	- set one-day shipping price higher
- Promoted Listings (https://pls.ebay.com/plsweb/plwelcome)
- ReplyManager (replymanager.com)
	- a good software tool for back-office ebay email/message management (ACL available)
- focus on content quality
	- accurate title and description
	- accurate pictures
	- crawl amazon and parsing information from each run_repricer.py runs and store db, but update title/description/pictures to ebay once a week
		- seperate crawling / uploading

### Week of 2016-08-28 - 2016-09-03

- use terapeak for finding hot category
- use ebay seller hub (https://www.ebay.com/sh) for my listing performance (find items to end)
- write a script scraping amazon items by keyword search
- run_repricer_sold.py - rewrite this script and run every 2 hours

### Week of 2016-08-21 - 2016-08-27

- automate fetching tracking number
- automate sending thank you email and feedback on package delivered
- automate ordering feature updates...

### Week of 2016-08-14 - 2016-08-20

- make scraper compatible with new amazon's url logic
	- amazon does not redirect to another asin link any more
	- check with 'twister' form
- update pip libraries (Scrapy 1.1.1, and others)
- automate with chrome extension (continue...)
	- ebay_orders [database table]
		id
		order_id
		record_number
		total_price
		shipping_cost
		buyer_email
		buyer_user_id
		buyer_status
		buyer_shipping_name
		buyer_shipping_street1
		buyer_shipping_street2
		buyer_shipping_city_name
		buyer_shipping_state_or_province
		buyer_shipping_postal_code
		buyer_shipping_country
		buyer_shipping_phone
		checkout_status
		creation_time
		paid_time

	- ebay_order_items [database table]
		id
		order_id
		ebid
		transaction_id
		title
		sku
		quantity
		price

	- ebay_order_shippings
		- id
		- order_id
		- carrier
		- tracking_number
	
	- ebay_order_amazon_orders
		- id
		- ebay_order_id
		- amazon_order_id

	- ebay_order_automation_errors
		- id
		- ebay_order_id
		- error_message

### Week of 2016-07-10 - 2016-07-23

- update pip libraries (Scrapy 1.1.1, and others)
- in order to run chrome browser in mobile mode, install User-Agent Switcher for Google Chrome extension. (https://chrome.google.com/webstore/detail/user-agent-switcher-for-g/ffhkkpnppgnfaobgihpdblnhmmbodake?hl=en)
- re-design chrome extension
	- extension icon
		- no popup
		- onclick icon: open automationJ page (show list of unplaced orders)
	- content scripts workflow:
		- order list page
			1. click 'Order now' button
			2. open new tab with amazon asin url
			3. listen one-time request (runtime.onMessage.addListener) and respond with order data
		- amazon item page
			1. once page loaded, request one-time request to the order list page and receive order data
			2. proceed automation

	- background/event page (eventPage.js)
		- fetch all orders from backend
		- store 'ebay order id' 'amazon order tab id' map
		- respond data from any request messages from content scripts

- automation - chrome extension
	- cross-reference with Selling Manager's Record ID
		GetSellingManagerSaleRecord - SellingManagerSoldOrder.SaleRecordID
	- chrome extension technical specs
		- chrome.storage.local
			- rfi.orders = [
				{
					orderId: order_id,
					asins: [ asin1, asin2 ],
					shippingName: buyer_shipping_name,
					shippingStreet1: buyer_shipping_street1,
					shippingStreet2: buyer_shipping_street2,
					shippingCity: buyer_shipping_city_name,
					shippingState: buyer_shipping_state_or_province,
					shippingPostal: buyer_shipping_postal_code,
					shippingCountry: buyer_shipping_country,
					shippingPhone: buyer_shipping_phone,
					shippingSpeed: buyer_shipping_country,
					amazonOrderStatus: 'not_ordered', # 'not_ordered', 'completed', 'error'
					amazonOrderErrorMessage: '',
				},
				{
					orderId: order_id,
					asins: [ asin1, asin2 ],
					shippingName: buyer_shipping_name,
					shippingStreet1: buyer_shipping_street1,
					shippingStreet2: buyer_shipping_street2,
					shippingCity: buyer_shipping_city_name,
					shippingState: buyer_shipping_state_or_province,
					shippingPostal: buyer_shipping_postal_code,
					shippingCountry: buyer_shipping_country,
					shippingPhone: buyer_shipping_phone,
					shippingSpeed: buyer_shipping_country,
					amazonOrderStatus: 'not_ordered', # 'not_ordered', 'completed', 'error'
					amazonOrderErrorMessage: '',
				},
				...
			]
			- refresh orders list on fetch
			- update amazonOrderStatus/amazonOrderErrorMessage on complete at amazon
			- store back to backend once completed



### Week of 2016-07-03 - 2016-07-09

- actions.py: __filter_orders_not_placed_at_origin function needs to be fixed - cannot use SKU field for filtering...
	- might need to cross-reference 'transactions' table in order to save/retrieve amazon order id
- automation - chrome extension
	- workflow
		1. extension popup
			- fetch and display orders (which not ordered to amazon)
				- display error messages for each orders if occur
			- have 'Refresh' button
			- have 'Order' buttons to each orders
			- have 'Order All' button at the top/bottom
		2. ordering
			- automation ordering process at amazon.com
			- if success:
				- retrieve and store order id
				- flag success
			- else:
				- flag error
				- store error code / description

### Week of 2016-06-26 - 2016-07-02

- automation (ordering/tracking/feedback)
	- using chrome extension - i.e. oberlo.com
- put original price (strikethrough price) if possible
	- Item.DiscountPriceInfo.OriginalRetailPrice (e.g. put 40% higher than original price)
	- use amazon_items.market_price column
- need to handle redirected amazon items (scrapy - compare asins in 'redirect_urls')
	- make oos if redirected to a different amazon item (asin)

### Week of 2016-06-19 - 2016-06-25

- write a script to remove all excl_brand items
- get number of clicks/solds info for each ebay items
	- ebay API - GetItem
		- Item.HitCount
		- Item.SellingStatus.QuantitySold
		- Item.WatchCount - add IncludeWatchCount on request
	- check item performance and remove/end poor-performed items
	- db table: ebay_item_stats
		- id
		- ebid
		- clicks
		- watches
		- solds
		- created_at
		- updated_at
		- ts
- study Terapeak
- register an account at Terapeak
- seperate amazon scrape and ebay listing
	- two different cronjobs
	- need db table(s) to track the scraped amazon item with timestamp
- make round-up price (e.g. $24.99) - make item/listing look more legit
- 80legs.com try out
- price tracking / history table
- fix ebay cagetory
	eg. 281983864538: B005NZ4MFQ
		- amazon category: Health & Household : Household Supplies : Dishwashing : Scouring Pads
		- ebay_category_id: 58102

### Week of 2016-06-12 - 2016-06-18

- add ebay_stores.margin_min_dollar column - default null
- need to double check repricer script - check amazon item link filtering
- resolve Crawlera performance issue - upgrade plan
	- Crawlera alternative
		- 80legs.com (free trial - limited feature) / datafiniti.co (free trial - 5-days)
		- mozenda.com

### Week of 2016-06-05 - 2016-06-11

- scrape variation each amazon items list on ebay store
	- use amazon_scrape_tasks table to store new asins
		1. scrape each amazon items and their variations, and store in amazon_scrape_tasks table
		2. list all items to ebay store based on amazon_scrape_tasks table (filtered by given task_id)

- run_repricer needs to be fixed: ebay item title/description updates (pictures - need seperate script/task)
	- run_repricer -> reviser
		- update price/quantity/status if necessary
		- update title/description if title changed

### Week of 2016-05-29 - 2016-06-04

- refresh best seller scraping and listing mechanism
	- add new columns on amazon_bestsellers: review_count, avg_rating
	- add new columns on ebay_store_preferred_categories: category_url
	- add new table: amazon_scrape_tasks
		- id
		- task_id (uuid)
		- ebay_store_id
		- asin
		- created_at
		- updated_at
		- ts
	- new logic:
		- scrape with subcategories
			1. scraping Amazon Best Sellers - with given categories and their subcategories
			2. store all information in tables, amazon_bestsellers and amazon_scrape_tasks
			3. scrape each amazon items based on amazon_scrape_tasks table (filtered by given task_id)
			4. list all items to ebay store based on amazon_scrape_tasks table (filtered by given task_id)
		- scrape without subcategories
			1. update table, ebay_store_preferred_categories, with given info
			2. scraping Amazon Best Sellers - with given categories
			3. store all information in tables, amazon_bestsellers and amazon_scrape_tasks
			4. scrape each amazon items based on amazon_scrape_tasks table (filtered by given task_id)
			5. list all items to ebay store based on following tables:
				- ebay_store_preferred_categories: ebay_store_id, category_url, max_items
				- amazon_bestsellers - bestseller_category_url, asin

- all the tasks below

### Week of 2016-05-22 - 2016-05-28

- apply ebay search engine (cassini)
	- utilize ebay item specific
	- parse 'Product Information' from amazon item page, and insert into ebay item specific

- all the tasks below

### Week of 2016-04-17 - 2016-04-23

- fix ebay item category mapping algoritm, as well as any incorrected items

- all the tasks below

### Week of 2016-04-10 - 2016-04-16

- let's working on overstock.com first!!

- Overstock product url pattern:
	http://www.overstock.com/ENTER_PID_HERE/product.html
	e.g. http://www.overstock.com/9074455/product.html

- build scraper for Wal-Mart (ShippingPass), Newegg (Premier), and Overstock (Gold club)

- allow PO BOX shipping address
	- make note it would take extra 3-5 business days

- need to rework /atoe/bin/listing_pictures_reviser.py (disabled for now)

- need to rework/seperate repricer - scraping part / ebay uploading part

- check ebay notification listeners - listeners down sometimes

- rework automate ordering - casperjs + frameworked

- import ebay item list for the new registered user

- start UI (web) with django + twitter bootstrap or crispy-forms
	- amazon item
		- tag based organizing
		- not category based any more
		- need to find out some way to handle amazon items which title has been changed... not to end item......
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3
    - crispy-forms - ref: http://django-crispy-forms.readthedocs.org/en/latest/

- (* long-term todo) improve performance of ebay revise item - logic update

- (* long-term todo) check/update amazon item pictures and also related ebay items if necessary

- (* long-term plan) allow user generate (customized) ebay item calculation formular

- (* long-term plan) gyft api for purchasing amazon gift card with paypal.


### Week of 2016-02-14 - 2016-02-20

- convert proxy engine from Tor+Privoxy to Crawlera
	- seperate services - Paid service: Crawlera middleware, Free service: Tor+Privoxy middleware

- allow PO BOX shipping address
	- make note it would take extra 3-5 business days

- need to rework /atoe/bin/listing_pictures_reviser.py (disabled for now)

- need to rework/seperate repricer - scraping part / ebay uploading part

- check ebay notification listeners - listeners down sometimes

- rework automate ordering - casperjs + frameworked

- import ebay item list for the new registered user

- start UI (web) with django + twitter bootstrap or crispy-forms
	- amazon item
		- tag based organizing
		- not category based any more
		- need to find out some way to handle amazon items which title has been changed... not to end item......
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3
    - crispy-forms - ref: http://django-crispy-forms.readthedocs.org/en/latest/

- postpone Crawlera proxy

- (* long-term todo) improve performance of ebay revise item - logic update

- (* long-term todo) check/update amazon item pictures and also related ebay items if necessary

- (* long-term plan) allow user generate (customized) ebay item calculation formular

- (* long-term plan) gyft api for purchasing amazon gift card with paypal.

- (* long-term plan) amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-02-15

##### Development

1. let's focus on auto-ordering - which is the cash cow
	- convert current casper script to frameworked
1. django admin
1. repricer improve scraping performance - privoxy + polipo + tor
	- setup seperate proxy server (with privoxy + polipo + tor)
	- improve scraping logic
	- frontera/scrapy cluster - eventually
1. start working on web interfaces - django + crispy-forms + Pure CSS
1. automate insert tracking code / send feedback to buyer - later

----------------------------------------
### Week of 2016-02-07 - 2016-02-13

- ebay revise item logic update

- import ebay item list for the new registered user

- start UI (web) with django + twitter bootstrap or crispy-forms	
	- amazon item
		- tag based organizing
		- not category based any more
		- need to find out some way to handle amazon items which title has been changed... not to end item......
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3
    - crispy-forms - ref: http://django-crispy-forms.readthedocs.org/en/latest/

- postpone Crawlera proxy

- (* long-term todo) check/update amazon item pictures and also related ebay items if necessary

- (* long-term plan) allow user generate (customized) ebay item calculation formular

- (* long-term plan) gyft api for purchasing amazon gift card with paypal.

- (* long-term plan) amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-02-12

##### Development

1. let's focus on auto-ordering - which is the cash cow
1. django admin
1. repricer improve scraping performance - privoxy + polipo + tor
	- setup seperate proxy server (with privoxy + polipo + tor)
	- improve scraping logic
	- frontera/scrapy cluster - eventually
1. start working on web interfaces - django + crispy-forms + Pure CSS
1. automate insert tracking code / send feedback to buyer - later

----------------------------------------
#### 2016-02-11

##### Development

1. django admin
1. repricer improve scraping performance - privoxy + polipo + tor
	- setup seperate proxy server (with privoxy + polipo + tor)
	- improve scraping logic
	- frontera/scrapy cluster - eventually
1. start working on web interfaces - django + crispy-forms + Pure CSS
1. automate insert tracking code / send feedback to buyer - later

----------------------------------------
#### 2016-02-10

##### Development

1. repricer improve scraping performance - privoxy + polipo + tor
	- setup seperate proxy server (with privoxy + polipo + tor)
	- improve scraping logic
	- frontera/scrapy cluster - eventually
1. start working on web interfaces - django + crispy-forms + Pure CSS
1. automate insert tracking code / send feedback to buyer - later

----------------------------------------
#### 2016-02-08

##### Development

1. repricer - need to improve performance/speed - i.e. change debug level - done (still need to monitor how much improved)
1. start working on web interfaces - django + crispy-forms
1. automate insert tracking code / send feedback to buyer - later

----------------------------------------
#### 2016-02-07

##### Development

1. revise ebay item (title/description/pictures) improve logic - done
1. repricer - need to improve performance/speed - i.e. change debug level
1. automate insert tracking code / send feedback to buyer
1. start working on web interfaces - django + crispy-forms

----------------------------------------
### Week of 2016-01-31 - 2016-02-06

- test django models
	- build relationship (foreignkeys) in db with django commend script

- import ebay item list for the new registered user

- start UI (web) with django + twitter bootstrap or crispy-forms	
	- amazon item
		- tag based organizing
		- not category based any more
		- need to find out some way to handle amazon items which title has been changed... not to end item......
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3
    - crispy-forms - ref: http://django-crispy-forms.readthedocs.org/en/latest/

- postpone Crawlera proxy

- (* long-term todo) check/update amazon item pictures and also related ebay items if necessary

- (* long-term plan) allow user generate (customized) ebay item calculation formular

- (* long-term plan) gyft api for purchasing amazon gift card with paypal.

- (* long-term plan) amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-02-06

##### Development

1. monitoring production scripts/db
1. hotfix item description / revise all ebay items

----------------------------------------
#### 2016-02-05

##### Development

1. migrate django database into production

----------------------------------------
#### 2016-02-02

##### Development

1. generate db relationship with django script
1. (* long-term todo) update amazon item pictures.

----------------------------------------
#### 2016-02-02

##### Development

1. generate db relationship with django script

----------------------------------------
#### 2016-02-01

##### Development

1. git rebase/merge branch - done
1. generate db relationship with django script

----------------------------------------
### Week of 2016-01-24 - 2016-01-30

- complete auto-ordering - working with Crawlera support team

- complete converting models from Storm to Django

- import ebay item list for the new registered user

- start UI (web) with django + twitter bootstrap or crispy-forms	- amazon item
		- tag based organizing
		- not category based any more
		- need to find out some way to handle amazon items which title has been changed... not to end item......
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3
    - crispy-forms - ref: http://django-crispy-forms.readthedocs.org/en/latest/

- (* long-term plan) gyft api for purchasing amazon gift card with paypal.

- (* long-term plan) amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-01-30

##### Development

1. keep converting models and model_managers module
1. Crawlera - cancel now, and re-register later on

----------------------------------------
#### 2016-01-27

##### Development

1. keep converting models and model_managers module
1. Crawlera - cancel now, and re-register later on

----------------------------------------
#### 2016-01-26

##### Development

1. fix ebay item title - allow commonly used special characters - done
1. keep converting models and model_managers module
1. Crawlera - upgrade (to do later)

----------------------------------------
#### 2016-01-25

##### Development

1. test and fix auto-ordering - need to upgrade plan... hmmm...
1. store all ebay item categories with django model - working on...
1. convert models and model_managers module - working on...

----------------------------------------
### Week of 2016-01-17 - 2016-01-23

- fix Cookie and other issues with integrating Crawlera proxy

- gyft api for purchasing amazon gift card with paypal.

- start UI (web) with django + twitter bootstrap
	- amazon item
		- tag based organizing
		- not category based any more
    - django+bootstrap pip package - ref: https://github.com/dyve/django-bootstrap3

- amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-01-20

##### Development

1. django 1.9 + bootstrap
    - continue converting model related classes to django...

----------------------------------------
#### 2016-01-19

##### Development

1. django 1.9 + bootstrap
    - continue converting model related classes to django

----------------------------------------
#### 2016-01-18

##### Development

1. django 1.9 + bootstrap
    - port all models to django models

----------------------------------------
#### 2016-01-16

##### Development

1. UI - django 1.9

----------------------------------------
### Week of 2016-01-10 - 2016-01-16

- finish automation ordering / tracking shipping
	- casperjs / celery / rabbitmq
- improve amazon-to-ebay category mapping
	- ebay api GetSuggestedCategories

			http://developer.ebay.com/devzone/xml/docs/reference/ebay/GetSuggestedCategories.html

- use private proxy service (Ninja Proxy, HideMyAss, Crawlera, ProxyMesh, or etc...) other than Tor for Site Automations

- gyft api for purchasing amazon gift card with paypal.

- start UI (web) with django
	- amazon item
		- tag based organizing
		- not category based any more

- amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-01-16

##### Development

1. UI - django 1.9

----------------------------------------
#### 2016-01-14

##### Development

1. set up private proxy server (either Crawlera or ProxyMesh) - working with Crawlera
1. UI - django

----------------------------------------
#### 2016-01-13

##### Development

1. setup automation ordering / tracking shipping celery tasks on order server - done (still need to monitor/test)
1. improve amazon-to-ebay category mapping - done
1. need to improve proxy for automations...
1. UI - django

----------------------------------------
#### 2016-01-12

##### Development

1. finish automation ordering / tracking shipping
1. improve amazon-to-ebay category mapping

----------------------------------------
### Week of 2016-01-03 - 2016-01-09

- improve performance ordering automation with lynx
- start UI (web) with django
	- amazon item
		- tag based organizing
		- not category based any more
- amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2016-01-05

##### Development

1. build script for lynx

----------------------------------------
#### 2016-01-04

##### Customer support

1. deal case with queenjane15 - done (refunded)

##### Development

1. build script for lynx
	- tested with testing script

----------------------------------------
### Week of 2015-12-27 - 2016-01-02

- complete auto ordering
- start UI (web) with django
	- amazon item
		- tag based organizing
		- not category based any more
- amazon prime compatitors
	- newegg premier
	- walmart free shipping

----------------------------------------
#### 2015-12-29

##### Development

1. amazon ordering bug fix - do not re-adding item to cart if already exists. - currently working..
1. send email to user once order has been placed / error occurred.

----------------------------------------
#### 2015-12-27

##### Development

1. amazon ordering bug fix - do not re-adding item to cart if already exists.
1. send email to user once order has been placed / error occurred.

----------------------------------------
### Week of 2015-12-20 - 2015-12-26

- complete auto ordering
- start UI (web) with django
- scale up - add 'ordering server' and 'db server' - done

----------------------------------------
#### 2015-12-25

##### Server management / Development

1. duplicate ateapp server for ordering server - done
1. test amazon ordering

----------------------------------------
#### 2015-12-23

##### Server management

1. set up database server (new linode server) with remote access - done
1. move mysqldump to new server - done
1. duplicate ateapp server for ordering server

----------------------------------------
#### 2015-12-20

##### Development

1. generate amazon order based on ebay transaction
1. script to post tracking number / to send thank-you-email to buyer
1. make cronjob of above [2.] - every 6 hours

----------------------------------------
### Week of 2015-12-13 - 2015-12-19

- keep working on auto-ordering to amazon.com - selenium + phantomjs

----------------------------------------
#### 2015-12-19

##### Development

1. update tracking number / leave feedback on ebay

----------------------------------------
#### 2015-12-18

##### Development

1. improve ordering script - reliability - done
1. amazon notification (SOAP) - X (unable to use SOAP - since not an amazon seller...)
	- using selenium + phantomjs scraping instead - done

----------------------------------------
#### 2015-12-16

##### Development

1. setup proxy (Tor + Privoxy)
1. workaround amazon's filtering
1. amazon notification (SOAP)

----------------------------------------
#### 2015-12-14

##### Development

1. keep working on auto-ordering - selenium + phantomjs

----------------------------------------

### Week of 2015-12-06 - 2015-12-12

- keep working on auto-ordering to amazon.com - casperjs

----------------------------------------
#### 2015-12-07

##### Development

1. listing.py - add option most discount items first - done
1. filter PrimePantry - done
1. keep working on auto-ordering - casperjs

----------------------------------------

### Week of 2015-11-29 - 2015-12-05

- bug fix on repricing - failed to parse amazon item page
- keep working on auto-ordering to amazon.com - casperjs
- fix amazon-to-ebay category mapping... received warning from ebay...

----------------------------------------
#### 2015-12-04

##### Development

1. revamp listing_sold.py script
1. keep working on auto-ordering - casperjs
1. fix amazon-to-ebay category mapping - making api for public??
1. implement ebay api RelistFixedPriceItem - let's postpone

----------------------------------------
#### 2015-12-03

##### Development

1. bug fix on repricing - done
	- failed to parse amazon item page
	- add task flag on each crons... just like old scripts
1. set oos instead of end items on each cases - done
1. keep working on auto-ordering - casperjs

----------------------------------------
#### 2015-12-02

##### Development

1. bug fix on repricing - failed to parse amazon item page

----------------------------------------

### Week of 2015-11-16 - 2015-11-23

- business research, review with numbers
	- what is your break-even much
	- how big is the market
	- how many competitors in the market
	- how much money I can make if I achieve certain amount of volume
- handle end list notification listener
- auto-ordering to amazon.com - casperjs

----------------------------------------
#### 2015-11-23

##### Development

1. why casperjs clicking not working???

----------------------------------------
#### 2015-11-20

##### Customer support

1. wrong item sent - done (by refund - sucks)
	- received refund from amazon.com
	- need to refund to the ebay buyer once message replied

##### Marketing

1. check how many compatitors

##### Development

1. testing/improving auto-ordering to amazon.com

----------------------------------------
#### 2015-11-19

##### Development

1. listing sold items - done
1. re-organize crontabs/scrapers - done
	- currently listed items
		- run_repricer.py - every hour
	- potential items
		- run_repricer_all.py - everyday - near midnight
		- run_repricer_sold.py - everyday - early morning
		- run_repricer_abs_prefd.py - everyday - near noon
		- run_bestseller.py - twice per week - near midnight

1. auto-ordering to amazon.com - phantomjs + casperjs - in progress
	- http://stackoverflow.com/a/24327791

----------------------------------------
#### 2015-11-18

##### Customer support

1. deal with re-invoicing - need to call ebay

##### Marketing

1. check how many compatitors

##### Development

1. auto-ordering to amazon.com - phantomjs + casperjs
	- http://stackoverflow.com/a/24327791

----------------------------------------
#### 2015-11-17

##### Marketing

1. check how many compatitors - still priceyak is the biggest compatitor

##### Development

1. auto-ordering to amazon.com - phantomjs + casperjs
	- http://stackoverflow.com/a/24327791

----------------------------------------
#### 2015-11-16

##### Marketing

1. check how many compatitors

##### Development

1. check ebay category issue - done
	- error code - 107, Category is not valid
	- e.g. title: 2 pack Seatbelt Cutter Window Breaker Emergency 
		- need to manually fix zz__a_to_e_category_maps table
1. trading error is not logging in db

----------------------------------------
### Week of 2015-11-08 - 2015-11-15

- scrapy amzn - complete migration
- move on to ebay notification listener

----------------------------------------
#### 2015-11-15

##### Development

1. scrape amazon and list new items
	- zz\_\_ebay\_store\_preferred\_categories
1. ebay notification listeners
	- add more listeners
		- on end list
1. auto-ordering to amazon.com - casperjs

----------------------------------------
#### 2015-11-14

##### Development

1. scrape amazon and list new items
	- zz\_\_ebay\_store\_preferred\_categories
1. ebay notification listeners
	- double check the error - done
	- add more listeners
		- on end list
1. auto-ordering to amazon.com - casperjs
1. graylog2 stability - improved

----------------------------------------
#### 2015-11-13

##### Development

1. tor + privoxy linode config check - done
1. amazon cd/dvd item scraping / breadcrumb.... - done
1. amazon keyword + category scraping - done
1. amazon_items - add column brand - done
1. add table - excl_brands - done
1. bug fix on ebay notification listners - done(?)

----------------------------------------
#### 2015-11-12

##### Development & Deployment

1. deploy and test
1. refactor php-soap/python-restful notif-listeners
1. implement more ebay notif-listeners

----------------------------------------
#### 2015-11-11

##### Development

1. setup tor + privoxy on production server
1. finalize ebay listing script - done
1. pricewatch script - done
	- use AmazonPricewatchSpider
1. migration:
	1. scrape amazon best sellers
	1. backup production db and copy into staging db
	1. migrate amazon\_items => zz\_\_amazon\_items
		- run /zz\_migration/mg\_amazon\_items.py
	1. migrate lookup\_ownerships => zz\_\_ebay\_store\_preferred\_categories
		- manual migration
	1. add more on zz\_\_ebay\_store\_preferred\_categories
	1. run listing at staging - for testing

1. (minor) log scraper errors in db

----------------------------------------
#### 2015-11-10

##### Development

1. zz\_\_preferred\_categories - done
1. setup tor + privoxy on production server
1. migrate old data to new database tables - partially done
	- grep all 'asin' from amazon\_items table
	- scrape with 'amazon\_asin' scraper
	- remove ebay\_items.amazon\_item\_id column (deprecated)
	- refactor /amazonmws/ebaystore/listing.py
		- with zz\_\_preferred\_categories table
	- refactor /amazonmws/monitor/amazon\_item\_monitor.py
		- use AmazonPricewatchSpider

1. (minor) log scraper errors in db

----------------------------------------
#### 2015-11-09

##### Development

1. scrapy + stem + privoxy + TOR - amazon.com scrape - done - now need to apply to production
			
		https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853

		https://github.com/aivarsk/scrapy-proxies (old)
		http://proxylist.hidemyass.com/ (old)		
		
		best practice:
		http://blog.privatenode.in/torifying-scrapy-project-on-ubuntu/
		https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
		
1. workaround copyright issue against ebay policy
1. new table zz\_\_amazon\_item\_offers

----------------------------------------

### Week of 2015-11-01 - 2015-11-07

- scrapy only based scraper
- amazon scrapy - best seller variation
- manual asin upload with csv

----------------------------------------
#### 2015-11-06

##### Marketing

1. DS Domination [http://dsdomination.com/](http://dsdomination.com/)

##### Development

1. set ip proxies - partially done... need to parse email and save IPs in database - disabled proxy middleware due to poor speed/conneciton. obay robots.txt instead... all /gp/offer-listing/ pages are blocked by robots.txt. considering TOR... for them
			
		https://github.com/aivarsk/scrapy-proxies
		http://proxylist.hidemyass.com/

1. set random user agents for scrapy - done with middleware
1. workaround copyright issue against ebay policy
1. column added in zz\_\_amazon\_items - done

		market_price
		merchant_id
		merchant_name

1. new table zz\_\_amazon\_item\_offers

----------------------------------------
#### 2015-11-05

##### Development

1. urgent!! - moved to next day
	- set ip proxies
			
			https://github.com/aivarsk/scrapy-proxies
			http://proxylist.hidemyass.com/
	- set random user agents for scrapy
	- workaround copyright issue against ebay policy

----------------------------------------
#### 2015-11-04

##### Development

1. scrapers
	- amazon best sellers - done
	- pricewatch (repricer) - done
1. ebay\_accounts (old ebay\_stores) - no need
	- ebay\_account\_preferences - no need

----------------------------------------
#### 2015-11-03

##### Development

1. scrapers
	- apply graylog - done
	- scraper for update/repricing amazon items (list of asin based scraper) - pretty much done
	- find/store ebay category id - done
		- related table: a\_to\_e\_category\_maps 

----------------------------------------
#### 2015-11-02

##### Development

1. scrapers - pretty much stabled...
	- scrapy only based amazon scraper

----------------------------------------
#### 2015-11-01

##### Development

1. scrapers - on progress
	- scrapy only based amazon scraper

----------------------------------------
#### 2015-10-30

##### Development - let's fix all issues today

1. ebay notification
	- store information to db on transaction complete
1. cronjob setup on app server - finally found the issue!
1. scrapers
	- research scrapy + scrapyd, and start refactoring
		- scrapyd is not very necessary at this time...
	- better try scrapy with looking after XHR requests [http://stackoverflow.com/a/8594831](http://stackoverflow.com/a/8594831)
	- refactor scrapers - using scrapy only. pull out selenium + phantomjs... too slow

----------------------------------------
#### 2015-10-29

##### ebay Compatible Application Check

1. approved!!

##### Development

1. new amazon item status - excluded - done
	- should not be updated/listed
	- need to update related ebay items entry as well - set to inactive
1. ebay notification - almost done - need to find a small bug to fix
	- build 'transactions' db table based on ebay provided information
1. cronjob setup on app server
	- might need to use python schedule instead (crontab cannot run python script. don't know why)
	- investigate more why cronjob doesn't work...
1. scrapers
	- research scrapy + scrapyd, and start refactoring
	- multi-thread scraping needed.

----------------------------------------
#### 2015-10-28

##### ebay store marketing

1. limit raised to 175 items!

##### ebay Compatible Application Check

1. must submit the application by completing the form 'app check' - application submitted on Oct 29th 6AM

##### BUG ON PRODUCTION

1. update all ebay item description - reached api limit. postpond to tomorrow. should apply [Compatible Application Check](https://go.developer.ebay.com/compatible-application-check-and-checklist-going-live)
	- related links
		- [http://developer.ebay.com/DevZone/guides/ebayfeatures/basics/Call-UsingLiveData.html#CompatibleApplicationCheck](http://developer.ebay.com/DevZone/guides/ebayfeatures/basics/Call-UsingLiveData.html#CompatibleApplicationCheck)
		- [https://go.developer.ebay.com/introduction-logos](https://go.developer.ebay.com/introduction-logos)
	- use / modify revise_items.py

##### Development

1. complete bakjin's listing - done, but need to revise descriptions
1. cronjob (or python schedule) for tasks
1. ebay notification
	- debug object transferred to php soap
	- watch any receiving notifications
	- handle ItemSold/FixedPriceTransaction/AuctionCheckoutComplete events

----------------------------------------
#### 2015-10-27

##### ebay store marketing

1. refresh all items - done

##### Development

1. ebay notification - still learning ebay information
	- watch any receiving notifications
	- handle ItemSold/FixedPriceTransaction/AuctionCheckoutComplete events
1. scrapers - research scrapy + scrapyd, and start refactoring - multi-thread scraping...
1. cronjob setup on app server - need to implement lock files for each tasks - avoid any over-runs - going to use python schedule instead (crontab cannot run python script. don't know why)

----------------------------------------
#### 2015-10-26

##### ebay store marketing

1. call and increase limit - cannot made today. should call back on Friday (Oct 30th)
1. send thank you messages to buyers - done

##### Development

1. ebay notification
	- setup on linode - done (both soap/restful. restrict restful access by ip)
	- event handling - ItemSold - failed to receive notifications..
1. need to improve amazon.com scraper - filter prime at list screens... - takes a lot of time to go over each detail screens... - need to improve all scrapers! (very slow)

----------------------------------------
#### 2015-10-25

##### Development

1. setup bakjin's account
	- improve scraper - get ebay category id based on 1) amazon category or 2) title at scraping - done
	- create table ebay\_store\_profiles, and improve ebay store feature - postponed

----------------------------------------
#### 2015-10-24

##### Deployment

1. install blueprint at linode appserver and reverse-engineering and build shell script file. - done

----------------------------------------
#### 2015-10-23

##### Developments / Deployment

1. write shell script - securing_server.sh - done
1. deploy app server to linode - done
1. deploy log server to linode - done

----------------------------------------
#### 2015-10-22

##### Developments

1. move config to root directory - done
1. make sure every scripts should be runnable via physical path - done
1. setup apache server config for both php soap and python restful servers (Macaw for php routing) - done
1. scrapyd for demonizing scrapy spiders
	- using alternative solution for now (cronjob)
		- ref: [http://stackoverflow.com/a/17235906](http://stackoverflow.com/a/17235906)
1. prepare to push the servers/task scripts to live
1. setup linode server

----------------------------------------
#### 2015-10-21

##### Developments

1. soap (php) + restful (python) application - done for the infrastructure

----------------------------------------
#### 2015-10-20

##### Developments

1. must filter add-on items from amazon - done
1. patch to update all amazon pictures - done
1. notification workflow:
	1. receive solditem notification from ebay
	1. store information in db, and do follow-up action

1. if I use php soap server: - on progress
	- pro 
		- may use example - server should work fine...
	- cons 
		- need to maintain 2 different code bases
	- how to minimize the maintenance?
	- must make bridge system with php soap + python restful...
	- 
1. scrape watchcount.com
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com

----------------------------------------
#### 2015-10-19

##### Developments

1. soap server + handling ebay notifications - with *pysimplesoap* lib - not successful (no headers tag support)
1. scrape watchcount.com
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com


----------------------------------------
#### 2015-10-18

##### Developments

1. soap server + handling ebay notifications - failed to implement *spyne* lib 
1. scrape watchcount.com - cannot even started
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com

----------------------------------------
#### 2015-10-16

##### Bigger plans / todos

1. improve scraper, monitoring system
1. transfer to linode server
1. improve mapping amazon category/items to ebay category - improved with rake
1. soap server + handling ebay notifications
1. amazon ordring automation - casperjs

##### Developments

1. improve scraper and item monitering system
	- one scraper for just collect amazon asin - selenium / phantomjs
	- one scraper for go over all amazon detail screen - scrapy
1. need to find a way to mapping amazon category and ebay category - improved with RAKE (Rapid Automatic Keyword Extraction algorithm) - [https://pypi.python.org/pypi/python-rake/1.0.5](https://pypi.python.org/pypi/python-rake/1.0.5), [https://github.com/aneesha/RAKE](https://github.com/aneesha/RAKE)

----------------------------------------
#### 2015-10-15

##### Developments

1. setting up bakjin's application - improve application with site based
	- category/keyword based amazon item scraper - done
	- ebay application api with multiple users / tokens - done
	- setup linode servers - both application server, log server

----------------------------------------
#### 2015-10-14

##### ebay store marketing / accounting

1. list the vaccum on ebay - done
1. post a comment on redflagdeals.com - done
	- [http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963](http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963)

##### Developments

1. setting up bakjin's application - improve application with site based
1. setup linode servers - both application server, log server


----------------------------------------
#### 2015-10-13

##### Developments

1. setting up bakjin's application - improve application with site based - on progress
1. setup linode servers - both application server, log server


----------------------------------------
#### 2015-10-10

##### ebay store marketing / accounting

1. proceed ebay item sold
	- questions: 
		- gyft.com cannot verify my mobile number. left a ticket - on process
		- amazon asks phone number of shipping information on checkout. may I give my phone number instead? - found buyer's phone number from **ebay.ca** management tool.

##### Developments

1. Auto-ordering - again...
	- soap with Spyne
	- navigate through amazon.com - must use casperjs, testing purpose. have to notify us as soon as possible


----------------------------------------
#### 2015-10-09

##### ebay store marketing

1. research more about sales tax

##### Developments

1. Auto-ordering
	- soap with Spyne
	- navigate through amazon.com


----------------------------------------
#### 2015-10-08

##### ebay store marketing

1. keep raising ebay feedbacks - done - 11 points

1. call ebay once feedback points get 10
	- called, but not resolved. received a ref# - 1-55275826862 - and will be resolved in 72 hours

1. meeting tonight, so what to ask:
	- monthly profit, monthly transaction - wbjworld
	- marketing other than feedbacks - pretty much nothing else than feedbacks
	- my items are not searchable, neither thecandidcow's ones are - wbjworld - not searchable either
	- notes:
		- purchase amazon gift card from [gyft.com]() - 2% cach back with paypal payment
		- [givingassistant.org]() - donation site - affiliation - 5% cash back on purchasing at amazon.com
		- tax rates depends on States

##### Developments

1. improve ebay api error handling - ebay\_trading\_api\_errors table - done

1. again... Auto-ordering, Auto-ordering, Auto-ordering!!!
	- soap is crazy... - understood pretty much
	- scrape and navigate amazon... - not yet


----------------------------------------
#### 2015-10-07

##### ebay store marketing

1. keep raising ebay feedbacks - 7 points so far

##### Developments

1. Auto-ordering, Auto-ordering, Auto-ordering!!!


----------------------------------------
#### 2015-10-06

##### ebay store marketing

1. keep raising ebay feedbacks - 4 points so far

##### Developments

1. update shipping policy template - done
	- add express shipping for $1.99 - extra money
	- make PO BOX available - but it will slow down your shipping - about 1-2 business days.

1. build automatic ordering system
	- check CasperJS
	- benchmark PriceYak


----------------------------------------
#### 2015-10-05

##### ebay Store / paypal business account

1. call paypal to verify bank account and credit card - not necessary

1. call ebay about my listings not searchable at ebay.com - done

1. switch linked paypal account at ebay.ca - not necessary

1. raising ebay feedbacks

1. go though ebay store marketing section

##### Developments

1. simplify amazon item monitoring system - merge amazon item price and amazon item status into a single process - need to test more

1. run the script on production


----------------------------------------
#### 2015-10-02

##### ebay Store

1. confirm Bank Account at paypal - done

1. subscribe to ebay Store Basic - done

1. work on ebay store settings
	- logo - done
	- search keywords - use google tool - done

##### Developments

1. monitor amazon item status changes - done

1. item inventory / quantity control - done

1. ebay notification
	- references
		- [http://developer.ebay.com/Devzone/guides/ebayfeatures/Notifications/Notifications.html]()
		- [http://developer.ebay.com/Devzone/XML/docs/HowTo/Notifications/Notifications_listing.html]()

	- using ebay_item_quantity.py scraper instead - done
		
1. create html template for item description - done
	- http://developer.ebay.com/DevZone/guides/ebayfeatures/Development/DescTemplates.html
	- use twitter bootstrap