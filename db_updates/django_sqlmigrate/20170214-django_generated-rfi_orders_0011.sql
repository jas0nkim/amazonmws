BEGIN;
--
-- Create model EbayOrderReturn
--
CREATE TABLE `ebay_order_returns` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `return_id` varchar(100) NOT NULL,
    `transaction_id` varchar(100) NOT NULL,
    `item_id` varchar(100) NOT NULL,
    `quantity` smallint NULL,
    `buyer_username` varchar(100) NOT NULL,
    `amount` numeric(15, 2) NOT NULL,
    `reason` varchar(100) NULL,
    `carrier` varchar(100) NULL,
    `tracking_number` varchar(100) NULL,
    `rma` varchar(100) NULL,
    `status` varchar(100) NULL,
    `state` varchar(100) NULL,
    `creation_time` datetime NULL,
    `raw_data` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);

CREATE INDEX `ebay_order_returns_f0c7a554` ON `ebay_order_returns` (`return_id`);
CREATE INDEX `ebay_order_returns_f847de52` ON `ebay_order_returns` (`transaction_id`);
CREATE INDEX `ebay_order_returns_82bfda79` ON `ebay_order_returns` (`item_id`);
CREATE INDEX `ebay_order_returns_310279b6` ON `ebay_order_returns` (`buyer_username`);
COMMIT;