BEGIN;
--
-- Add field order_status to ebayorder
--
ALTER TABLE `ebay_orders` ADD COLUMN `order_status` varchar(32) NULL;
ALTER TABLE `ebay_orders` ALTER COLUMN `order_status` DROP DEFAULT;

COMMIT;