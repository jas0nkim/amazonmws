CREATE TABLE `zz__excl_brands` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(100) NOT NULL,
  `category` text DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_zz__excl_brands_brand_name` (`brand_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- AmazonBasics
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Amazon', NULL, NOW(), NOW());

-- AmazonBasics
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('AmazonBasics', NULL, NOW(), NOW());

-- Sigma Beauty
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Sigma Beauty', 'Beauty', NOW(), NOW());

-- EDOTech
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('EDOTech', 'Cell Phones & Accessories', NOW(), NOW());

-- Solid Tactical
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Solid Tactical', 'Hunting & Fishing', NOW(), NOW());

-- OXO
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('OXO', 'Home & Kitchen', NOW(), NOW());

-- Sonder Essentials
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Sonder Essentials', 'Home & Kitchen', NOW(), NOW());

-- Busy Life
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Busy Life', 'Automotive', NOW(), NOW());

-- simplehuman
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('simplehuman', 'Home & Kitchen', NOW(), NOW());

-- Nutri Bullet
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Nutri Bullet', 'Home & Kitchen', NOW(), NOW());

-- Altura Photo
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Altura Photo', 'Electronics', NOW(), NOW());

-- Spigen
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Spigen', 'Cell Phones & Accessories', NOW(), NOW());

-- Evelots
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Evelots', 'Home & Kitchen', NOW(), NOW());

-- Spoonk
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('Spoonk', 'Health & Personal Care', NOW(), NOW());

-- SONGMICS
INSERT INTO `zz__excl_brands` (`brand_name`, `category`, `created_at`, `updated_at`) VALUES ('SONGMICS', 'Home & Kitchen', NOW(), NOW());
