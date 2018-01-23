BEGIN;
--
-- Alter field error_code on ebaynotificationerror
--
CREATE INDEX `ebay_notification_errors_error_code_23a8b5d8` ON `ebay_notification_errors` (`error_code`);
--
-- Alter field error_code on ebaytradingapierror
--
CREATE INDEX `ebay_trading_api_errors_error_code_c8f313b5` ON `ebay_trading_api_errors` (`error_code`);
COMMIT;