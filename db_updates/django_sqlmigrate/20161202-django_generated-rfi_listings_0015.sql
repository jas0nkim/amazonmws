BEGIN;
--
-- Add field level to ebaystorecategory
--
ALTER TABLE `ebay_store_categories` ADD COLUMN `level` integer DEFAULT 1 NULL;
ALTER TABLE `ebay_store_categories` ALTER COLUMN `level` DROP DEFAULT;

COMMIT;