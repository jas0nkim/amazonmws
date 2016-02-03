BEGIN;

-- amazon_bestsellers
ALTER TABLE `amazon_bestsellers` DROP INDEX `index_zz__amazon_bestsellers_asin`;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `bestseller_category_url` longtext NOT NULL;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `asin` varchar(32) NOT NULL;
ALTER TABLE `amazon_bestsellers` ALTER COLUMN `asin` DROP DEFAULT;

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

-- amazon_item_pictures

-- a_to_e_category_maps
ALTER TABLE `a_to_e_category_maps` MODIFY COLUMN `ebay_category_id` varchar(100) NOT NULL;
ALTER TABLE `a_to_e_category_maps` ALTER COLUMN `ebay_category_id` DROP DEFAULT;

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

-- ebay_items
ALTER TABLE `ebay_items` MODIFY COLUMN `eb_price` numeric(15, 2) NOT NULL;
ALTER TABLE `ebay_items` MODIFY COLUMN `ebay_category_id` varchar(100) NOT NULL;

-- ebay_store_preferred_categories
ALTER TABLE `ebay_store_preferred_categories` MODIFY COLUMN `category_type` varchar(17) NOT NULL;
ALTER TABLE `ebay_store_preferred_categories` MODIFY COLUMN `status` smallint NULL;

-- excl_brands
ALTER TABLE `excl_brands` MODIFY COLUMN `category` longtext NULL;

-- amazon_orders
ALTER TABLE `amazon_orders` MODIFY COLUMN `item_price` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_orders` MODIFY COLUMN `shipping_and_handling` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_orders` MODIFY COLUMN `tax` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_orders` MODIFY COLUMN `total` numeric(15, 2) NOT NULL;

-- transactions
ALTER TABLE `transactions` MODIFY COLUMN `transaction_price` numeric(15, 2) NOT NULL;
ALTER TABLE `transactions` MODIFY COLUMN `sales_tax_percent` numeric(5, 2) NULL;
ALTER TABLE `transactions` MODIFY COLUMN `sales_tax_amount` numeric(15, 2) NULL;
ALTER TABLE `transactions` MODIFY COLUMN `amount_paid` numeric(15, 2) NOT NULL;
ALTER TABLE `transactions` MODIFY COLUMN `raw_item` longtext NULL;
ALTER TABLE `transactions` MODIFY COLUMN `raw_transactionarray` longtext NULL;
ALTER TABLE `transactions` MODIFY COLUMN `raw_xml` longtext NULL;

-- ebay_notification_errors
ALTER TABLE `ebay_notification_errors` MODIFY COLUMN `response` longtext NULL;
ALTER TABLE `ebay_notification_errors` MODIFY COLUMN `description` longtext NULL;

-- ebay_trading_api_errors
ALTER TABLE `ebay_trading_api_errors` DROP INDEX `index_ebay_trading_api_errors_amazon_item_id`;
ALTER TABLE `ebay_trading_api_errors` DROP INDEX `index_ebay_trading_api_errors_ebay_item_id`;
ALTER TABLE `ebay_trading_api_errors` DROP COLUMN `amazon_item_id`;
ALTER TABLE `ebay_trading_api_errors` DROP COLUMN `ebay_item_id`;
ALTER TABLE `ebay_trading_api_errors` MODIFY COLUMN `request` longtext NULL;
ALTER TABLE `ebay_trading_api_errors` MODIFY COLUMN `response` longtext NULL;
ALTER TABLE `ebay_trading_api_errors` MODIFY COLUMN `description` longtext NULL;

-- error_ebay_invalid_category
ALTER TABLE `error_ebay_invalid_category` MODIFY COLUMN `request` longtext NULL;


--
-- indexes and foreignkey constraints
--

-- amazon_bestsellers
CREATE INDEX `amazon_bestsellers_62130e1b` ON `amazon_bestsellers` (`asin`);
ALTER TABLE `amazon_bestsellers` ADD CONSTRAINT `amazon_bestsellers_asin_27274c9c_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_item_offers
ALTER TABLE `amazon_item_offers` ADD CONSTRAINT `amazon_item_offers_asin_e7ef0260_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_item_pictures
ALTER TABLE `amazon_item_pictures` ADD CONSTRAINT `amazon_item_pictures_asin_7a2b328d_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_item_pictures
CREATE INDEX `a_to_e_category_maps_3b7506d9` ON `a_to_e_category_maps` (`ebay_category_id`);
ALTER TABLE `a_to_e_category_maps` ADD CONSTRAINT `e16d07189a0f0e635d30468faf6048bb` FOREIGN KEY (`ebay_category_id`) REFERENCES `ebay_product_categories` (`category_id`);

-- ebay_items
ALTER TABLE `ebay_items` ADD CONSTRAINT `ebay_items_asin_ddfe7985_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);
ALTER TABLE `ebay_items` ADD CONSTRAINT `D8dc21e57266c5192e0982f1b3113fea` FOREIGN KEY (`ebay_category_id`) REFERENCES `ebay_product_categories` (`category_id`);
ALTER TABLE `ebay_items` ADD CONSTRAINT `ebay_items_ebay_store_id_fe53255b_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);

-- ebay_store_preferred_categories
ALTER TABLE `ebay_store_preferred_categories` ADD CONSTRAINT `ebay_store_preferred_ca_ebay_store_id_477c9394_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);

-- amazon_orders
ALTER TABLE `amazon_orders` ADD CONSTRAINT `amazon_orders_amazon_account_id_913c5107_fk_amazon_accounts_id` FOREIGN KEY (`amazon_account_id`) REFERENCES `amazon_accounts` (`id`);
ALTER TABLE `amazon_orders` ADD CONSTRAINT `amazon_orders_asin_4839d969_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- transactions
ALTER TABLE `transactions` ADD CONSTRAINT `transactions_item_id_6817dd0b_fk_ebay_items_ebid` FOREIGN KEY (`item_id`) REFERENCES `ebay_items` (`ebid`);
ALTER TABLE `transactions` ADD CONSTRAINT `transactions_seller_user_id_6db9864b_fk_ebay_stores_username` FOREIGN KEY (`seller_user_id`) REFERENCES `ebay_stores` (`username`);

-- ebay_notification_errors
ALTER TABLE `ebay_notification_errors` ADD CONSTRAINT `ebay_notification_error_ebay_store_id_d7e08626_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);

-- ebay_trading_api_errors
ALTER TABLE `ebay_trading_api_errors` ADD CONSTRAINT `ebay_trading_api_errors_asin_123d7ef6_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);
ALTER TABLE `ebay_trading_api_errors` ADD CONSTRAINT `ebay_trading_api_errors_ebid_67f91b0a_fk_ebay_items_ebid` FOREIGN KEY (`ebid`) REFERENCES `ebay_items` (`ebid`);

-- error_ebay_invalid_category
ALTER TABLE `error_ebay_invalid_category` ADD CONSTRAINT `error_ebay_invalid_category_asin_166b2a2f_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);
ALTER TABLE `error_ebay_invalid_category` ADD CONSTRAINT `a4a84c858278b68ea946879d6b57ab23` FOREIGN KEY (`ebay_category_id`) REFERENCES `ebay_product_categories` (`category_id`);

COMMIT;