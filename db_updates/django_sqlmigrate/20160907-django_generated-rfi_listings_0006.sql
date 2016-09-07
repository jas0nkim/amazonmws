BEGIN;
--
-- Create model EbayStoreCategory
--
CREATE TABLE `ebay_store_categories` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `category_id` bigint NOT NULL UNIQUE,
    `parent_category_id` bigint NULL,
    `name` varchar(100) NOT NULL UNIQUE,
    `order` integer NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_store_id` integer unsigned NOT NULL);

ALTER TABLE `ebay_store_categories` ADD CONSTRAINT `ebay_store_categories_ebay_store_id_4b8cd9f4_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);

CREATE INDEX `ebay_store_categories_3ae127fc` ON `ebay_store_categories` (`ebay_store_id`);

COMMIT;