BEGIN;
--
-- Add field ebay_store to ebayitemstat
--
ALTER TABLE `ebay_item_stats` ADD COLUMN `ebay_store_id` integer unsigned DEFAULT 1 NOT NULL;
ALTER TABLE `ebay_item_stats` ALTER COLUMN `ebay_store_id` DROP DEFAULT;
CREATE INDEX `ebay_item_stats_3ae127fc` ON `ebay_item_stats` (`ebay_store_id`);
ALTER TABLE `ebay_item_stats` ADD CONSTRAINT `ebay_item_stats_ebay_store_id_ae3e5854_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);

COMMIT;