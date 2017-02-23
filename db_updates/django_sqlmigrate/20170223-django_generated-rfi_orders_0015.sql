BEGIN;
--
-- Rename field amount on ebayorderreturn to est_refund_amount
--
ALTER TABLE `ebay_order_returns` CHANGE `amount` `est_refund_amount` numeric(15, 2) NOT NULL;
--
-- Add field act_refund_amount to ebayorderreturn
--
ALTER TABLE `ebay_order_returns` ADD COLUMN `act_refund_amount` numeric(15, 2) NULL;
ALTER TABLE `ebay_order_returns` ALTER COLUMN `act_refund_amount` DROP DEFAULT;
COMMIT;