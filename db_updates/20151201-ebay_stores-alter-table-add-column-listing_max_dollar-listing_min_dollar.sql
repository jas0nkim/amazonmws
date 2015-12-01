ALTER TABLE `ebay_stores` ADD COLUMN `listing_min_dollar` decimal(15,2) DEFAULT NULL AFTER `margin_max_dollar`;
ALTER TABLE `ebay_stores` ADD COLUMN `listing_max_dollar` decimal(15,2) DEFAULT NULL AFTER `listing_min_dollar`;
