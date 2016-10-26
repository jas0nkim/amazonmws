BEGIN;
--
-- Remove field ebay_store from ebayitemrepricedhistory
--
ALTER TABLE `ebay_item_repriced_histories` DROP FOREIGN KEY `ebay_item_repriced_hist_ebay_store_id_08ae0acc_fk_ebay_stores_id`;
ALTER TABLE `ebay_item_repriced_histories` DROP COLUMN `ebay_store_id` CASCADE;
--
-- Delete model EbayItemRepricedHistory
--
DROP TABLE `ebay_item_repriced_histories` CASCADE;

COMMIT;