CREATE TABLE `ebay_product_categories` (
    `id` integer(11) unsigned AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `category_id` integer(11) NOT NULL,
    `category_level` smallint(3) NOT NULL,
    `category_name` varchar(100) NOT NULL,
    `category_parent_id` integer(11) NOT NULL,
    `auto_pay_enabled` tinyint(1) DEFAULT 1,
    `best_offer_enabled` tinyint(1) DEFAULT 1,
    `leaf_category` tinyint(1) DEFAULT 0
);

ALTER TABLE `ebay_product_categories` ADD INDEX `index_ebay_product_categories_category_id` (`category_id`);
ALTER TABLE `ebay_product_categories` ADD INDEX `index_ebay_product_categories_category_parent_id` (`category_parent_id`);