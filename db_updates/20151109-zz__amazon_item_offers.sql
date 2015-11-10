CREATE TABLE `zz__amazon_item_offers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `asin` varchar(32) DEFAULT NULL,
  `price` decimal(15,2) NOT NULL,
  `quantity` smallint(5) unsigned DEFAULT '0',
  `is_fba` smallint(3) DEFAULT '0',
  `merchant_id` varchar(32) DEFAULT NULL,
  `merchant_name` varchar(100) DEFAULT NULL,
  `revision` int(11) unsigned DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__amazon_item_offers_asin` (`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
