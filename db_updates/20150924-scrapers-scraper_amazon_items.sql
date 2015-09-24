CREATE TABLE `scrapers` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `description` text DEFAULT NULL
);

INSERT INTO `scrapers` (name) VALUES ('amazon_bestsellers_toyandgames');
INSERT INTO `scrapers` (name) VALUES ('amazon_halloween_accessories');

CREATE TABLE `scraper_amazon_items` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `scraper_id` integer(11) unsigned NOT NULL,
    `amazon_item_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `scraper_amazon_items` ADD INDEX `index_scraper_amazon_items_scraper_id` (`scraper_id`);
ALTER TABLE `scraper_amazon_items` ADD INDEX `index_scraper_amazon_items_amazon_item_id` (`amazon_item_id`);
ALTER TABLE `scraper_amazon_items` ADD INDEX `index_scraper_amazon_items_asin` (`asin`);