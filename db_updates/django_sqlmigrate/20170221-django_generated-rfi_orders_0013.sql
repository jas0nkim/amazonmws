BEGIN;
--
-- Alter field comments on ebayorderreturn
--
ALTER TABLE `ebay_order_returns` MODIFY `comments` longtext NULL;
COMMIT;