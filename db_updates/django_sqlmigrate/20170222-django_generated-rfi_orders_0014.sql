BEGIN;
--
-- Add field ebay_store to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `ebay_store_id` integer unsigned NULL;
ALTER TABLE `ebay_order_returns` ALTER COLUMN `ebay_store_id` DROP DEFAULT;
CREATE INDEX `ebay_order_returns_3ae127fc` ON `ebay_order_returns` (`ebay_store_id`);
ALTER TABLE `ebay_order_returns` ADD CONSTRAINT `ebay_order_returns_ebay_store_id_aae844bd_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
COMMIT;