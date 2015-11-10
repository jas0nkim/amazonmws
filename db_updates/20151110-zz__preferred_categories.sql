CREATE TABLE `zz__ebay_store_preferred_categories` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ebay_store_id` int(11) unsigned NOT NULL,
  `category_type` enum('amazon', 'amazon_bestseller') NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `max_items` int(11) unsigned DEFAULT '0',
  `priority` smallint(5) unsigned DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__ebay_store_preferred_categories_ebay_store_id` (`ebay_store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
