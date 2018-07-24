BEGIN;
--
-- Add field quantity_sold to ebayitem
--
ALTER TABLE `ebay_items` ADD COLUMN `quantity_sold` smallint DEFAULT 0 NOT NULL;
ALTER TABLE `ebay_items` ALTER COLUMN `quantity_sold` DROP DEFAULT;
--
-- Add field quantity_sold to ebayitemvariation
--
ALTER TABLE `ebay_item_variations` ADD COLUMN `quantity_sold` smallint DEFAULT 0 NOT NULL;
ALTER TABLE `ebay_item_variations` ALTER COLUMN `quantity_sold` DROP DEFAULT;
--
-- Alter field ship_to_location_availability_quantity on ebayinventoryitem
--
UPDATE `ebay_inventory_items` SET `ship_to_location_availability_quantity` = 0 WHERE `ship_to_location_availability_quantity` IS NULL;
ALTER TABLE `ebay_inventory_items` MODIFY `ship_to_location_availability_quantity` smallint NOT NULL;
--
-- Alter field status on ebayinventorylocation
--
UPDATE `ebay_inventory_locations` SET `status` = 1 WHERE `status` IS NULL;
ALTER TABLE `ebay_inventory_locations` MODIFY `status` smallint;
--
-- Alter field status on ebayitem
--
UPDATE `ebay_items` SET `status` = 0 WHERE `status` IS NULL;
ALTER TABLE `ebay_items` MODIFY `status` smallint NOT NULL;
--
-- Alter field quantity on ebayitemvariation
--
UPDATE `ebay_item_variations` SET `quantity` = 0 WHERE `quantity` IS NULL;
ALTER TABLE `ebay_item_variations` MODIFY `quantity` smallint NOT NULL;
--
-- Alter field available_quantity on ebayoffer
--
UPDATE `ebay_offers` SET `available_quantity` = 0 WHERE `available_quantity` IS NULL;
ALTER TABLE `ebay_offers` MODIFY `available_quantity` smallint NOT NULL;
--
-- Alter field quantity_limit_per_buyer on ebayoffer
--
ALTER TABLE `ebay_offers` ALTER COLUMN `quantity_limit_per_buyer` SET DEFAULT 0;
UPDATE `ebay_offers` SET `quantity_limit_per_buyer` = 0 WHERE `quantity_limit_per_buyer` IS NULL;
ALTER TABLE `ebay_offers` MODIFY `quantity_limit_per_buyer` smallint NOT NULL;
ALTER TABLE `ebay_offers` ALTER COLUMN `quantity_limit_per_buyer` DROP DEFAULT;
--
-- Alter field status on ebayoffer
--
UPDATE `ebay_offers` SET `status` = 0 WHERE `status` IS NULL;
ALTER TABLE `ebay_offers` MODIFY `status` smallint NOT NULL;
--
-- Alter field priority on ebaystorepreferredcategory
--
UPDATE `ebay_store_preferred_categories` SET `priority` = 0 WHERE `priority` IS NULL;
ALTER TABLE `ebay_store_preferred_categories` MODIFY `priority` smallint NOT NULL;
--
-- Alter field status on ebaystorepreferredcategory
--
UPDATE `ebay_store_preferred_categories` SET `status` = 1 WHERE `status` IS NULL;
ALTER TABLE `ebay_store_preferred_categories` MODIFY `status` smallint NOT NULL;
COMMIT;
