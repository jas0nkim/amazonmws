BEGIN;
--
-- Create model EbayPicture
--
CREATE TABLE `ebay_pictures` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `source_picture_url` varchar(255) NOT NULL,
    `picture_url` varchar(255) NOT NULL,
    `base_url` varchar(255) NOT NULL,
    `full_url` varchar(255) NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL
);
--
-- Create model EbayPictureSetMember
--
CREATE TABLE `ebay_picture_set_members` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `member_url` varchar(255) NOT NULL,
    `picture_height` smallint NULL,
    `picture_width` smallint NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `ts` datetime NOT NULL,
    `ebay_picture_id` integer NOT NULL
);
CREATE INDEX `ebay_pictures_8bde78c2` ON `ebay_pictures` (`source_picture_url`);
CREATE INDEX `ebay_pictures_b7e31e55` ON `ebay_pictures` (`picture_url`);
CREATE INDEX `ebay_pictures_63769eef` ON `ebay_pictures` (`base_url`);
CREATE INDEX `ebay_pictures_7b63d87c` ON `ebay_pictures` (`full_url`);
ALTER TABLE `ebay_picture_set_members` ADD CONSTRAINT `ebay_picture_set_me_ebay_picture_id_7f5fba1b_fk_ebay_pictures_id` FOREIGN KEY (`ebay_picture_id`) REFERENCES `ebay_pictures` (`id`);
CREATE INDEX `ebay_picture_set_members_03ba4b6f` ON `ebay_picture_set_members` (`member_url`);
CREATE INDEX `ebay_picture_set_members_cc2d498f` ON `ebay_picture_set_members` (`ebay_picture_id`);

COMMIT;