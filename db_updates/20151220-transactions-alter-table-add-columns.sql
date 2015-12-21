ALTER TABLE `transactions` ADD COLUMN `carrier` varchar(100) DEFAULT NULL AFTER `external_transaction_status`;
ALTER TABLE `transactions` ADD COLUMN `tracking_number` varchar(100) DEFAULT NULL AFTER `carrier`;
