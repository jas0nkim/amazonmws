CREATE TABLE `discovered_items` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `url` text NOT NULL,
    `asin` varchar(32) NOT NULL,
    `title` text NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
);
