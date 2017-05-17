BEGIN;
--
-- Remove field ebay_store from amazonscrapetask
--
ALTER TABLE `amazon_scrape_tasks` DROP FOREIGN KEY `amazon_scrape_tasks_ebay_store_id_52bcbf43_fk_ebay_stores_id`;
ALTER TABLE `amazon_scrape_tasks` DROP COLUMN `ebay_store_id` CASCADE;
COMMIT;
