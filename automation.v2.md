# Automation V2.0 (improved scraping)

### new database tables

1. **zz\_\_amazon\_items**

1. **zz\_\_amazon\_item\_pictures**

1. **zz\_\_ebay\_item\_pictures**

		id
		amazon_item_picture_id
		asin
		picture_url
		created_at
		updated_at
		ts

1. **zz\_\_a\_to\_e\_category\_maps**
	- update this table on amazon item scraping..

			id
			amazon_category
			ebay_category_id
			ebay_category_name
			created_at
			updated_at
			ts

1. **zz\_\_amazon\_bestsellers**
	- update once a week
 
			id
			asin
			bestseller_category
			rank
			created_at
			updated_at
			ts

1. **zz\_\_amazon\_bestsellers_archived**
	- copy from zz\_\_amazon\_bestsellers - once a week - just before updating zz\_\_amazon\_bestsellers table 
	- **note: zz\_\_amazon\_bestsellers.updated\_at = zz\_\_amazon\_bestsellers_archived.created\_at**

			id
			asin
			bestseller_category
			rank
			created_at
			ts

