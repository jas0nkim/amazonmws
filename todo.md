# Plans

### Week of 2016-10-23 - 2016-10-29

- store ebay pictures - too much calling UploadSiteHostedPictures... wasting ebay api quota and time...
	- db tables
		- ebay_picture_services (new)
			source_picture_url
			picture_url
			base_url
			full_url
			created_at
			updated_at
		- ebay_picture_set_members (new)
			ebay_picture_services_id
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
	- phase 2:
		- updates ebay item's title/description only if amazon source updated

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