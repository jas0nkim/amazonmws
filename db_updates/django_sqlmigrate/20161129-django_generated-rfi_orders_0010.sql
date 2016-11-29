BEGIN;
--
-- Add field payment_status to ebayorder
--
ALTER TABLE `ebay_orders` ADD COLUMN `payment_status` varchar(32) NULL;
ALTER TABLE `ebay_orders` ALTER COLUMN `payment_status` DROP DEFAULT;

-- filling up 'Succeeded' on existing data
UPDATE `ebay_orders` SET `payment_status` = 'Succeeded';

COMMIT;