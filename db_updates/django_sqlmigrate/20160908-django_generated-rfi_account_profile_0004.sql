BEGIN;
--
-- Add field expedited_shipping_fee to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `expedited_shipping_fee` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` ALTER COLUMN `expedited_shipping_fee` DROP DEFAULT;
--
-- Add field oneday_shipping_fee to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `oneday_shipping_fee` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` ALTER COLUMN `oneday_shipping_fee` DROP DEFAULT;
--
-- Add field standard_shipping_fee to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `standard_shipping_fee` numeric(15, 2) NULL;
ALTER TABLE `ebay_stores` ALTER COLUMN `standard_shipping_fee` DROP DEFAULT;

COMMIT;