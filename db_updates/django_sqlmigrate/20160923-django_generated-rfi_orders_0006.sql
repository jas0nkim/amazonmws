BEGIN;
--
-- Add field is_variation to ebayorderitem
--
ALTER TABLE `ebay_order_items` ADD COLUMN `is_variation` bool DEFAULT 0 NOT NULL;
ALTER TABLE `ebay_order_items` ALTER COLUMN `is_variation` DROP DEFAULT;

COMMIT;