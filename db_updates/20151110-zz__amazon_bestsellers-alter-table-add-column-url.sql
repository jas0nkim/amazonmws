ALTER TABLE `zz__amazon_bestsellers` ADD COLUMN `url` text NOT NULL after `bestseller_category`;
ALTER TABLE `zz__amazon_bestsellers_archived` ADD COLUMN `url` text NOT NULL after `bestseller_category`;