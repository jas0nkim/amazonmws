BEGIN;
--
-- Create model EbayItemPopularity
--
CREATE TABLE `ebay_item_popularities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebid` varchar(100) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `popularity` smallint NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL);
--
-- Create model EbayItemRepricedHistory
--
CREATE TABLE `ebay_item_repriced_histories` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebid` varchar(100) NOT NULL,
    `ebay_item_variation_id` integer NOT NULL,
    `asin` varchar(32) NULL,
    `parent_asin` varchar(32) NULL,
    `eb_price` numeric(15, 2) NOT NULL,
    `quantity` smallint NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL);
ALTER TABLE `ebay_item_popularities` ADD CONSTRAINT `ebay_item_popularities_ebay_store_id_bfe08235_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_item_popularities_26635314` ON `ebay_item_popularities` (`ebid`);
CREATE INDEX `ebay_item_popularities_bb72ef9d` ON `ebay_item_popularities` (`parent_asin`);
CREATE INDEX `ebay_item_popularities_4b0eed65` ON `ebay_item_popularities` (`popularity`);
CREATE INDEX `ebay_item_popularities_3ae127fc` ON `ebay_item_popularities` (`ebay_store_id`);
ALTER TABLE `ebay_item_repriced_histories` ADD CONSTRAINT `ebay_item_repriced_hist_ebay_store_id_08ae0acc_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_item_repriced_histories_26635314` ON `ebay_item_repriced_histories` (`ebid`);
CREATE INDEX `ebay_item_repriced_histories_0f89fbd9` ON `ebay_item_repriced_histories` (`ebay_item_variation_id`);
CREATE INDEX `ebay_item_repriced_histories_62130e1b` ON `ebay_item_repriced_histories` (`asin`);
CREATE INDEX `ebay_item_repriced_histories_bb72ef9d` ON `ebay_item_repriced_histories` (`parent_asin`);
CREATE INDEX `ebay_item_repriced_histories_3ae127fc` ON `ebay_item_repriced_histories` (`ebay_store_id`);

COMMIT;