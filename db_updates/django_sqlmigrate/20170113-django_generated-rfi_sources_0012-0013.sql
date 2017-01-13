BEGIN;
--
-- Delete model AliexpressStore
--
DROP TABLE `aliexpress_stores` CASCADE;
--
-- Create model AliexpressStore
--
CREATE TABLE `aliexpress_stores` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `store_id` varchar(100) NOT NULL,
    `store_name` varchar(255) NULL,
    `company_id` varchar(100) NULL,
    `owner_member_id` varchar(100) NULL,
    `store_location` varchar(255) NULL,
    `store_opened_since` date NULL,
    `deliveryguarantee_days` varchar(100) NULL,
    `return_policy` varchar(255) NULL,
    `is_topratedseller` bool NOT NULL,
    `has_buyerprotection` bool NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL);

CREATE INDEX `aliexpress_stores_7473547c` ON `aliexpress_stores` (`store_id`);
CREATE INDEX `aliexpress_stores_447d3092` ON `aliexpress_stores` (`company_id`);
CREATE INDEX `aliexpress_stores_9adb17cb` ON `aliexpress_stores` (`owner_member_id`);
COMMIT;
