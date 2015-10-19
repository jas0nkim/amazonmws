# Plans

## 2015-10-19

#### Developments

1. soap server + handling ebay notifications - with **pysimplesoap** lib
1. scrape watchcount.com
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com


## 2015-10-18

#### Developments

1. soap server + handling ebay notifications - failed to implement *spyne* lib 
1. scrape watchcount.com - cannot even started
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com

## 2015-10-16

#### Bigger plans / todos

1. improve scraper, monitoring system
1. transfer to linode server
1. improve mapping amazon category/items to ebay category - improved with rake
1. soap server + handling ebay notifications
1. amazon ordring automation - casperjs

#### Developments

1. improve scraper and item monitering system
	- one scraper for just collect amazon asin - selenium / phantomjs
	- one scraper for go over all amazon detail screen - scrapy
1. need to find a way to mapping amazon category and ebay category - improved with RAKE (Rapid Automatic Keyword Extraction algorithm) - [https://pypi.python.org/pypi/python-rake/1.0.5](https://pypi.python.org/pypi/python-rake/1.0.5), [https://github.com/aneesha/RAKE](https://github.com/aneesha/RAKE)

## 2015-10-15

#### Developments

1. setting up bakjin's application - improve application with site based
	- category/keyword based amazon item scraper - done
	- ebay application api with multiple users / tokens - done
	- setup linode servers - both application server, log server

## 2015-10-14

#### ebay store marketing / accounting

1. list the vaccum on ebay - done
1. post a comment on redflagdeals.com - done
	- [http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963](http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963)

#### Developments

1. setting up bakjin's application - improve application with site based
1. setup linode servers - both application server, log server


## 2015-10-13

#### Developments

1. setting up bakjin's application - improve application with site based - on progress
1. setup linode servers - both application server, log server


## 2015-10-10

#### ebay store marketing / accounting

1. proceed ebay item sold
	- questions: 
		- gyft.com cannot verify my mobile number. left a ticket - on process
		- amazon asks phone number of shipping information on checkout. may I give my phone number instead? - found buyer's phone number from **ebay.ca** management tool.

#### Developments

1. Auto-ordering - again...
	- soap with Spyne
	- navigate through amazon.com - must use casperjs, testing purpose. have to notify us as soon as possible


## 2015-10-09

#### ebay store marketing

1. research more about sales tax

#### Developments

1. Auto-ordering
	- soap with Spyne
	- navigate through amazon.com


## 2015-10-08

#### ebay store marketing

1. keep raising ebay feedbacks - done - 11 points

1. call ebay once feedback points get 10
	- called, but not resolved. received a ref# - 1-55275826862 - and will be resolved in 72 hours

1. meeting tonight, so what to ask:
	- monthly profit, monthly transaction - wbjworld
	- marketing other than feedbacks - pretty much nothing else than feedbacks
	- my items are not searchable, neither thecandidcow's ones are - wbjworld - not searchable either
	- notes:
		- purchase amazon gift card from [gyft.com]() - 2% cach back with paypal payment
		- [givingassistant.org]() - donation site - affiliation - 5% cash back on purchasing at amazon.com
		- tax rates depends on States

#### Developments

1. improve ebay api error handling - ebay\_trading\_api\_errors table - done

1. again... Auto-ordering, Auto-ordering, Auto-ordering!!!
	- soap is crazy... - understood pretty much
	- scrape and navigate amazon... - not yet


## 2015-10-07

#### ebay store marketing

1. keep raising ebay feedbacks - 7 points so far

#### Developments

1. Auto-ordering, Auto-ordering, Auto-ordering!!!


## 2015-10-06

#### ebay store marketing

1. keep raising ebay feedbacks - 4 points so far

#### Developments

1. update shipping policy template - done
	- add express shipping for $1.99 - extra money
	- make PO BOX available - but it will slow down your shipping - about 1-2 business days.

1. build automatic ordering system
	- check CasperJS
	- benchmark PriceYak


## 2015-10-05

#### ebay Store / paypal business account

1. call paypal to verify bank account and credit card - not necessary

1. call ebay about my listings not searchable at ebay.com - done

1. switch linked paypal account at ebay.ca - not necessary

1. raising ebay feedbacks

1. go though ebay store marketing section

#### Developments

1. simplify amazon item monitoring system - merge amazon item price and amazon item status into a single process - need to test more

1. run the script on production


## 2015-10-02

#### ebay Store

1. confirm Bank Account at paypal - done

2. subscribe to ebay Store Basic - done

3. work on ebay store settings
	- logo - done
	- search keywords - use google tool - done

#### Developments

1. monitor amazon item status changes - done

1. item inventory / quantity control - done

1. ebay notification
	- references
		- [http://developer.ebay.com/Devzone/guides/ebayfeatures/Notifications/Notifications.html]()
		- [http://developer.ebay.com/Devzone/XML/docs/HowTo/Notifications/Notifications_listing.html]()

	- using ebay_item_quantity.py scraper instead - done
		
1. create html template for item description - done
	- http://developer.ebay.com/DevZone/guides/ebayfeatures/Development/DescTemplates.html
	- use twitter bootstrap

