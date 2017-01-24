BEGIN;
--
-- Add field status to aliexpressstore
--
ALTER TABLE `aliexpress_stores` ADD COLUMN `status` bool DEFAULT 1 NOT NULL;
ALTER TABLE `aliexpress_stores` ALTER COLUMN `status` DROP DEFAULT;
COMMIT;