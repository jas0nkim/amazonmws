ALTER TABLE `lookups` ADD COLUMN `spider_name` varchar(100) DEFAULT NULL AFTER `id`;
ALTER TABLE `lookups` ADD INDEX `index_lookups_spider_name` (`spider_name`);