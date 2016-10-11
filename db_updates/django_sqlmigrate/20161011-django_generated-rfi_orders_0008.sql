BEGIN;
--
-- Remove field asin from amazonorder
--
ALTER TABLE `amazon_orders` DROP COLUMN `asin`;

COMMIT;