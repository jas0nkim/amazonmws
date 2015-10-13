# Automation


## note

- listing at ebay
- stock check at amazon
- price check at amazon

==> update to ebay list


- once order comes in at ebay store, must show on dashboard (my own)
- show amazon link - order now button with given order detail information


- whenever amazon description/price/status changed, update to ebay right away

- best_seller_spider : 


## workflow / features

#### discover amazon best seller items

- related db tables:
	- amazon\_items
	- amazon\_item\_pictures
	- scraper\_amazon\_items
- scrape amazon best seller items / special query items and their pictures, and store in database amazon\_items, amazon\_item\_pictures
	- i.e. scrapy crawl bestsellers_toysandgames


#### list an item to ebay store

- related db tables:
	- scraper\_amazon\_items
	- amazon\_items
	- amazon\_item\_pictures
	- ebay\_items
	- ebay\_listing\_errors
- go throw amazon\_items and ebay\_items and find any unlisted items and OOS items on ebay
	- conditions:
		- amazon\_items.status = 1 (active)
		- no ebay items entry yet or ebay\_items.status = 2
- listing
	- check whether already listed on ebay (but OOS)
		- if yes:
			1. update with ebay api - **ReviseInventoryStatus**
			1. then update related tables - ebay\_items.status = 1 (active), log item\_quantity\_history
		- if no:
			1. use ebay api - **findItemsAdvanced** - to get ebay category (leaf) for the amazon item
				- if no category found, log the amazon item id / asin information in seperated database - unlisted\_amazon\_items
			1. calculate desired / listing price at ebay
				- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
			1. then use **VerifyAddFixedPriceItem** to verify before listing item on ebay
				- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
			1. then use **UploadSiteHostedPictures** to upload pictures to ebay
				- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
			1. finally use **AddFixedPriceItem** to list amazon item to ebay and store ebay\_items with ebid (ebay item id), ebay category id, and my price at ebay
				- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items


#### monitor amazon item status / price / review count / average rating changes Ver.2

##### active amazon items
- merge *monitor amazon item price changes Ver.1* and *monitor amazon item status changes Ver.1*
- related db tables:
	- amazon\_items
	- amazon\_item\_status\_history
	- amazon\_item\_price\_history
	- ebay\_items
	- ebay\_listing\_errors
- procedure
	1. go throw amazon\_items and find any price or status changes
		- status check - is FBA or not, OOS?
		- price check - has changed?
		- update review count
		- update average rating
	1. if the amazon item is not available or not FBA any longer:
		- make sure to check other sellers as well to click via 'new' link
		- then end ebay listing with ebay api - **EndItem** - if necessary
		- update ebay\_items status
		- log at amazon\_item\_status\_history
		- then list another amazon item to ebay - refer *list an item to ebay store*
	1. if the amazon item does not have enough stock or out of stock:
		- **TODO: check other sellers as well**
		- then set ebay item quantity to 0 with ebay api -**ReviseInventoryStatus** - if necessary
		- log at amazon\_item\_status\_history
	1. if the amazon item price has been changed:
		- make sure to check other sellers as well to click via 'new' link
		- update ebay price with ebay api - **ReviseInventoryStatus** - if necessary
		- update ebay\_items.eb_price column
		- log at amazon\_item\_price\_history
	1. update review count
	1. update average rating

##### TODO: out of stock amazon items
- procedure
	1. go throw all OOS amazon\_items
	1. if the stock is enough:
		- check the price has been changed as well
		- update amazon\_items.status column - and price column if necessary
		- log at amazon\_item\_status\_history - and at amazon\_item\_price\_history if necessary


#### ebay item inventory / quantity control
**TODO: need to improve this functionality - due to OOS feature**

- related db tables:
	- ebay\_items
	- item\_quantity\_history
- procedure
	1. go throw all active ebay items, and scrape the ebay item page: settings.EBAY_ITEM_LINK_PREFIX + ebid
	2. update with ebay api - **ReviseInventoryStatus**
	3. then update related tables


#### TODO: Set ebay Platform notification for application

- related db tables:
	- ebay\_notificaion\_errors
- set notification with ebay api - **SetNotificationPreferences**


#### TODO: Auto-ordering
	

#### TODO: need to improve html template for item description

- [http://developer.ebay.com/DevZone/guides/ebayfeatures/Development/DescTemplates.html]()
- use twitter bootstrap


#### TODO: improve ebay\_listing\_errors table

- make more generic - ebay\_listing\_errors --> ebay\_trading\_api\_errors
- store by MessageID - key
- store any ebay api errors/warnings
- store all messages
- store related asin/ebid if available


*DEPRECATED*

<del>monitor amazon item price changes Ver.1</del>

- related db tables:
	- amazon\_items
	- amazon\_item\_price\_history
	- ebay\_items
- procedure
	1. use amazon api - **GetCompetitivePricingForASIN**
		- fallback scrape amazon url to check the price.
	2. if any price changes, update ebay price with ebay api - **ReviseItem**
	3. then log at amazon\_item\_price\_history, and update price value at amazon\_items and ebay\_items


*DEPRECATED*

<del>monitor amazon item status changes Ver.1</del>

- related db tables:
	- amazon\_items
	- amazon\_item\_status\_history
	- ebay\_items
- procedure
	1. go throw amazon\_items and find any status changes
		- <del>the link (asin) still available</del> *removed (not realiable, and FBA check still handles this)*
		- is still FBA?
		- **TODO: is out of stock?**
	2. if the amazon item is not available or not FBA any longer, log at amazon\_item\_status\_history
	3. then end ebay listing with ebay api - **EndItem**


*DEPRECATED*

<del>(not necessary) relist ebay items via ebay notification</del>

- related db tables:
	- ebay\_items
	- item\_status\_history
	- ebay\_notificaion\_errors
- related ebay notification
	- **ItemClosed**
- relist 


## available commands

##### scrape amazon.com by keywoards - kids custume
	scrapy crawl keywords_kidscustume

##### scrape amazon.com best sellers - toys and games
	scrapy crawl bestsellers_toysandgames
	
##### list items to ebay
	python /path/to/amazonmws/amazonmws/ebaystore/listing.py

##### monitor FBA item status / price changes and update if nessessary
	python /path/to/amazonmws/amazonmws/monitor/amazon_item_monitor.py

##### monitor item quantity changes at ebay and update if nessessary
	python /path/to/amazonmws/amazonmws/monitor/ebay_item_quantity.py

*DEPRECATED*

<del>monitor item price changes from amazon and update if nessessary</del>

	python /path/to/amazonmws/amazonmws/monitor/amazon_item.py


*DEPRECATED*

<del>monitor item status changes from amazon and update if nessessary</del>

	python /path/to/amazonmws/amazonmws/monitor/amazon_item_status.py

