ALTER TABLE `ebay_stores` ADD COLUMN `feedback_comment` text DEFAULT NULL AFTER `item_description_template`;
ALTER TABLE `ebay_stores` ADD COLUMN `message_on_shipping_subject` text DEFAULT NULL AFTER `feedback_comment`;
ALTER TABLE `ebay_stores` ADD COLUMN `message_on_shipping_body` text DEFAULT NULL AFTER `message_on_shipping_subject`;