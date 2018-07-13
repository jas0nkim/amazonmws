BEGIN;
--
-- Create model EbayInventoryItemEbayInventoryItemGroup
--
CREATE TABLE `ebay_inventory_items_ebay_inventory_item_groups` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY);
--
-- Alter field sku on ebayinventoryitem
--
DROP INDEX `ebay_inventory_items_sku_98342e3d` ON `ebay_inventory_items`;
ALTER TABLE `ebay_inventory_items` ADD CONSTRAINT `ebay_inventory_items_sku_98342e3d_uniq` UNIQUE (`sku`);
--
-- Alter field inventory_item_group_key on ebayinventoryitemgroup
--
DROP INDEX `ebay_inventory_item_groups_inventory_item_group_key_cb1da08e` ON `ebay_inventory_item_groups`;
ALTER TABLE `ebay_inventory_item_groups` ADD CONSTRAINT `ebay_inventory_item_grou_inventory_item_group_key_cb1da08e_uniq` UNIQUE (`inventory_item_group_key`);
--
-- Add field ebay_inventory_item to ebayinventoryitemebayinventoryitemgroup
--
ALTER TABLE `ebay_inventory_items_ebay_inventory_item_groups` ADD COLUMN `sku` varchar(100) NULL;
--
-- Add field ebay_inventory_item_group to ebayinventoryitemebayinventoryitemgroup
--
ALTER TABLE `ebay_inventory_items_ebay_inventory_item_groups` ADD COLUMN `inventory_item_group_key` varchar(100) NULL;
CREATE INDEX `ebay_inventory_items_ebay_inventory_item_groups_sku_ca4102e9` ON `ebay_inventory_items_ebay_inventory_item_groups` (`sku`);
ALTER TABLE `ebay_inventory_items_ebay_inventory_item_groups` ADD CONSTRAINT `ebay_inventory_items_sku_ca4102e9_fk_ebay_inve` FOREIGN KEY (`sku`) REFERENCES `ebay_inventory_items` (`sku`);
CREATE INDEX `ebay_inventory_items_ebay_i_inventory_item_group_key_bfb916ce` ON `ebay_inventory_items_ebay_inventory_item_groups` (`inventory_item_group_key`);
ALTER TABLE `ebay_inventory_items_ebay_inventory_item_groups` ADD CONSTRAINT `ebay_inventory_items_inventory_item_group_bfb916ce_fk_ebay_inve` FOREIGN KEY (`inventory_item_group_key`) REFERENCES `ebay_inventory_item_groups` (`inventory_item_group_key`);
COMMIT;
