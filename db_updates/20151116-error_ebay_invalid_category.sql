CREATE TABLE `error_ebay_invalid_category` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` varchar(100) NOT NULL,
  `asin` varchar(32) NOT NULL,
  `amazon_category` varchar(255) NOT NULL,
  `ebay_category_id` varchar(100) DEFAULT NULL,
  `request` text NOT NULL,
  `status` smallint(3) unsigned DEFAULT 0,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_error_ebay_invalid_category_message_id` (`message_id`),
  KEY `index_error_ebay_invalid_category_asin` (`asin`),
  KEY `index_error_ebay_invalid_category_amazon_category` (`amazon_category`),
  KEY `index_error_ebay_invalid_category_ebay_category_id` (`ebay_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;