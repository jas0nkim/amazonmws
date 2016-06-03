BEGIN;
--
-- Create model AmazonScrapeTask
--
CREATE TABLE `amazon_scrape_tasks` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `task_id` varchar(255) NOT NULL,
    `ebay_store_id` integer(11) unsigned NOT NULL,
    `asin` varchar(32) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
--
-- Add field category_url to ebaystorepreferredcategory
--
ALTER TABLE `ebay_store_preferred_categories` ADD COLUMN `category_url` longtext NOT NULL;
UPDATE `ebay_store_preferred_categories` SET `category_url` = '';
ALTER TABLE `amazon_scrape_tasks` ADD CONSTRAINT `amazon_scrape_tasks_asin_fd87fa45_fk_amazon_items_asin` FOREIGN KEY (`asin`) REFERENCES `amazon_items` (`asin`);
ALTER TABLE `amazon_scrape_tasks` ADD CONSTRAINT `amazon_scrape_tasks_ebay_store_id_52bcbf43_fk_ebay_stores_id` FOREIGN KEY (`ebay_store_id`) REFERENCES `ebay_stores` (`id`);
CREATE INDEX `amazon_scrape_tasks_57746cc8` ON `amazon_scrape_tasks` (`task_id`);
CREATE INDEX `amazon_scrape_tasks_62130e1b` ON `amazon_scrape_tasks` (`asin`);
CREATE INDEX `amazon_scrape_tasks_3ae127fc` ON `amazon_scrape_tasks` (`ebay_store_id`);

COMMIT;