BEGIN;
--
-- Add field title to ebayinventoryitemgroup
--
ALTER TABLE `ebay_inventory_item_groups` ADD COLUMN `title` longtext NULL;
COMMIT;