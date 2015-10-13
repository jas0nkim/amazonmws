ALTER TABLE `ebay_items` ADD COLUMN `ebay_store_id` int(11) unsigned NOT NULL AFTER `id`;
ALTER TABLE `ebay_items` ADD INDEX `index_iebay_items_ebay_store_id` (`ebay_store_id`);
