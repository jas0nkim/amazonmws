CREATE TABLE `zz__amazon_bestsellers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `asin` varchar(32) NOT NULL,
  `bestseller_category` varchar(255) NOT NULL,
  `rank` smallint(5) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__amazon_bestsellers_asin` (`asin`),
  KEY `index_zz__amazon_bestsellers_bestseller_category` (`bestseller_category`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `zz__amazon_bestsellers_archived` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `asin` varchar(32) NOT NULL,
  `bestseller_category` varchar(255) NOT NULL,
  `rank` smallint(5) NOT NULL,
  `created_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `zz__amazon_bestsellers_archived_asin` (`asin`),
  KEY `zz__amazon_bestsellers_archived_bestseller_category` (`bestseller_category`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
