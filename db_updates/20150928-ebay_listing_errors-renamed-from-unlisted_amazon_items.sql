RENAME TABLE `unlisted_amazon_items` TO `ebay_listing_errors`;

ALTER TABLE `ebay_listing_errors` ADD COLUMN `ebay_item_id` int(11) unsigned DEFAULT '0' AFTER `asin`;
ALTER TABLE `ebay_listing_errors` ADD COLUMN `ebid` varchar(100) DEFAULT NULL AFTER `ebay_item_id`;
ALTER TABLE `ebay_listing_errors` ADD COLUMN `related_ebay_api` varchar(255) DEFAULT NULL AFTER `reason`;

ALTER TABLE `ebay_listing_errors` CHANGE `status` `type` smallint(3) unsigned DEFAULT '0';