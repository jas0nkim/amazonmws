CREATE TABLE `zz__a_to_b_category_maps` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `amazon_category` varchar(255) NOT NULL,
  `ebay_category_id` varchar(100) NOT NULL,
  `ebay_category_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__a_to_b_category_maps_amazon_category` (`amazon_category`),
  KEY `index_zz__a_to_b_category_maps_ebay_category_id` (`ebay_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

