BEGIN;
--
-- Remove field amazon_item from ebayitem
--
ALTER TABLE `ebay_items` DROP FOREIGN KEY `ebay_items_asin_ddfe7985_fk_amazon_items_asin`;
ALTER TABLE `ebay_items` DROP INDEX `index_ebay_items_asin`;
-- ALTER TABLE `ebay_items` DROP COLUMN `asin` CASCADE;
--
-- Add field asin to ebayitem
--
-- ALTER TABLE `ebay_items` ADD COLUMN `asin` varchar(32) NULL;
-- ALTER TABLE `ebay_items` ALTER COLUMN `asin` DROP DEFAULT;
CREATE INDEX `ebay_items_62130e1b` ON `ebay_items` (`asin`);

COMMIT;