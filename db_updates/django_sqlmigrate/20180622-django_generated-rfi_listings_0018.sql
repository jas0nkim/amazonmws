BEGIN;

--
-- Create model EbayInventoryItem
--
CREATE TABLE `ebay_inventory_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `sku` varchar(100) NOT NULL,
    `ship_to_location_availability_quantity` smallint NULL,
    `title` longtext NOT NULL,
    `description` longtext NULL,
    `aspects` longtext NULL,
    `image_urls` longtext NULL,
    `inventory_item_group_keys` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL
);

--
-- Create model EbayInventoryItemGroup
--
CREATE TABLE `ebay_inventory_item_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `inventory_item_group_key` varchar(100) NOT NULL,
    `description` longtext NULL,
    `common_aspects` longtext NULL,
    `image_urls` longtext NULL,
    `variant_skus` longtext NULL,
    `aspects_image_varies_by` longtext NULL,
    `varies_by_specifications` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL
);

--
-- Create model EbayInventoryLocation
--
CREATE TABLE `ebay_inventory_locations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `merchant_location_key` varchar(255) NOT NULL,
    `address_country` varchar(32) NULL,
    `status` smallint NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL
);

--
-- Create model EbayOffer
--
CREATE TABLE `ebay_offers` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `offer_id` varchar(100) NOT NULL,
    `listing_id` varchar(100) NULL,
    `available_quantity` smallint NULL,
    `ebay_category_id` varchar(100) NULL,
    `payment_policy_id` varchar(100) NULL,
    `return_policy_id` varchar(100) NULL,
    `fulfillment_policy_id` varchar(100) NULL,
    `merchant_location_key` varchar(255) NOT NULL,
    `original_retail_price` numeric(15, 2) NOT NULL,
    `original_retail_price_currency` varchar(32) NULL,
    `price` numeric(15, 2) NOT NULL,
    `price_currency` varchar(32) NULL,
    `quantity_limit_per_buyer` smallint NULL,
    `store_category_names` longtext NULL,
    `sku` varchar(100) NOT NULL,
    `marketplace_id` varchar(32) NOT NULL,
    `listing_format` varchar(32) NOT NULL,
    `status` smallint NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL
);

ALTER TABLE `ebay_inventory_items` ADD CONSTRAINT `ebay_inventory_items_ebay_store_id_a0d1d004_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_inventory_items_sku_98342e3d` ON `ebay_inventory_items` (`sku`);
CREATE INDEX `ebay_inventory_items_ebay_store_id_a0d1d004` ON `ebay_inventory_items` (`ebay_store_id`);

ALTER TABLE `ebay_inventory_item_groups` ADD CONSTRAINT `ebay_inventory_item__ebay_store_id_e044e7d7_fk_ebay_stor` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_inventory_item_groups_inventory_item_group_key_cb1da08e` ON `ebay_inventory_item_groups` (`inventory_item_group_key`);
CREATE INDEX `ebay_inventory_item_groups_ebay_store_id_e044e7d7` ON `ebay_inventory_item_groups` (`ebay_store_id`);

ALTER TABLE `ebay_inventory_locations` ADD CONSTRAINT `ebay_inventory_locat_ebay_store_id_71305b89_fk_ebay_stor` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_inventory_locations_merchant_location_key_628f8dc7` ON `ebay_inventory_locations` (`merchant_location_key`);
CREATE INDEX `ebay_inventory_locations_ebay_store_id_71305b89` ON `ebay_inventory_locations` (`ebay_store_id`);

ALTER TABLE `ebay_offers` ADD CONSTRAINT `ebay_offers_ebay_store_id_f5d29d9f_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_offers_offer_id_abf456c4` ON `ebay_offers` (`offer_id`);
CREATE INDEX `ebay_offers_listing_id_1a8f1ddb` ON `ebay_offers` (`listing_id`);
CREATE INDEX `ebay_offers_ebay_category_id_30181cd8` ON `ebay_offers` (`ebay_category_id`);
CREATE INDEX `ebay_offers_merchant_location_key_7f0f9a4b` ON `ebay_offers` (`merchant_location_key`);
CREATE INDEX `ebay_offers_sku_9e62dfac` ON `ebay_offers` (`sku`);
CREATE INDEX `ebay_offers_marketplace_id_68f81c4a` ON `ebay_offers` (`marketplace_id`);
CREATE INDEX `ebay_offers_listing_format_2d1a3ffe` ON `ebay_offers` (`listing_format`);
CREATE INDEX `ebay_offers_ebay_store_id_f5d29d9f` ON `ebay_offers` (`ebay_store_id`);
COMMIT;
