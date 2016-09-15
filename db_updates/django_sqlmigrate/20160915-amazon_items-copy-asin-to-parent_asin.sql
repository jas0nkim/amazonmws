BEGIN;
-- data migration - copy all amazon_items.asin to amazon_items.parent_asin
UPDATE `amazon_items` SET `parent_asin` = `asin`;
COMMIT;