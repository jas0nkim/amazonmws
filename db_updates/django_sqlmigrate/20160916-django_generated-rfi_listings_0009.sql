BEGIN;
--
-- Create model EbayCategoryFeatures
--
CREATE TABLE `ebay_category_features` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ebay_category_id` varchar(100) NOT NULL UNIQUE,
    `ebay_category_name` varchar(255) NULL,
    `upc_enabled` varchar(100) NULL,
    `variations_enabled` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);

COMMIT;