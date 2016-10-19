BEGIN;
--
-- Create model AmazonItemDescription
--
CREATE TABLE `amazon_item_descriptions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `description` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model AmazonItemFeature
--
CREATE TABLE `amazon_item_features` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `features` longtext NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model AmazonItemMarketPrice
--
CREATE TABLE `amazon_item_market_prices` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `market_price` numeric(15, 2) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model AmazonItemPrice
--
CREATE TABLE `amazon_item_prices` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `price` numeric(15, 2) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model AmazonItemQuantity
--
CREATE TABLE `amazon_item_quantites` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `quantity` smallint NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model AmazonItemTitle
--
CREATE TABLE `amazon_item_titles` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `asin` varchar(32) NOT NULL,
    `parent_asin` varchar(32) NULL,
    `title` longtext NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
CREATE INDEX `amazon_item_descriptions_62130e1b` ON `amazon_item_descriptions` (`asin`);
CREATE INDEX `amazon_item_descriptions_bb72ef9d` ON `amazon_item_descriptions` (`parent_asin`);
CREATE INDEX `amazon_item_features_62130e1b` ON `amazon_item_features` (`asin`);
CREATE INDEX `amazon_item_features_bb72ef9d` ON `amazon_item_features` (`parent_asin`);
CREATE INDEX `amazon_item_market_prices_62130e1b` ON `amazon_item_market_prices` (`asin`);
CREATE INDEX `amazon_item_market_prices_bb72ef9d` ON `amazon_item_market_prices` (`parent_asin`);
CREATE INDEX `amazon_item_prices_62130e1b` ON `amazon_item_prices` (`asin`);
CREATE INDEX `amazon_item_prices_bb72ef9d` ON `amazon_item_prices` (`parent_asin`);
CREATE INDEX `amazon_item_quantites_62130e1b` ON `amazon_item_quantites` (`asin`);
CREATE INDEX `amazon_item_quantites_bb72ef9d` ON `amazon_item_quantites` (`parent_asin`);
CREATE INDEX `amazon_item_titles_62130e1b` ON `amazon_item_titles` (`asin`);
CREATE INDEX `amazon_item_titles_bb72ef9d` ON `amazon_item_titles` (`parent_asin`);

COMMIT;