CREATE TABLE `amazon_items` (
    `id` integer(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `url` text NOT NULL,
    `asin` varchar(32) NOT NULL,
    `category` varchar(100) DEFAULT NULL,
    `subcategory` varchar(100) DEFAULT NULL,
    `title` text NOT NULL,
    `price` numeric(15,2) NOT NULL,
    `description` text DEFAULT NULL,
    `status` smallint(3) DEFAULT 0,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` timestamp DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE `amazon_items` ADD INDEX `index_amazon_items_asin` (`asin`);