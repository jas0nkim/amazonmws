BEGIN;
--
-- Add field creditcard_number to amazonaccount
--
ALTER TABLE `amazon_accounts` ADD COLUMN `creditcard_number` varchar(100) NULL;
ALTER TABLE `amazon_accounts` ALTER COLUMN `creditcard_number` DROP DEFAULT;
--
-- Add field status to amazonaccount
--
ALTER TABLE `amazon_accounts` ADD COLUMN `status` bool DEFAULT 1 NOT NULL;
ALTER TABLE `amazon_accounts` ALTER COLUMN `status` DROP DEFAULT;

COMMIT;