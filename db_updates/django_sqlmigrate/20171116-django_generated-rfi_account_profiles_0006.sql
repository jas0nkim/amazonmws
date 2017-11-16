BEGIN;
--
-- Add field message_on_return_request_body to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `message_on_return_request_body` longtext NULL;
--
-- Add field message_on_return_request_subject to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `message_on_return_request_subject` longtext NULL;
COMMIT;