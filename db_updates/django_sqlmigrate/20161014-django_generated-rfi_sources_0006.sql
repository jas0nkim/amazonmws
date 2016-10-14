BEGIN;
--
-- Create model AmazonItemCachedHtmlPage
--
CREATE TABLE `amazon_item_cached_html_pages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `request_url` varchar(255) NOT NULL,
    `response_url` varchar(255) NOT NULL,
    `body` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);
CREATE INDEX `amazon_item_cached_html_pages_62130e1b` ON `amazon_item_cached_html_pages` (`asin`);
CREATE INDEX `amazon_item_cached_html_pages_fb103b87` ON `amazon_item_cached_html_pages` (`request_url`);
CREATE INDEX `amazon_item_cached_html_pages_a13b54a8` ON `amazon_item_cached_html_pages` (`response_url`);

COMMIT;