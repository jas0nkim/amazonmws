BEGIN;
--
-- Add field policy_shipping_international to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `policy_shipping_international` longtext NULL;

COMMIT;