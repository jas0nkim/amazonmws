ALTER TABLE `ebay_stores` ADD COLUMN `fixed_salestax_percentage` smallint(5) DEFAULT '10' AFTER `use_salestax_table`;