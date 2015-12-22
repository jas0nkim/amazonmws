CREATE TABLE `amazon_accounts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `billing_postal` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `amazon_accounts_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


-- relationship table of ebay_stores & amazon_accounts

CREATE TABLE `ebay_store_amazon_accounts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ebay_store_id` int(11) unsigned NOT NULL,
  `amazon_account_id` int(11) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ebay_store_amazon_accounts_ebay_store_id` (`ebay_store_id`),
  KEY `ebay_store_amazon_accounts_amazon_account_id` (`amazon_account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `amazon_orders` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` varchar(100) NOT NULL,
  `asin` varchar(32) NOT NULL,
  `amazon_account_id` int(11) unsigned NOT NULL,
  `item_price` decimal(15,2) NOT NULL,
  `shipping_and_handling` decimal(15,2) NOT NULL,
  `tax` decimal(15,2) NOT NULL,
  `total` decimal(15,2) NOT NULL,
  `buyer_shipping_name` varchar(100) DEFAULT NULL,
  `buyer_shipping_street1` varchar(100) DEFAULT NULL,
  `buyer_shipping_street2` varchar(100) DEFAULT NULL,
  `buyer_shipping_city_name` varchar(100) DEFAULT NULL,
  `buyer_shipping_state_or_province` varchar(100) DEFAULT NULL,
  `buyer_shipping_country` varchar(100) DEFAULT NULL,
  `buyer_shipping_phone` varchar(100) DEFAULT NULL,
  `buyer_shipping_postal_code` varchar(100) DEFAULT NULL,
  `carrier` varchar(100) DEFAULT NULL,
  `tracking_number` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `amazon_orders_order_id` (`order_id`),
  KEY `amazon_orders_asin` (`asin`),
  KEY `amazon_orders_amazon_account_id` (`amazon_account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


-- relationship table of transactions & amazon_orders

CREATE TABLE `transaction_amazon_orders` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `transaction_id` int(11) unsigned NOT NULL,
  `amazon_order_id` int(11) unsigned DEFAULT NULL,
  `internal_error_type` smallint(5) DEFAULT NULL,
  `internal_error_message` varchar(255) DEFAULT NULL,
  `is_ordering_in_process` tinyint(3) DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `transaction_amazon_orders_transaction_id` (`transaction_id`),
  KEY `transaction_amazon_orders_amazon_order_id` (`amazon_order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
