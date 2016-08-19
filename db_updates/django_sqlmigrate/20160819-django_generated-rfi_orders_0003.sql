BEGIN;
--
-- Add field ebay_order to ebayorderitem
--
ALTER TABLE `ebay_order_items` ADD COLUMN `ebay_order_id` integer NULL;
ALTER TABLE `ebay_order_items` ALTER COLUMN `ebay_order_id` DROP DEFAULT;
--
-- Add field ebay_order to ebayordershipping
--
ALTER TABLE `ebay_order_shippings` ADD COLUMN `ebay_order_id` integer NULL;
ALTER TABLE `ebay_order_shippings` ALTER COLUMN `ebay_order_id` DROP DEFAULT;
CREATE INDEX `ebay_order_items_1a976cec` ON `ebay_order_items` (`ebay_order_id`);
ALTER TABLE `ebay_order_items` ADD CONSTRAINT `ebay_order_items_ebay_order_id_0f609dde_fk_ebay_orders_id` FOREIGN KEY (`ebay_order_id`) REFERENCES `ebay_orders` (`id`);
CREATE INDEX `ebay_order_shippings_1a976cec` ON `ebay_order_shippings` (`ebay_order_id`);
ALTER TABLE `ebay_order_shippings` ADD CONSTRAINT `ebay_order_shippings_ebay_order_id_e444721a_fk_ebay_orders_id` FOREIGN KEY (`ebay_order_id`) REFERENCES `ebay_orders` (`id`);

COMMIT;