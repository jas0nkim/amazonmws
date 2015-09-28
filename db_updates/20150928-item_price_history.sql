CREATE TABLE `item_price_history` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `ebay_item_id` integer(11) unsigned DEFAULT NULL,
    `ebid` varchar(100) DEFAULT NULL,
    `am_price` numeric(15,2) NOT NULL,
    `eb_price` numeric(15,2) DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `item_price_history` ADD INDEX `index_item_price_history_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `item_price_history` ADD INDEX `index_item_price_history_asin` (`asin`);
ALTER TABLE `item_price_history` ADD INDEX `index_item_price_history_ebay_item_id` (`ebay_item_id`);
ALTER TABLE `item_price_history` ADD INDEX `index_item_price_history_ebid` (`ebid`);
