BEGIN;
--
-- Alter field name on ebaystorecategory
--
ALTER TABLE `ebay_store_categories` DROP INDEX `name`;

COMMIT;