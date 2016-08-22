BEGIN;
--
-- Remove field amazon_order from transactionamazonorder
--
ALTER TABLE `transaction_amazon_orders` DROP FOREIGN KEY `transaction_amazon__amazon_order_id_f480905f_fk_amazon_orders_id`;
ALTER TABLE `transaction_amazon_orders` DROP COLUMN `amazon_order_id` CASCADE;
--
-- Remove field transaction from transactionamazonorder
--
ALTER TABLE `transaction_amazon_orders` DROP FOREIGN KEY `transaction_amazon_or_transaction_id_adcc4169_fk_transactions_id`;
ALTER TABLE `transaction_amazon_orders` DROP COLUMN `transaction_id` CASCADE;
--
-- Alter field creation_time on ebayorder
--
--
-- Delete model TransactionAmazonOrder
--
DROP TABLE `transaction_amazon_orders` CASCADE;

COMMIT;