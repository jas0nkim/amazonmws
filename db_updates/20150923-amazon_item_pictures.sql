CREATE TABLE `amazon_item_pictures` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `original_picture_url` varchar(255) DEFAULT NULL,
    `converted_picture_url` varchar(255) DEFAULT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `amazon_item_pictures` ADD INDEX `index_amazon_item_pictures_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `amazon_item_pictures` ADD INDEX `index_amazon_item_pictures_amazon_asin` (`asin`);