BEGIN;
--
-- Create model EbayItemStat
--
CREATE TABLE `ebay_item_stats` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `ebid` varchar(100) NOT NULL UNIQUE, `clicks` integer NULL, `watches` integer NULL, `solds` integer NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `ts` datetime NOT NULL);

COMMIT;