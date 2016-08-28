BEGIN;
--
-- Add field feedback_left to ebayorder
--
ALTER TABLE `ebay_orders` ADD COLUMN `feedback_left` bool DEFAULT 0 NOT NULL;
ALTER TABLE `ebay_orders` ALTER COLUMN `feedback_left` DROP DEFAULT;

COMMIT;