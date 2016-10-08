BEGIN;
--
-- Create model AmazonOrderItem
--
CREATE TABLE `amazon_order_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_id` varchar(100) NOT NULL,
    `asin` varchar(32) NULL,
    `is_variation` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
--
-- Remove field amazon_item from amazonorder
--
ALTER TABLE `amazon_orders` DROP FOREIGN KEY `amazon_orders_asin_4839d969_fk_amazon_items_asin`;
ALTER TABLE `amazon_orders` MODIFY COLUMN `asin` varchar(32) NULL;
--
-- Add field savings to amazonorder
--
ALTER TABLE `amazon_orders` ADD COLUMN `savings` numeric(15, 2) DEFAULT 0.00 NOT NULL;
ALTER TABLE `amazon_orders` ALTER COLUMN `savings` DROP DEFAULT;
--
-- Add field amazon_order to amazonorderitem
--
ALTER TABLE `amazon_order_items` ADD COLUMN `amazon_order_id` integer unsigned NULL;
ALTER TABLE `amazon_order_items` ALTER COLUMN `amazon_order_id` DROP DEFAULT;
CREATE INDEX `amazon_order_items_69dfcb07` ON `amazon_order_items` (`order_id`);
CREATE INDEX `amazon_order_items_62130e1b` ON `amazon_order_items` (`asin`);
CREATE INDEX `amazon_order_items_b7b49caa` ON `amazon_order_items` (`amazon_order_id`);
ALTER TABLE `amazon_order_items` ADD CONSTRAINT `amazon_order_items_amazon_order_id_a8d1885f_fk_amazon_orders_id` FOREIGN KEY (`amazon_order_id`) REFERENCES `amazon_orders` (`id`);

COMMIT;