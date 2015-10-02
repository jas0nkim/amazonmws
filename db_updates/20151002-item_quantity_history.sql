CREATE TABLE `item_quantity_history` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `ebay_item_id` integer(11) unsigned DEFAULT NULL,
    `ebid` varchar(100) DEFAULT NULL,
    `quantity` smallint(5) unsigned DEFAULT 0,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `item_quantity_history` ADD INDEX `index_item_quantity_history_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `item_quantity_history` ADD INDEX `index_item_quantity_history_asin` (`asin`);
ALTER TABLE `item_quantity_history` ADD INDEX `index_item_quantity_history_ebay_item_id` (`ebay_item_id`);
ALTER TABLE `item_quantity_history` ADD INDEX `index_item_quantity_history_ebid` (`ebid`);
