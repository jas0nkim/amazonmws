BEGIN;
--
-- Remove field message_id from ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` DROP COLUMN `message_id`;
--
-- Add field count to ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` ADD COLUMN `count` integer DEFAULT 0 NOT NULL;
ALTER TABLE `ebay_trading_api_errors` ALTER COLUMN `count` DROP DEFAULT;
--
-- Add field message_ids to ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` ADD COLUMN `message_ids` longtext NULL;
--
-- Add field severity_code to ebaytradingapierror
--
ALTER TABLE `ebay_trading_api_errors` ADD COLUMN `severity_code` varchar(32) NULL;
--
-- Alter field error_code on ebaytradingapierror
--
CREATE INDEX `ebay_trading_api_errors_severity_code_4239ce3b` ON `ebay_trading_api_errors` (`severity_code`);
COMMIT;