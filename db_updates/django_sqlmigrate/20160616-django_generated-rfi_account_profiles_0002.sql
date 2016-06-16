BEGIN;
--
-- Add field margin_min_dollar to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `margin_min_dollar` numeric(15, 2) DEFAULT 0.00 NULL;
ALTER TABLE `ebay_stores` ALTER COLUMN `margin_min_dollar` DROP DEFAULT;

COMMIT;