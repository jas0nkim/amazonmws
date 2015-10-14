INSERT INTO `ebay_stores` (
	`email`, 
	`username`, 
	`password`, 
	`token`, 
	`store_name`, 
	`paypal_username`, 
	`margin_percentage`, 
	`margin_max_dollar`, 
	`policy_shipping`, 
	`policy_payment`, 
	`policy_return`,
	`use_salestax_table`,
	`created_at`,
	`updated_at`
) VALUES (
	'Kate_chun@hotmail.com',
	'Kat.burr',
	'Sihyun8!',
	'AgAAAA**AQAAAA**aAAAAA**y8YeVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AGmIeoDZiBpQWdj6x9nY+seQ**8P8CAA**AAMAAA**ROenUuvFASJWgci56fhL7s6YEY8sUkk0WToEdiClISbmmoZNnlSW8psbuEWyaDP0ItxOpOQ6oIwGGvSr2xt2CF/+vjJw72dqJBHh5n+1LXeB9EjkQiF67dkW1REn5V77x6krqF6opXm+lrLXFEXeH90dbfkSjhM4Z8fBHJqnZ9FP79Slgoc+iG5EgQkG6MbxOC2Ko/UlXzOL7tM3Ei6ju2SMU+cFsiIaV75LB9fYO4D9S11sr6W/e1KFK3521nkhDPGYGbfn+/lBzFS7T+51Um7hQKl+B292MQ5jnQvu9TvqpZzsOvg6NP/dckttwvm1/J8FI+s3oy9KL1hFta86Lxw/u89kTY4iR0kSd/5YhgUuo+4z82Rb9/pd77rJWUds/S3j3jGcbJkQmVp03B4+eq2Zj2nuZpr3R+91jLXXNa8duMCUmRB9OQBzmlDrdhdoo3n4qHQ+beJx9Ek+z1WhT/9AwjdCj2zaD2kWHeL0EeJk47S0/x15QqviWxkmlV/gr642acM8B1fi58CIY3onisO+hCgGy4iWBv18Mdrxd+8mlKDgO4orkaa37DHYneqS0te0uLi0K28dcc+hQfM99VzOPW9Ba7LxN07VHshAM8I6vj9Tg3Qqfc6ZCF5WCZk+Rx9VFbsoSNKCeEmhJY1TjMrSak6bSqjPfcObxFhpeDxnYZoM8wfCNHdbXGn62WXr6K6KjAipaWsMZhr45L+30mUzZQRtAjIavvB5MADY/k+cyH/xIdQFir+nh+far4Bl',
	'kat.burr',
	'Kate_chun@hotmail.com',
	'10',
	'2.50',
	NULL,
	NULL,
	NULL,
	1,
	NOW(),
	NOW()
);

INSERT INTO `lookups` (
	`url`, 
	`description`
) VALUES (
	'http://www.amazon.com/s/ref=nb_sb_ss_c_0_9?url=search-alias%3Dautomotive&field-keywords=car+accessories&sprefix=car+accessories%2Cbaby-products%2C149&rh=n%3A15684181%2Ck%3Acar+accessories&ajr=0',
	'Amazon - Automotive : car accessories [keywords]'
);

INSERT INTO `lookups` (
	`url`, 
	`description`
) VALUES (
	'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbaby-products&field-keywords=baby+toy&rh=n%3A165796011%2Ck%3Ababy+toy&ajr=0',
	'Amazon - Baby : baby toy [keywords]'
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	2, 
	4, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	2, 
	5, 
	now(), 
	now()
);
