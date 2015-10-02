CREATE TABLE `item_status_history` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `ebay_item_id` integer(11) unsigned DEFAULT NULL,
    `ebid` varchar(100) DEFAULT NULL,
    `am_status` smallint(3) unsigned DEFAULT 0,
    `eb_status` smallint(3) unsigned DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `item_status_history` ADD INDEX `index_item_status_history_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `item_status_history` ADD INDEX `index_item_status_history_asin` (`asin`);
ALTER TABLE `item_status_history` ADD INDEX `index_item_status_history_ebay_item_id` (`ebay_item_id`);
ALTER TABLE `item_status_history` ADD INDEX `index_item_status_history_ebid` (`ebid`);
