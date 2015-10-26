INSERT INTO `ebay_stores` (
	`email`, 
	`username`, 
	`password`, 
	`token`, 
	`token_expiration`,
	`store_name`, 
	`paypal_username`, 
	`margin_percentage`, 
	`margin_max_dollar`, 
	`policy_shipping`, 
	`policy_payment`, 
	`policy_return`,
	`use_salestax_table`,
	`item_description_template`,
	`created_at`,
	`updated_at`
) VALUES (
	'baekjine@gmail.com',
	'wbjworld',
	'Qorwls77!',
	'AgAAAA**AQAAAA**aAAAAA**sjsuVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFloSkAJaBoASdj6x9nY+seQ**8P8CAA**AAMAAA**3mHw2di9uLfUOym5R8dGFcPOlJ1uE9KZeq2qsV++C61/Qq6ChojtWPSbaEBjDtja9kwnsVjT+jldmMz7cj8mI6YZOSydSWOBLbe5wh9maMJPg1KgHXgR4OQWuDFF6GYWTBukzFBbWv9zRVUrfi49kPQHzh9qnWs3TPQI48RmO7o0j9YsmWWVFutgFv5kC2MHdhYCuJvrxyIgI6w9NZXmylhqdnAqn3X1pfTwhurGzNaEUkInh+U9b9xo/V0ikqr9JOdEUoO6tuQ2Weky9ojc4d6SHzZnptGIvqC08iYYQVZgdzfUolg6J5BIuOBn+wU5+oWqAaPBTOIaiFR0RmWsY3V9sbA1oN50f8Mk+q524pH2XzN2nRINAmzflY6HrEsswWPYY9YvO92m1pRgee4NW8VmQFMse/p3RiIKZligxZxWAL1zY8J5eb2Paaclr1t5GbKjq744WyGmvQRNFPaEU6Z+6cFOey83gW+pORr7IE2WJf5BQJ26dC/oguvCnFbQNlcvhUDnMHXxVTW6ZV4TOASqrPRZSO9KMfDjc63c3CspL21SnwV9MZPO0VrljIlFkVCFgTSEObyERyqH0D4onyE9F9ogp6+Il9sNtJ18cexvN5qpLqx7mdplTTyth/y+8Wyc/vKMm+ZcP33dNDssmEAbaNVO8mnDW4YKvoZAyKtG+f03cnzJ4RHlFq8kDb0SgN6XTOYqnqqBp2y6j9xgxV8tAtq2E4CSBRz7kAkjLois1SFpsLltXyXJqJZiFrL2',
	'2017-04-18',
	'wbjworld',
	'baekjine@gmail.com',
	'10',
	'2.50',
	NULL,
	NULL,
	NULL,
	1,
	'<!-- Zinc EPID: [ASIN] -->
<font size="6" color="blue">Welcome To BJWorld!</font>
<BR><BR>
<B><font size="4">{{ title }}</font></B>
<BR>
<BR><BR>
<B>Product Description</B>
<BR><BR>
{{ description }}
<BR><BR>
<B>Product Features</B>
<BR><BR>
{{ features }}',
	NOW(),
	NOW()
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/Makeup-Brushes-Tools-Accessories/b/ref=dp_bc_3?ie=UTF8&node=11059391',
	'Amazon - Beauty : Tools & Accessories : Makeup Brushes & Tools'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/cell-phone-car-accessories/b/ref=dp_bc_3?ie=UTF8&node=2407759011',
	'Amazon - Cell Phones & Accessories : Accessories : Car Accessories'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/b/ref=dp_bc_3?ie=UTF8&node=12896641',
	'Amazon - Arts, Crafts & Sewing : Painting, Drawing & Art Supplies : Drawing'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/b/ref=dp_bc_3?ie=UTF8&node=3737951',
	'Amazon - Patio, Lawn & Garden : Pest Control : Repellents'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/Networking-Computer-Add-Ons-Computers/b/ref=dp_bc_3?ie=UTF8&node=172504',
	'Amazon - Electronics : Computers & Accessories : Networking Products'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/small-animals-exercise-wheels/b/ref=dp_bc_3?ie=UTF8&node=2975523011',
	'Amazon - Pet Supplies : Small Animals : Exercise Wheels'
);

INSERT INTO `lookups` (
	`spider_name`,
	`url`, 
	`description`
) VALUES (
	'keywords_dblookup',
	'http://www.amazon.com/brain-teasers/b/ref=dp_bc_3?ie=UTF8&node=166360011',
	'Amazon - Toys & Games : Puzzles : Brain Teasers'
);


INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	6, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	7, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	8, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	9, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	10, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	11, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	3, 
	12, 
	now(), 
	now()
);
