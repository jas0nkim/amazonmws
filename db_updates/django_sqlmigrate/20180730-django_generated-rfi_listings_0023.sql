BEGIN;
--
-- Create model ArchivedEbayItem
--
CREATE TABLE `archived_ebay_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebay_store_id` integer NULL,
    `asin` varchar(32) NULL,
    `ebid` varchar(100) NOT NULL UNIQUE,
    `ebay_category_id` varchar(100) NULL,
    `eb_price` numeric(15, 2) NOT NULL,
    `quantity` smallint NULL,
    `quantity_sold` smallint NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model ArchivedEbayItemVariation
--
CREATE TABLE `archived_ebay_item_variations` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebay_item_id` integer NULL,
    `ebid` varchar(100) NOT NULL,
    `asin` varchar(32) NOT NULL,
    `specifics` varchar(255) NULL,
    `eb_price` numeric(15, 2) NOT NULL,
    `quantity` smallint NOT NULL,
    `quantity_sold` smallint NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);

CREATE INDEX `archived_ebay_items_ebay_store_id_09198ffe` ON `archived_ebay_items` (`ebay_store_id`);
CREATE INDEX `archived_ebay_items_asin_58005ed8` ON `archived_ebay_items` (`asin`);
CREATE INDEX `archived_ebay_items_ebay_category_id_04f20a2c` ON `archived_ebay_items` (`ebay_category_id`);
CREATE INDEX `archived_ebay_item_variations_ebay_item_id_85dc3ba9` ON `archived_ebay_item_variations` (`ebay_item_id`);
CREATE INDEX `archived_ebay_item_variations_ebid_8075ae4b` ON `archived_ebay_item_variations` (`ebid`);
CREATE INDEX `archived_ebay_item_variations_asin_91895473` ON `archived_ebay_item_variations` (`asin`);
COMMIT;