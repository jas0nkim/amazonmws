#!/bin/bash
stty -echo
printf "database password? "
read INPUT_PASS
stty echo
printf "\n"

TABLE_NAMES=("zz__a_to_e_category_maps" "zz__amazon_bestsellers" "zz__amazon_bestsellers_archived" "zz__amazon_item_offers" "zz__amazon_item_pictures" "zz__amazon_items" "zz__ebay_store_preferred_categories")

for t in "${TABLE_NAMES[@]}"
do
	echo "Proceessing $t database table..."

	mysql -u atewriteuser -p$INPUT_PASS amazonmws -e "TRUNCATE TABLE $t;"
done
