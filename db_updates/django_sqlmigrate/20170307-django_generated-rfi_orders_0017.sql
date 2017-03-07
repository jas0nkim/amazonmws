BEGIN;
--
-- Add field note to amazonorderreturn
--
ALTER TABLE `amazon_order_returns` ADD COLUMN `note` longtext NULL;
--
-- Add field note to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `note` longtext NULL;
--
-- Add field raw_data_detailed to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `raw_data_detailed` longtext NULL;
COMMIT;