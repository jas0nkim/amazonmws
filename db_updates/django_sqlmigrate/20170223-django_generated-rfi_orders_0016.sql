BEGIN;
--
-- Create model AmazonOrderReturn
--
CREATE TABLE `amazon_order_returns` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `order_id` varchar(100) NOT NULL,
    `asin` varchar(32) NULL,
    `return_id` varchar(100) NULL,
    `ebay_return_id` varchar(100) NULL,
    `quantity` smallint NULL,
    `refunded_amount` numeric(15, 2) NULL,
    `carrier` varchar(100) NULL,
    `tracking_number` varchar(100) NULL,
    `rma` varchar(100) NULL,
    `status` varchar(100) NULL,
    `returned_date` date NULL,
    `refunded_date` date NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `amazon_account_id` integer unsigned NOT NULL
);
ALTER TABLE `amazon_order_returns` ADD CONSTRAINT `amazon_order_re_amazon_account_id_1fbb6f64_fk_amazon_accounts_id` FOREIGN KEY (`amazon_account_id`) REFERENCES `amazon_accounts` (`id`);
CREATE INDEX `amazon_order_returns_69dfcb07` ON `amazon_order_returns` (`order_id`);
CREATE INDEX `amazon_order_returns_62130e1b` ON `amazon_order_returns` (`asin`);
CREATE INDEX `amazon_order_returns_f0c7a554` ON `amazon_order_returns` (`return_id`);
CREATE INDEX `amazon_order_returns_354c234d` ON `amazon_order_returns` (`ebay_return_id`);
CREATE INDEX `amazon_order_returns_e1cea68c` ON `amazon_order_returns` (`amazon_account_id`);
COMMIT;