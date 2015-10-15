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
	'AgAAAA**AQAAAA**aAAAAA**RuMfVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AAkIuhCZaCpA2dj6x9nY+seQ**8P8CAA**AAMAAA**ALITZSRUzEzp8QJeEqchNVdMx/l6ri3kFik21V1BgmGWhJi+ofMNAbKRCM4yRLMQPP3X6rZaBj3/IyOGLcvoR0VoHSS8yCNsOb5j7E2WtAYqAAoNhbDA6yVzFQokahRwVx1J1N9M2ANpSlS8+flF0rET/A/Al8wOtIQg2leht8uKYsf4OiFRmPRAcQPF0deLnpMPLsTL4BF2UBRiFdvYtwc15oFnrr8Afg1/Kd7eleBsg9ITNJgmaixHuedH0nfXQkBtwf9VNszL5bHsAFDDthD+qUSo5NmuE16SRdFzJki73MdKYyZw8Or3scnZpN27y53fdjaZWG55N4BLBUccfMAneLrT9VnIB8cK8/c/nM/DSyX5cLqN6LD8uxK+mED4VpAZSKeX4q4hIdjhv4JG+lN4VA19lJssmmfZYnJ6p9SOUjDsRP44YLEe0/Ue6r8ahx71YKpGlAp2Oqog8sTXEI4bcNwFd8JV9QH5MFkHp596je8ggLcwgUvQj/9iTjOPnAEv+tGrhsXeheP/R0q5c1cgAjwDBo83xKlEInuOByvsJ/0Z+vRFKxKPjaWqf49fnLJjPNBjvXQ/V1/GW00tpFOekilI6cWZCeaLWET8hUMIPTVZNxX8eIbAzBVIKwqmgpkJWO6UjLJ3xDGjr1qDb55idNKmA4mLvunWL6o2KuU26aiPhxNWJzDjYT6B1Oz7TNSSbnayt30Ii3K7vrLSZfUzDjnMP7MrRsDFV2lhhn2DrC244uDWxaVVaw/MU/Iu',
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
