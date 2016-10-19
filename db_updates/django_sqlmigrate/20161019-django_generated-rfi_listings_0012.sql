BEGIN;
--
-- Create model EbayItemLastReviseAttempted
--
CREATE TABLE `ebay_item_last_revise_attempted` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebid` varchar(100) NOT NULL,
    `ebay_item_variation_id` integer NOT NULL,
    `asin` varchar(32) NULL,
    `parent_asin` varchar(32) NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL
);
ALTER TABLE `ebay_item_last_revise_attempted` ADD CONSTRAINT `ebay_item_last_revise_a_ebay_store_id_079d6a1a_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `ebay_item_last_revise_attempted_26635314` ON `ebay_item_last_revise_attempted` (`ebid`);
CREATE INDEX `ebay_item_last_revise_attempted_0f89fbd9` ON `ebay_item_last_revise_attempted` (`ebay_item_variation_id`);
CREATE INDEX `ebay_item_last_revise_attempted_62130e1b` ON `ebay_item_last_revise_attempted` (`asin`);
CREATE INDEX `ebay_item_last_revise_attempted_bb72ef9d` ON `ebay_item_last_revise_attempted` (`parent_asin`);
CREATE INDEX `ebay_item_last_revise_attempted_3ae127fc` ON `ebay_item_last_revise_attempted` (`ebay_store_id`);

COMMIT;