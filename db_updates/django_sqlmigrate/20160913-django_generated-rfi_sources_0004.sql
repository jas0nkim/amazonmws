BEGIN;
--
-- Add field parent_asin to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `parent_asin` varchar(32) NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `parent_asin` DROP DEFAULT;
CREATE INDEX `amazon_items_bb72ef9d` ON `amazon_items` (`parent_asin`);

COMMIT;