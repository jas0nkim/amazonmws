BEGIN;
--
-- Add field comments to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `comments` varchar(255) NULL;
ALTER TABLE `ebay_order_returns` ALTER COLUMN `comments` DROP DEFAULT;
COMMIT;