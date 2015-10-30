INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/tools-gadgets/b/ref=dp_bc_3?ie=UTF8&node=289754',
	'Amazon - Home & Kitchen : Kitchen & Dining : Kitchen Utensils & Gadgets'
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	1, 
	13, 
	now(), 
	now()
);

-- drop all ownerships for kat.burr
DELETE FROM `lookup_ownerships` WHERE `ebay_store_id` = 2;

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	2, 
	13, 
	now(), 
	now()
);
