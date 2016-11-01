BEGIN;
--
-- Add field has_sizechart to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `has_sizechart` bool DEFAULT 0 NOT NULL;
ALTER TABLE `amazon_items` ALTER COLUMN `has_sizechart` DROP DEFAULT;

COMMIT;