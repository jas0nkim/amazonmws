BEGIN;
--
-- Create model EbayOrder
--
CREATE TABLE `ebay_orders` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_id` varchar(100) NOT NULL UNIQUE, `record_number` integer NOT NULL, `total_price` numeric(15, 2) NOT NULL, `shipping_cost` numeric(15, 2) NULL, `buyer_email` varchar(100) NOT NULL, `buyer_user_id` varchar(100) NOT NULL, `buyer_status` varchar(32) NULL, `buyer_shipping_name` varchar(100) NULL, `buyer_shipping_street1` varchar(100) NULL, `buyer_shipping_street2` varchar(100) NULL, `buyer_shipping_city_name` varchar(100) NULL, `buyer_shipping_state_or_province` varchar(100) NULL, `buyer_shipping_postal_code` varchar(100) NULL, `buyer_shipping_country` varchar(32) NULL, `buyer_shipping_phone` varchar(100) NULL, `checkout_status` varchar(32) NOT NULL, `creation_time` datetime NULL, `paid_time` datetime NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `ts` datetime NOT NULL, `ebay_store_id` integer unsigned NULL) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Create model EbayOrderAmazonOrder
--
CREATE TABLE `ebay_order_amazon_orders` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Create model EbayOrderAutomationError
--
CREATE TABLE `ebay_order_automation_errors` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `error_message` varchar(255) NULL, `ebay_order_id` varchar(100) NULL) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Create model EbayOrderItem
--
CREATE TABLE `ebay_order_items` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_id` varchar(100) NOT NULL, `ebid` varchar(100) NOT NULL, `transaction_id` varchar(100) NOT NULL, `title` varchar(255) NULL, `sku` varchar(100) NULL, `quantity` smallint NULL, `price` numeric(15, 2) NOT NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `ts` datetime NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Create model EbayOrderShipping
--
CREATE TABLE `ebay_order_shippings` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_id` varchar(100) NOT NULL, `carrier` varchar(100) NULL, `tracking_number` varchar(100) NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `ts` datetime NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Alter field order_id on amazonorder
--
ALTER TABLE `amazon_orders` ADD CONSTRAINT `amazon_orders_order_id_a2428600_uniq` UNIQUE (`order_id`);
--
-- Add field amazon_order to ebayorderamazonorder
--
ALTER TABLE `ebay_order_amazon_orders` ADD COLUMN `amazon_order_id` varchar(100) NULL;
ALTER TABLE `ebay_order_amazon_orders` ALTER COLUMN `amazon_order_id` DROP DEFAULT;
--
-- Add field ebay_order to ebayorderamazonorder
--
ALTER TABLE `ebay_order_amazon_orders` ADD COLUMN `ebay_order_id` varchar(100) NULL;
ALTER TABLE `ebay_order_amazon_orders` ALTER COLUMN `ebay_order_id` DROP DEFAULT;
ALTER TABLE `ebay_orders` ADD CONSTRAINT `ebay_orders_ebay_store_id_085a6b55_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_orders_36bcfb1f` ON `ebay_orders` (`buyer_email`);
CREATE INDEX `ebay_orders_1aeb7048` ON `ebay_orders` (`buyer_user_id`);
CREATE INDEX `ebay_orders_3ae127fc` ON `ebay_orders` (`ebay_store_id`);
ALTER TABLE `ebay_order_automation_errors` ADD CONSTRAINT `ebay_order_automa_ebay_order_id_6512ff71_fk_ebay_orders_order_id` FOREIGN KEY (`ebay_order_id`) REFERENCES `ebay_orders` (`order_id`);
CREATE INDEX `ebay_order_automation_errors_1a976cec` ON `ebay_order_automation_errors` (`ebay_order_id`);
CREATE INDEX `ebay_order_items_69dfcb07` ON `ebay_order_items` (`order_id`);
CREATE INDEX `ebay_order_items_26635314` ON `ebay_order_items` (`ebid`);
CREATE INDEX `ebay_order_items_f847de52` ON `ebay_order_items` (`transaction_id`);
CREATE INDEX `ebay_order_shippings_69dfcb07` ON `ebay_order_shippings` (`order_id`);
CREATE INDEX `ebay_order_amazon_orders_b7b49caa` ON `ebay_order_amazon_orders` (`amazon_order_id`);
ALTER TABLE `ebay_order_amazon_orders` ADD CONSTRAINT `ebay_order_am_amazon_order_id_05f6c1d2_fk_amazon_orders_order_id` FOREIGN KEY (`amazon_order_id`) REFERENCES `amazon_orders` (`order_id`);
CREATE INDEX `ebay_order_amazon_orders_1a976cec` ON `ebay_order_amazon_orders` (`ebay_order_id`);
ALTER TABLE `ebay_order_amazon_orders` ADD CONSTRAINT `ebay_order_amazon_ebay_order_id_d4d1e392_fk_ebay_orders_order_id` FOREIGN KEY (`ebay_order_id`) REFERENCES `ebay_orders` (`order_id`);

COMMIT;