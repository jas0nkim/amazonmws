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
	`created_at`,
	`updated_at`
) VALUES (
	'redflagitems@gmail.com',
	'redflagitems777',
	NULL,
	'AgAAAA**AQAAAA**aAAAAA**hosBVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhDpGBqQudj6x9nY+seQ**KpIDAA**AAMAAA**xjNZU6YJeBz7IvO/PFjWzBJ3e647Uk/z3DrMd4f/njEDWaMwXYZU5wxpxcyVdw7mQ7k2gZNLRbZTLk7tBOqeCq1+U5eVNxe+r7cPl9iGrBoD/lDhh/VeQ5DUF6TuwS55gNLhL0C5sm8GHFc0n7SiBZCxD0Ql3S1q1F/Yp6Um4r0l0rou1tsOTbaKWhdhWKxijDy3vogdpa/kZ+xwMkIicjAEsseks0el4wBeZdaygrOvN1zM0l5uOMvRNC6DO9EqV+j7DMRCDqVOsXfe8zhHMCIgGfJJrUK6MJje5IjLrtDQVXQAFA7MTO57nQ8XpZ2LLviHbn/50+2FxhEOc7UI4pqRVCPcKmDcrxXYGeo/AXnR7w+WXw7cuhoTlC5OTY87A2Cbc4qikWkSNkmFCoNimaDy5UycCVVxnQxdWSgMH1a+NNt5bHvjlZw5DH4Zks0CwT0zl3n5G6RCIUZw8C6VQ+skeXXaUcXzT6LVWujb7UG6cmTHPqvmQ1MyyMZ7tam+RFYXwvzTFVwuF8XXsqdB7SfEN3TSFKZ2l0njJT+iybKUQFJ7NYk17GBFnv5HriGatM1Uj9KkWPI+HY4s3QFrPzaI+HO7/KQhB/dq3Ot6DJNNz3XlmpmHDz7KFeWw+1c88zsuPP9fcQmUs68zxECIbE3vu90Vk9oxeuhT3VKq/sKJo5LPMxOfCV8rK+XcgQhd1ev41/VUuHPXQmlLmQhSYUx0jmfyPFuaa7T7Za0gDaVxKZ0ljeNwZ5ImgdM5wT9w',
	'redflagitems',
	'oroojass@hotmail.com',
	'3',
	'2.50',
	'<p>All of our products come with free Standard Shipping. Handling time on our orders is between 1-2 business days. We will ship your item out using the most efficient carrier to your area (USPS, UPS, FedEx, Lasership, etc.). Once it has been shipped out, you should be receiving it within 2 - 6 business days depends on selected delivery service on checkout. Currently, we only ship to physical addresses located within the 48 contiguous states of America. APO/FPO addresses, Alaska and Hawaii are outside of our shipping zone.</p>',
	'<p>We only accept Paypal. Credit Card Payment Acceptable through PayPal.</p>',
	'<p>We fully guarantee all of our items. All items are Brand new and unused. 14 days refunds - we accept returns with defective or being pre-authorized. 10 percent restocking fee may apply.  Please contact us to get an authorization and returning address before sending the item back. Please leave a note with your eBay ID along with the returned item. Buyers pay shipping fees at their own cost to return products for exchange or refund. We will be responsible for the postage of replacements sending out.</p>',
	NOW(),
	NOW()
);

INSERT INTO `lookups` (
	`url`, 
	`description`
) VALUES (
	'http://www.amazon.com/s/ref=sr_ex_n_8?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721068011%2Cn%3A2229578011&bbn=721068011&ie=UTF8&qid=1443730551',
	'Amazon - Clothing, Shoes & Jewelry : Costumes & Accessories : Masks : Kids & Baby'
);

INSERT INTO `lookups` (
	`url`, 
	`description`
) VALUES (
	'http://www.amazon.com/s/ref=lp_721070011_ex_n_7?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721070011%2Cn%3A2229581011&bbn=721070011&ie=UTF8&qid=1443731015',
	'Amazon - Clothing, Shoes & Jewelry : Costumes & Accessories : More Accessories : Kids & Baby'
);

INSERT INTO `lookups` (
	`url`, 
	`description`
) VALUES (
	'http://www.amazon.com/gp/search/ref=sr_ex_n_9?rh=n%3A7141123011%2Cn%3A7586165011%2Cn%3A721067011%2Cn%3A2229575011&bbn=721067011&ie=UTF8&qid=1443731030',
	'Amazon - Clothing, Shoes & Jewelry : Costumes & Accessories : Hats & Caps : Kids & Baby'
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	1, 
	1, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	1, 
	2, 
	now(), 
	now()
);

INSERT INTO `lookup_ownerships` (
	`ebay_store_id`, 
	`lookup_id`, 
	`created_at`, 
	`updated_at`
) values (
	1, 
	3, 
	now(), 
	now()
);

UPDATE `ebay_items` SET `ebay_store_id` = 1 WHERE `ebay_store_id` = 0;
