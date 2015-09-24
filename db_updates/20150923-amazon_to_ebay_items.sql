CREATE TABLE `amazon_to_ebay_items` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `ebid` varchar(100) NOT NULL,
    `eb_price` numeric(15,2) NOT NULL,
    `status` smallint(3) unsigned DEFAULT 0,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `amazon_items` ADD INDEX `index_amazon_items_asin` (`asin`);