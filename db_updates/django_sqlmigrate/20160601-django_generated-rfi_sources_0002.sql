BEGIN;
--
-- Add field specifications to amazonitem
--
ALTER TABLE `amazon_items` ADD COLUMN `specifications` longtext NULL;

COMMIT;