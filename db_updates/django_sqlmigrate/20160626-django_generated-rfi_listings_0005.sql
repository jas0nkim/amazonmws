BEGIN;
--
-- Alter field ebid on ebayitemstat
--  (drop unique, and add index back)
--
ALTER TABLE `ebay_item_stats` DROP INDEX `ebid`;
ALTER TABLE `ebay_item_stats` ADD INDEX `ebid` (`ebid`);

COMMIT;