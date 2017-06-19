BEGIN;
--
-- Add field refund_issued_date to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `refund_issued_date` datetime NULL;
ALTER TABLE `ebay_order_returns` ALTER COLUMN `refund_issued_date` DROP DEFAULT;
COMMIT;
