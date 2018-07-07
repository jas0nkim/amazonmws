BEGIN;
--
-- Add field oauth_refresh_token to ebaystore
--
ALTER TABLE `ebay_stores` ADD COLUMN `oauth_refresh_token` longtext NULL;
COMMIT;