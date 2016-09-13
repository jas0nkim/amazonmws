BEGIN;
--
-- Create model EbayItemVariation
--
CREATE TABLE `ebay_item_variations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebid` varchar(100) NOT NULL,
    `asin` varchar(32) NOT NULL,
    `specifics` varchar(255) NULL,
    `eb_price` numeric(15, 2) NOT NULL,
    `quantity` smallint NULL, 
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL, 
    `ebay_item_id` integer unsigned NOT NULL);
--
-- Add field parent_asin to amazonscrapetask
--
ALTER TABLE `amazon_scrape_tasks` ADD COLUMN `parent_asin` varchar(32) NULL;
ALTER TABLE `amazon_scrape_tasks` ALTER COLUMN `parent_asin` DROP DEFAULT;
ALTER TABLE `ebay_item_variations` ADD CONSTRAINT `ebay_item_variations_ebay_item_id_06d7cadf_fk_ebay_items_id` FOREIGN KEY (`ebay_item_id`) REFERENCES `ebay_items` (`id`);
CREATE INDEX `ebay_item_variations_26635314` ON `ebay_item_variations` (`ebid`);
CREATE INDEX `ebay_item_variations_62130e1b` ON `ebay_item_variations` (`asin`);
CREATE INDEX `ebay_item_variations_389acb9f` ON `ebay_item_variations` (`ebay_item_id`);
CREATE INDEX `amazon_scrape_tasks_bb72ef9d` ON `amazon_scrape_tasks` (`parent_asin`);

COMMIT;
