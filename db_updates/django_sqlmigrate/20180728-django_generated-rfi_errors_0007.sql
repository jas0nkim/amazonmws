BEGIN;
--
-- Add field http_status to amazonscrapeerror
--
ALTER TABLE `amazon_scrape_errors` ADD COLUMN `http_status` integer DEFAULT 0 NULL;
ALTER TABLE `amazon_scrape_errors` ALTER COLUMN `http_status` DROP DEFAULT;
--
-- Add field system_error_message to amazonscrapeerror
--
ALTER TABLE `amazon_scrape_errors` ADD COLUMN `system_error_message` varchar(255) NULL;
--
-- Alter field parent_asin on amazonscrapeerror
--
DROP INDEX `amazon_scrape_errors_parent_asin_47aff305` ON `amazon_scrape_errors`;
CREATE INDEX `amazon_scrape_errors_http_status_75b58442` ON `amazon_scrape_errors` (`http_status`);
CREATE INDEX `amazon_scrape_errors_system_error_message_bc5c0867` ON `amazon_scrape_errors` (`system_error_message`);
COMMIT;