INSERT INTO `amazon_accounts` (
	`email`, 
	`password`, 
	`billing_postal`, 
	`created_at`,
	`updated_at`
) VALUES (
	'redflagitems.0020@gmail.com',
	'12ReDF002AZIt!em!s',
	'M5B0A5',
	NOW(),
	NOW()
);

INSERT INTO `ebay_store_amazon_accounts` (
	`ebay_store_id`, 
	`amazon_account_id`, 
	`created_at`,
	`updated_at`
) VALUES (
	'1',
	'1',
	NOW(),
	NOW()
);
