BEGIN;
--
-- Create model AmazonItemApparel
--
CREATE TABLE `amazon_item_apparels` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `parent_asin` varchar(32) NOT NULL,
    `size_chart` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
CREATE INDEX `amazon_item_apparels_bb72ef9d` ON `amazon_item_apparels` (`parent_asin`);

COMMIT;