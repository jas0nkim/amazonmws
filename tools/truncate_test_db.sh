#!/bin/bash
stty -echo
printf "database password? "
read INPUT_PASS
stty echo
printf "\n"

TABLE_NAMES=("amazon_items" "amazon_item_pictures" "ebay_items" "ebay_listing_errors" "item_price_history" "item_status_history" "scraper_amazon_items")

for t in "${TABLE_NAMES[@]}"
do
	echo "Proceessing $t database table..."

	mysql -u atewriteuser -p$INPUT_PASS amazonmws -e "TRUNCATE TABLE $t;"
done
