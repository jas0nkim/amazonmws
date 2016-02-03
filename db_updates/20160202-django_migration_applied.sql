-- amazon_bestsellers
ALTER TABLE `amazon_bestsellers` DROP INDEX `index_zz__amazon_bestsellers_asin`;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `bestseller_category_url` longtext NOT NULL;
ALTER TABLE `amazon_bestsellers` MODIFY COLUMN `asin` varchar(32) NOT NULL;
ALTER TABLE `amazon_bestsellers` ALTER COLUMN `asin` DROP DEFAULT;
CREATE INDEX `amazon_bestsellers_62130e1b` ON `amazon_bestsellers` (`asin`);
ALTER TABLE `amazon_bestsellers` ADD CONSTRAINT `amazon_bestsellers_asin_27274c9c_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_items
ALTER TABLE `amazon_items` MODIFY COLUMN `url` longtext NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `title` longtext NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `price` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `market_price` numeric(15, 2) NOT NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `quantity` smallint NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `features` longtext NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `description` longtext NULL;
ALTER TABLE `amazon_items` MODIFY COLUMN `avg_rating` double precision NULL;

-- amazon_item_offers
ALTER TABLE `amazon_item_offers` MODIFY COLUMN `asin` varchar(32) NOT NULL;
ALTER TABLE `amazon_item_offers` ALTER COLUMN `asin` DROP DEFAULT;
ALTER TABLE `amazon_item_offers` ADD CONSTRAINT `amazon_item_offers_asin_e7ef0260_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- amazon_item_pictures
ALTER TABLE `amazon_item_pictures` ADD CONSTRAINT `amazon_item_pictures_asin_7a2b328d_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);

-- a_to_e_category_maps
ALTER TABLE `a_to_e_category_maps` MODIFY COLUMN `ebay_category_id` varchar(100) NOT NULL;
ALTER TABLE `a_to_e_category_maps` ALTER COLUMN `ebay_category_id` DROP DEFAULT;
CREATE INDEX `a_to_e_category_maps_3b7506d9` ON `a_to_e_category_maps` (`ebay_category_id`);
ALTER TABLE `a_to_e_category_maps` ADD CONSTRAINT `e16d07189a0f0e635d30468faf6048bb` FOREIGN KEY (`ebay_category_id`) REFERENCES `ebay_product_categories` (`category_id`);
