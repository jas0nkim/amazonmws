CREATE TABLE `unlisted_amazon_items` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `reason` text NOT NULL,
    `resolved_howto` varchar(255) DEFAULT NULL,
    `status` smallint(3) unsigned DEFAULT 0,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `unlisted_amazon_items` ADD INDEX `index_unlisted_amazon_items_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `unlisted_amazon_items` ADD INDEX `index_unlisted_amazon_items_asin` (`asin`);