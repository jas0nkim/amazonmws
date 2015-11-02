CREATE TABLE `zz__amazon_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asin` varchar(32) NOT NULL,
  `url` text NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `title` text NOT NULL,
  `price` decimal(15,2) NOT NULL,
  `quantity` smallint(5) unsigned DEFAULT '0',
  `features` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `review_count` smallint(5) unsigned DEFAULT '0',
  `avg_rating` float unsigned DEFAULT '0',
  `is_fba` smallint(3) DEFAULT '0',
  `is_fba_by_other_seller` smallint(3) DEFAULT '0',
  `is_addon` smallint(3) DEFAULT '0',
  `status` smallint(3) DEFAULT '1',
  -- `ebay_category_id` varchar(32) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__amazon_items_asin` (`asin`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `zz__amazon_item_pictures` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `asin` varchar(32) NOT NULL,
  `picture_url` varchar(255) NOT NULL,
  -- `ebay_picture_url` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__amazon_item_pictures_amazon_asin` (`asin`),
  KEY `index_zz__amazon_item_pictures_amazon_picture_url` (`picture_url`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

