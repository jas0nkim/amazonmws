BEGIN;
--
-- Create model AliexpressCategory
--
CREATE TABLE `aliexpress_categories` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL,
    `category_id` varchar(100) NOT NULL,
    `category_name` varchar(100) NULL,
    `parent_category_id` varchar(100) NULL,
    `parent_category_name` varchar(100) NULL,
    `root_category_id` varchar(100) NULL,
    `root_category_name` varchar(100) NULL,
    `is_leaf` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressItem
--
CREATE TABLE `aliexpress_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL, `url` varchar(255) NULL,
    `store_id` varchar(100) NOT NULL,
    `store_name` varchar(255) NULL,
    `store_location` varchar(255) NULL,
    `store_opened_since` varchar(255) NULL,
    `category_id` varchar(100) NULL,
    `category_name` varchar(255) NULL,
    `category` varchar(255) NULL,
    `title` varchar(255) NULL,
    `market_price` numeric(15, 2) NOT NULL,
    `price` numeric(15, 2) NOT NULL,
    `quantity` smallint NULL,
    `specifications` longtext NULL,
    `pictures` longtext NULL,
    `review_count` smallint NULL,
    `review_rating` double precision NULL,
    `orders` smallint NULL,
    `status` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressItemApparel
--
CREATE TABLE `aliexpress_item_apparels` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL,
    `size_chart` longtext NULL,
    `status` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressItemDescription
--
CREATE TABLE `aliexpress_item_descriptions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL,
    `description` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressItemShipping
--
CREATE TABLE `aliexpress_item_shippings` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL,
    `country_code` varchar(100) NOT NULL,
    `has_epacket` bool NOT NULL,
    `epacket_cost` numeric(15, 2) NOT NULL,
    `epacket_estimated_delivery_time_min` smallint NULL,
    `epacket_estimated_delivery_time_max` smallint NULL,
    `epacket_tracking` bool NOT NULL,
    `all_options` longtext NULL,
    `status` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressItemSku
--
CREATE TABLE `aliexpress_item_skus` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alxid` varchar(100) NOT NULL,
    `sku` varchar(255) NOT NULL,
    `market_price` numeric(15, 2) NOT NULL,
    `price` numeric(15, 2) NOT NULL,
    `quantity` smallint NULL,
    `specifications` longtext NULL,
    `pictures` longtext NULL,
    `bulk_price` numeric(15, 2) NOT NULL,
    `bulk_order` smallint NULL,
    `raw_data` longtext NULL,
    `status` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressStore
--
CREATE TABLE `aliexpress_stores` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `store_name` varchar(255) NULL,
    `store_id` varchar(100) NULL,
    `owner_member_id` varchar(100) NULL,
    `store_location` varchar(255) NULL,
    `store_opened_since` date NULL,
    `deliveryguarantee_days` varchar(100) NULL,
    `return_policy` varchar(255) NULL,
    `is_topratedseller` bool NOT NULL,
    `has_buyerprotection` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressStoreFeedback
--
CREATE TABLE `aliexpress_store_feedbacks` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `store_id` varchar(100) NOT NULL,
    `feedback_score` smallint NULL,
    `feedback_percentage` double precision NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AliexpressStoreFeedbackDetailed
--
CREATE TABLE `aliexpress_store_feedbacks_detailed` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `store_id` varchar(100) NOT NULL,
    `itemasdescribed_score` double precision NULL,
    `itemasdescribed_ratings` smallint NULL,
    `itemasdescribed_percent` double precision NULL,
    `communication_score` double precision NULL,
    `communication_ratings` smallint NULL,
    `communication_percent` double precision NULL,
    `shippingspeed_score` double precision NULL,
    `shippingspeed_ratings` smallint NULL,
    `shippingspeed_percent` double precision NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Create model AlxToEbayCategoryMap
--
CREATE TABLE `alx_to_ebay_category_maps` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `aliexpress_category` varchar(255) NULL,
    `ebay_category_id` varchar(100) NULL,
    `ebay_category_name` varchar(255) NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);


CREATE INDEX `aliexpress_categories_b97d4ab0` ON `aliexpress_categories` (`alxid`);
CREATE INDEX `aliexpress_categories_b583a629` ON `aliexpress_categories` (`category_id`);
CREATE INDEX `aliexpress_categories_2263e5df` ON `aliexpress_categories` (`parent_category_id`);
CREATE INDEX `aliexpress_categories_ed61d628` ON `aliexpress_categories` (`root_category_id`);
CREATE INDEX `aliexpress_items_b97d4ab0` ON `aliexpress_items` (`alxid`);
CREATE INDEX `aliexpress_items_7473547c` ON `aliexpress_items` (`store_id`);
CREATE INDEX `aliexpress_items_b583a629` ON `aliexpress_items` (`category_id`);
CREATE INDEX `aliexpress_item_apparels_b97d4ab0` ON `aliexpress_item_apparels` (`alxid`);
CREATE INDEX `aliexpress_item_descriptions_b97d4ab0` ON `aliexpress_item_descriptions` (`alxid`);
CREATE INDEX `aliexpress_item_shippings_b97d4ab0` ON `aliexpress_item_shippings` (`alxid`);
CREATE INDEX `aliexpress_item_shippings_55eceb8d` ON `aliexpress_item_shippings` (`country_code`);
CREATE INDEX `aliexpress_item_skus_b97d4ab0` ON `aliexpress_item_skus` (`alxid`);
CREATE INDEX `aliexpress_item_skus_f8c461fd` ON `aliexpress_item_skus` (`sku`);
CREATE INDEX `aliexpress_stores_7473547c` ON `aliexpress_stores` (`store_id`);
CREATE INDEX `aliexpress_stores_9adb17cb` ON `aliexpress_stores` (`owner_member_id`);
CREATE INDEX `aliexpress_store_feedbacks_7473547c` ON `aliexpress_store_feedbacks` (`store_id`);
CREATE INDEX `aliexpress_store_feedbacks_detailed_7473547c` ON `aliexpress_store_feedbacks_detailed` (`store_id`);
CREATE INDEX `alx_to_ebay_category_maps_3b7506d9` ON `alx_to_ebay_category_maps` (`ebay_category_id`);
COMMIT;
