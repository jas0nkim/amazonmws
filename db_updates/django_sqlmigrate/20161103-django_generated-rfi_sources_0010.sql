BEGIN;
--
-- Change Meta options on atoecategorymap
--
--
-- Add field international_shipping to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `international_shipping` bool DEFAULT 0 NOT NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `international_shipping` DROP DEFAULT;
--
-- Alter field ebay_category_name on atoecategorymap
--

COMMIT;