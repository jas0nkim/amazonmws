BEGIN;
--
-- Add field variation_specifics to ebayinventoryitem
--
ALTER TABLE `ebay_inventory_items` ADD COLUMN `variation_specifics` longtext NULL;
COMMIT;
