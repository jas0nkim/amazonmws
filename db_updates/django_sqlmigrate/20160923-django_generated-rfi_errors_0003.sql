BEGIN;
--
-- Remove field amazon_item from ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` DROP FOREIGN KEY `ebay_trading_api_errors_asin_123d7ef6_fk_amazon_items_asin`;
-- ALTER TABLE `ebay_trading_api_errors` DROP COLUMN `asin` CASCADE;
--
-- Remove field ebay_item from ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` DROP FOREIGN KEY `ebay_trading_api_errors_ebid_67f91b0a_fk_ebay_items_ebid`;
-- ALTER TABLE `ebay_trading_api_errors` DROP COLUMN `ebid` CASCADE;
--
-- Remove field amazon_item from errorebayinvalidcategory
--
ALTER TABLE `error_ebay_invalid_category` DROP FOREIGN KEY `error_ebay_invalid_category_asin_166b2a2f_fk_amazon_items_asin`;
-- ALTER TABLE `error_ebay_invalid_category` DROP COLUMN `asin` CASCADE;
--
-- Add field asin to ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` MODIFY COLUMN `asin` varchar(32) NULL;
ALTER TABLE `ebay_trading_api_errors` ALTER COLUMN `asin` DROP DEFAULT;
--
-- Add field ebid to ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` MODIFY COLUMN `ebid` varchar(100) NULL;
ALTER TABLE `ebay_trading_api_errors` ALTER COLUMN `ebid` DROP DEFAULT;
--
-- Add field asin to errorebayinvalidcategory
--
ALTER TABLE `error_ebay_invalid_category` MODIFY COLUMN `asin` varchar(32) NULL;
ALTER TABLE `error_ebay_invalid_category` ALTER COLUMN `asin` DROP DEFAULT;
CREATE INDEX `ebay_trading_api_errors_62130e1b` ON `ebay_trading_api_errors` (`asin`);
CREATE INDEX `ebay_trading_api_errors_26635314` ON `ebay_trading_api_errors` (`ebid`);
CREATE INDEX `error_ebay_invalid_category_62130e1b` ON `error_ebay_invalid_category` (`asin`);

COMMIT;