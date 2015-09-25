CREATE TABLE `ebay_items` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `ebid` varchar(100) NOT NULL,
    `ebay_category_id` varchar(32) NOT NULL,
    `eb_price` numeric(15,2) NOT NULL,
    `quantity` smallint(5) unsigned DEFAULT 0,
    `status` smallint(3) unsigned DEFAULT 0,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `ebay_items` ADD INDEX `index_ebay_items_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `ebay_items` ADD INDEX `index_ebay_items_asin` (`asin`);
ALTER TABLE `ebay_items` ADD INDEX `index_ebay_items_ebid` (`ebid`);
ALTER TABLE `ebay_items` ADD INDEX `index_ebay_items_ebay_category_id` (`ebay_category_id`);