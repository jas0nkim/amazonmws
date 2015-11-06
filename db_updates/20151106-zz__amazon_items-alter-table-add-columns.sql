ALTER TABLE `zz__amazon_items` ADD COLUMN `market_price` decimal(15,2) NOT NULL AFTER `price`;
ALTER TABLE `zz__amazon_items` ADD COLUMN `merchant_id` varchar(32) DEFAULT NULL AFTER `is_addon`;
ALTER TABLE `zz__amazon_items` ADD COLUMN `merchant_name` varchar(100) DEFAULT NULL AFTER `merchant_id`;