ALTER TABLE `amazon_items` MODIFY COLUMN `category` varchar(255) DEFAULT NULL;
ALTER TABLE `amazon_items` DROP COLUMN `subcategory`;
ALTER TABLE `amazon_items` ADD COLUMN `features` text DEFAULT NULL AFTER `price`;
ALTER TABLE `amazon_items` ADD COLUMN `ebay_category_id` varchar(32) DEFAULT NULL AFTER `status`;