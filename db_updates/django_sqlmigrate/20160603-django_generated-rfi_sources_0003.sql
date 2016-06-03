BEGIN;
--
-- Add field avg_rating to amazonbestseller
--
ALTER TABLE `amazon_bestsellers` ADD COLUMN `avg_rating` double precision DEFAULT 0 NULL;
ALTER TABLE `amazon_bestsellers` ALTER COLUMN `avg_rating` DROP DEFAULT;
--
-- Add field review_count to amazonbestseller
--
ALTER TABLE `amazon_bestsellers` ADD COLUMN `review_count` smallint DEFAULT 0 NULL;
ALTER TABLE `amazon_bestsellers` ALTER COLUMN `review_count` DROP DEFAULT;

COMMIT;