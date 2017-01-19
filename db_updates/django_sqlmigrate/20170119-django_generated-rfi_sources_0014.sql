BEGIN;
--
-- Remove field alxid from aliexpresscategory
--
ALTER TABLE `aliexpress_categories` DROP COLUMN `alxid` CASCADE;
COMMIT;