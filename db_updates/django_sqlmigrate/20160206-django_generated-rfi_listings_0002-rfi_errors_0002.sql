BEGIN;
--
-- Remove field ebay_item_category from ebayitem
--
ALTER TABLE `ebay_items` DROP FOREIGN KEY `D8dc21e57266c5192e0982f1b3113fea`;
ALTER TABLE `ebay_items` DROP COLUMN `ebay_category_id` CASCADE;
--
-- Add field ebay_category_id to ebayitem
--
ALTER TABLE `ebay_items` ADD COLUMN `ebay_category_id` varchar(100) NULL;
ALTER TABLE `ebay_items` ALTER COLUMN `ebay_category_id` DROP DEFAULT;
CREATE INDEX `ebay_items_3b7506d9` ON `ebay_items` (`ebay_category_id`);

--
-- Remove field ebay_category from errorebayinvalidcategory
--
ALTER TABLE `error_ebay_invalid_category` DROP FOREIGN KEY `a4a84c858278b68ea946879d6b57ab23`;
ALTER TABLE `error_ebay_invalid_category` DROP COLUMN `ebay_category_id` CASCADE;
--
-- Add field ebay_category_id to errorebayinvalidcategory
--
ALTER TABLE `error_ebay_invalid_category` ADD COLUMN `ebay_category_id` varchar(100) NULL;
ALTER TABLE `error_ebay_invalid_category` ALTER COLUMN `ebay_category_id` DROP DEFAULT;
CREATE INDEX `error_ebay_invalid_category_3b7506d9` ON `error_ebay_invalid_category` (`ebay_category_id`);

COMMIT;