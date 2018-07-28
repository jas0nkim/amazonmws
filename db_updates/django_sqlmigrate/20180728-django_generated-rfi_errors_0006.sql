BEGIN;
--
-- Create model AmazonScrapeError
--
CREATE TABLE `amazon_scrape_errors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `html` longtext NOT NULL,
    `error_code` varchar(100) NULL,
    `description` longtext NULL,
    `asin` varchar(32) NULL,
    `parent_asin` varchar(32) NULL,
    `url` longtext NULL,
    `count` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);

CREATE INDEX `amazon_scrape_errors_error_code_66f81b91` ON `amazon_scrape_errors` (`error_code`);
CREATE INDEX `amazon_scrape_errors_asin_e91667f4` ON `amazon_scrape_errors` (`asin`);
CREATE INDEX `amazon_scrape_errors_parent_asin_47aff305` ON `amazon_scrape_errors` (`parent_asin`);
COMMIT;