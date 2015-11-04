CREATE TABLE `zz__amazon_bestsellers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bestseller_category` varchar(255) NOT NULL,
  `rank` smallint(5) NOT NULL,
  `asin` varchar(32) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__amazon_bestsellers_bestseller_category` (`bestseller_category`),
  KEY `index_zz__amazon_bestsellers_rank` (`rank`),
  KEY `index_zz__amazon_bestsellers_asin` (`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `zz__amazon_bestsellers_archived` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `bestseller_category` varchar(255) NOT NULL,
  `rank` smallint(5) NOT NULL,
  `asin` varchar(32) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `zz__amazon_bestsellers_archived_bestseller_category` (`bestseller_category`),
  KEY `zz__amazon_bestsellers_archived_rank` (`rank`),
  KEY `zz__amazon_bestsellers_archived_asin` (`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
