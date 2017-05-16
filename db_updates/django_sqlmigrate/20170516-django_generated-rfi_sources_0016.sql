BEGIN;
--
-- Add field meta_description to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `meta_description` varchar(255) NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `meta_description` DROP DEFAULT;
--
-- Add field meta_keywords to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `meta_keywords` varchar(255) NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `meta_keywords` DROP DEFAULT;
--
-- Add field meta_title to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `meta_title` varchar(255) NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `meta_title` DROP DEFAULT;
COMMIT;
