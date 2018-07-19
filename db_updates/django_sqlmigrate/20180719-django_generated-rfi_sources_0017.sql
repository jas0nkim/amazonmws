BEGIN;
--
-- Alter field meta_description on amazonitem
--
ALTER TABLE `amazon_items` MODIFY `meta_description` longtext NULL;
--
-- Alter field meta_keywords on amazonitem
--
ALTER TABLE `amazon_items` MODIFY `meta_keywords` longtext NULL;
--
-- Alter field meta_title on amazonitem
--
ALTER TABLE `amazon_items` MODIFY `meta_title` longtext NULL;
COMMIT;