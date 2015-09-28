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

- **discover amazon best seller items**
	- related db tables:
		- amazon\_items
		- amazon\_item\_pictures
		- scraper\_amazon\_items
	- scrape amazon best seller items / special query items and their pictures, and store in database amazon\_items, amazon\_item\_pictures
		- i.e. scrapy crawl bestsellers_toysandgames

- **list an item to ebay store**
	- related db tables:
		- scraper\_amazon\_items
		- amazon\_items
		- amazon\_item\_pictures
		- ebay\_items
		- unlisted\_amazon\_items
	- go throw amazon\_items and ebay\_items and find any unlisted items on ebay
		- conditions:
			- amazon\_items.status = 1 (active)
	- listing
		1. use ebay api - **findItemsAdvanced** - to get ebay category (leaf) for the amazon item
			- if no category found, log the amazon item id / asin information in seperated database - unlisted\_amazon\_items
		1. calculate desired / listing price at ebay
			- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
		1. then use **VerifyAddFixedPriceItem** to verify before listing item on ebay
			- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
		1. then use **UploadSiteHostedPictures** to upload  pictures to ebay
			- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items
		1. finally use **AddFixedPriceItem** to list amazon item to ebay and store ebay\_items with ebid (ebay item id), ebay category id, and my price at ebay
			- if error occurs, log the amazon item id / asin in unlisted\_amazon\_items

- **TODO: need to create html template for item description**
	- http://developer.ebay.com/DevZone/guides/ebayfeatures/Development/DescTemplates.html
	- use twitter bootstrap

- **monitor amazon item price changes**
	- related db tables:
		- amazon\_items
		- amazon\_item\_price\_history
		- ebay\_items
	- procedure
		1. use amazon api - **GetCompetitivePricingForASIN**
			- fallback scrape amazon url to check the price.
		2. if any price changes, log at amazon\_item\_price\_history, and update price value at amazon\_items
		3. then update ebay price with ebay api - **ReviseItem**

- **monitor amazon item status changes**
	- related db tables:
		- amazon\_items
		- amazon\_item\_status\_history
		- ebay\_items
	- procedure
		1. go throw amazon\_items and find any status chages
			- the link (asin) still available?
			- is still FBA?
		2. if the amazon item is not available or not FBA any longer, log at amazon\_item\_status\_history
		3. then end ebay listing with ebay api - **EndItem**


- **TODO: relist ebay items via ebay notification**

- **TODO: order handling via ebay notification**