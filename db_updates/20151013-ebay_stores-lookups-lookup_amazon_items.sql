CREATE TABLE `ebay_stores` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `token` text DEFAULT NULL,
  `store_name` varchar(100) DEFAULT NULL,
  `paypal_username` varchar(100) NOT NULL,
  `margin_percentage` smallint(5) DEFAULT '10',
  `margin_max_dollar` numeric(15,2) DEFAULT '10.00',
  `policy_shipping` text DEFAULT NULL,
  `policy_payment` text DEFAULT NULL,
  `policy_return` text DEFAULT NULL,
  `use_salestax_table` tinyint(3) DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `lookups` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `lookup_ownerships` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ebay_store_id` int(11) unsigned NOT NULL,
  `lookup_id` int(11) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_lookup_ownerships_ebay_store_id` (`ebay_store_id`),
  KEY `index_lookup_ownerships_lookup_id` (`lookup_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `lookup_amazon_items` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `lookup_id` int(11) unsigned NOT NULL,
  `amazon_item_id` int(11) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_lookup_amazon_items_lookup_id` (`lookup_id`),
  KEY `index_lookup_amazon_items_amazon_item_id` (`amazon_item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
