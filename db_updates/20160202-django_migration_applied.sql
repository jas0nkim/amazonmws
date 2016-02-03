-- amazon_bestsellers
ALTER TABLE `amazon_bestsellers` DROP INDEX `index_zz__amazon_bestsellers_asin`;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `bestseller_category_url` longtext NOT NULL;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `asin` varchar(32) NOT NULL;
ALTER TABLE `amazon_bestsellers` ALTER COLUMN `asin` DROP DEFAULT;
CREATE INDEX `amazon_bestsellers_62130e1b` ON `amazon_bestsellers` (`asin`);
ALTER TABLE `amazon_bestsellers` ADD CONSTRAINT `amazon_bestsellers_asin_27274c9c_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_items
ALTER TABLE `amazon_items` MODIFY COLUMN `url` longtext NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `title` longtext NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `price` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `market_price` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `quantity` smallint NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `features` longtext NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `description` longtext NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `avg_rating` double precision NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `is_fba` bool NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `is_addon` bool NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `is_pantry` bool NOT NULL;

-- amazon_item_offers
ALTER TABLE `amazon_item_offers` MODIFY COLUMN `is_fba` bool NOT NULL;
ALTER TABLE `amazon_item_offers` MODIFY COLUMN `asin` varchar(32) NOT NULL;
ALTER TABLE `amazon_item_offers` ALTER COLUMN `asin` DROP DEFAULT;
ALTER TABLE `amazon_item_offers` ADD CONSTRAINT `amazon_item_offers_asin_e7ef0260_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_item_pictures
ALTER TABLE `amazon_item_pictures` ADD CONSTRAINT `amazon_item_pictures_asin_7a2b328d_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- a_to_e_category_maps
ALTER TABLE `a_to_e_category_maps` MODIFY COLUMN `ebay_category_id` varchar(100) NOT NULL;
ALTER TABLE `a_to_e_category_maps` ALTER COLUMN `ebay_category_id` DROP DEFAULT;
CREATE INDEX `a_to_e_category_maps_3b7506d9` ON `a_to_e_category_maps` (`ebay_category_id`);
ALTER TABLE `a_to_e_category_maps` ADD CONSTRAINT `e16d07189a0f0e635d30468faf6048bb` FOREIGN KEY (`ebay_category_id`) REFERENCES `ebay_product_categories` (`category_id`);

-- ebay_stores
ALTER TABLE `ebay_stores` MODIFY COLUMN `token` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `margin_max_dollar` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `listing_min_dollar` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `listing_max_dollar` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `policy_shipping` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `policy_payment` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `policy_return` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `returns_accepted` bool NOT NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `use_salestax_table` bool NOT NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `item_description_template` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `feedback_comment` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `message_on_shipping_subject` longtext NULL;
ALTER TABLE `ebay_stores` MODIFY COLUMN `message_on_shipping_body` longtext NULL;

-- ebay_store_amazon_accounts to amazon_accounts_ebay_stores
RENAME TABLE `ebay_store_amazon_accounts` TO `amazon_accounts_ebay_stores`;
ALTER TABLE `ebay_store_amazon_accounts` DROP INDEX `ebay_store_amazon_accounts_ebay_store_id`;
ALTER TABLE `ebay_store_amazon_accounts` DROP INDEX `ebay_store_amazon_accounts_amazon_account_id`;
ALTER TABLE `amazon_accounts_ebay_stores` CHANGE COLUMN `amazon_account_id` `amazonaccount_id` integer NOT NULL;
ALTER TABLE `amazon_accounts_ebay_stores` CHANGE COLUMN `ebay_store_id` `ebaystore_id` integer NOT NULL;
ALTER TABLE `amazon_accounts_ebay_stores` DROP COLUMN `created_at`;
ALTER TABLE `amazon_accounts_ebay_stores` DROP COLUMN `updated_at`;
ALTER TABLE `amazon_accounts_ebay_stores` DROP COLUMN `ts`;
