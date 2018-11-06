BEGIN;
--
-- Change Meta options on exclbrand
--
--
-- Add field reason_hide_from_search to ebayitemstat
--
ALTER TABLE `ebay_item_stats` ADD COLUMN `reason_hide_from_search` varchar(100) NULL;
COMMIT;