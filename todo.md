# Plans

### Week of 2015-11-08 - 2015-11-15

- scrapy amzn - complete migration
- move on to ebay notification listener

----------------------------------------
#### 2015-11-15

##### Development

1. scrape amazon and list new items
	- zz\_\_ebay\_store\_preferred\_categories
1. ebay notification listeners
	- add more listeners
		- on end list
1. auto-ordering to amazon.com - casperjs

----------------------------------------
#### 2015-11-14

##### Development

1. scrape amazon and list new items
	- zz\_\_ebay\_store\_preferred\_categories
1. ebay notification listeners
	- double check the error - done
	- add more listeners
		- on end list
1. auto-ordering to amazon.com - casperjs
1. graylog2 stability - improved

----------------------------------------
#### 2015-11-13

##### Development

1. tor + privoxy linode config check - done
1. amazon cd/dvd item scraping / breadcrumb.... - done
1. amazon keyword + category scraping - done
1. amazon_items - add column brand - done
1. add table - excl_brands - done
1. bug fix on ebay notification listners - done(?)

----------------------------------------
#### 2015-11-12

##### Development & Deployment

1. deploy and test
1. refactor php-soap/python-restful notif-listeners
1. implement more ebay notif-listeners

----------------------------------------
#### 2015-11-11

##### Development

1. setup tor + privoxy on production server
1. finalize ebay listing script - done
1. pricewatch script - done
	- use AmazonPricewatchSpider
1. migration:
	1. scrape amazon best sellers
	1. backup production db and copy into staging db
	1. migrate amazon\_items => zz\_\_amazon\_items
		- run /zz\_migration/mg\_amazon\_items.py
	1. migrate lookup\_ownerships => zz\_\_ebay\_store\_preferred\_categories
		- manual migration
	1. add more on zz\_\_ebay\_store\_preferred\_categories
	1. run listing at staging - for testing

1. (minor) log scraper errors in db

----------------------------------------
#### 2015-11-10

##### Development

1. zz\_\_preferred\_categories - done
1. setup tor + privoxy on production server
1. migrate old data to new database tables - partially done
	- grep all 'asin' from amazon\_items table
	- scrape with 'amazon\_asin' scraper
	- remove ebay\_items.amazon\_item\_id column (deprecated)
	- refactor /amazonmws/ebaystore/listing.py
		- with zz\_\_preferred\_categories table
	- refactor /amazonmws/monitor/amazon\_item\_monitor.py
		- use AmazonPricewatchSpider

1. (minor) log scraper errors in db

----------------------------------------
#### 2015-11-09

##### Development

1. scrapy + stem + privoxy + TOR - amazon.com scrape - done - now need to apply to production
			
		https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853

		https://github.com/aivarsk/scrapy-proxies (old)
		http://proxylist.hidemyass.com/ (old)		
		
		best practice:
		http://blog.privatenode.in/torifying-scrapy-project-on-ubuntu/
		https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
		
1. workaround copyright issue against ebay policy
1. new table zz\_\_amazon\_item\_offers

----------------------------------------

### Week of 2015-11-01 - 2015-11-07

- scrapy only based scraper
- amazon scrapy - best seller variation
- manual asin upload with csv

----------------------------------------
#### 2015-11-06

##### Marketing

1. DS Domination [http://dsdomination.com/](http://dsdomination.com/)

##### Development

1. set ip proxies - partially done... need to parse email and save IPs in database - disabled proxy middleware due to poor speed/conneciton. obay robots.txt instead... all /gp/offer-listing/ pages are blocked by robots.txt. considering TOR... for them
			
		https://github.com/aivarsk/scrapy-proxies
		http://proxylist.hidemyass.com/

1. set random user agents for scrapy - done with middleware
1. workaround copyright issue against ebay policy
1. column added in zz\_\_amazon\_items - done

		market_price
		merchant_id
		merchant_name

1. new table zz\_\_amazon\_item\_offers

----------------------------------------
#### 2015-11-05

##### Development

1. urgent!! - moved to next day
	- set ip proxies
			
			https://github.com/aivarsk/scrapy-proxies
			http://proxylist.hidemyass.com/
	- set random user agents for scrapy
	- workaround copyright issue against ebay policy

----------------------------------------
#### 2015-11-04

##### Development

1. scrapers
	- amazon best sellers - done
	- pricewatch (repricer) - done
1. ebay\_accounts (old ebay\_stores) - no need
	- ebay\_account\_preferences - no need

----------------------------------------
#### 2015-11-03

##### Development

1. scrapers
	- apply graylog - done
	- scraper for update/repricing amazon items (list of asin based scraper) - pretty much done
	- find/store ebay category id - done
		- related table: a\_to\_e\_category\_maps 

----------------------------------------
#### 2015-11-02

##### Development

1. scrapers - pretty much stabled...
	- scrapy only based amazon scraper

----------------------------------------
#### 2015-11-01

##### Development

1. scrapers - on progress
	- scrapy only based amazon scraper

----------------------------------------
#### 2015-10-30

##### Development - let's fix all issues today

1. ebay notification
	- store information to db on transaction complete
1. cronjob setup on app server - finally found the issue!
1. scrapers
	- research scrapy + scrapyd, and start refactoring
		- scrapyd is not very necessary at this time...
	- better try scrapy with looking after XHR requests [http://stackoverflow.com/a/8594831](http://stackoverflow.com/a/8594831)
	- refactor scrapers - using scrapy only. pull out selenium + phantomjs... too slow

----------------------------------------
#### 2015-10-29

##### ebay Compatible Application Check

1. approved!!

##### Development

1. new amazon item status - excluded - done
	- should not be updated/listed
	- need to update related ebay items entry as well - set to inactive
1. ebay notification - almost done - need to find a small bug to fix
	- build 'transactions' db table based on ebay provided information
1. cronjob setup on app server
	- might need to use python schedule instead (crontab cannot run python script. don't know why)
	- investigate more why cronjob doesn't work...
1. scrapers
	- research scrapy + scrapyd, and start refactoring
	- multi-thread scraping needed.

----------------------------------------
#### 2015-10-28

##### ebay store marketing

1. limit raised to 175 items!

##### ebay Compatible Application Check

1. must submit the application by completing the form 'app check' - application submitted on Oct 29th 6AM

##### BUG ON PRODUCTION

1. update all ebay item description - reached api limit. postpond to tomorrow. should apply [Compatible Application Check](https://go.developer.ebay.com/compatible-application-check-and-checklist-going-live)
	- related links
		- [http://developer.ebay.com/DevZone/guides/ebayfeatures/basics/Call-UsingLiveData.html#CompatibleApplicationCheck](http://developer.ebay.com/DevZone/guides/ebayfeatures/basics/Call-UsingLiveData.html#CompatibleApplicationCheck)
		- [https://go.developer.ebay.com/introduction-logos](https://go.developer.ebay.com/introduction-logos)
	- use / modify revise_items.py

##### Development

1. complete bakjin's listing - done, but need to revise descriptions
1. cronjob (or python schedule) for tasks
1. ebay notification
	- debug object transferred to php soap
	- watch any receiving notifications
	- handle ItemSold/FixedPriceTransaction/AuctionCheckoutComplete events

----------------------------------------
#### 2015-10-27

##### ebay store marketing

1. refresh all items - done

##### Development

1. ebay notification - still learning ebay information
	- watch any receiving notifications
	- handle ItemSold/FixedPriceTransaction/AuctionCheckoutComplete events
1. scrapers - research scrapy + scrapyd, and start refactoring - multi-thread scraping...
1. cronjob setup on app server - need to implement lock files for each tasks - avoid any over-runs - going to use python schedule instead (crontab cannot run python script. don't know why)

----------------------------------------
#### 2015-10-26

##### ebay store marketing

1. call and increase limit - cannot made today. should call back on Friday (Oct 30th)
1. send thank you messages to buyers - done

##### Development

1. ebay notification
	- setup on linode - done (both soap/restful. restrict restful access by ip)
	- event handling - ItemSold - failed to receive notifications..
1. need to improve amazon.com scraper - filter prime at list screens... - takes a lot of time to go over each detail screens... - need to improve all scrapers! (very slow)

----------------------------------------
#### 2015-10-25

##### Development

1. setup bakjin's account
	- improve scraper - get ebay category id based on 1) amazon category or 2) title at scraping - done
	- create table ebay\_store\_profiles, and improve ebay store feature - postponed

----------------------------------------
#### 2015-10-24

##### Deployment

1. install blueprint at linode appserver and reverse-engineering and build shell script file. - done

----------------------------------------
#### 2015-10-23

##### Developments / Deployment

1. write shell script - securing_server.sh - done
1. deploy app server to linode - done
1. deploy log server to linode - done

----------------------------------------
#### 2015-10-22

##### Developments

1. move config to root directory - done
1. make sure every scripts should be runnable via physical path - done
1. setup apache server config for both php soap and python restful servers (Macaw for php routing) - done
1. scrapyd for demonizing scrapy spiders
	- using alternative solution for now (cronjob)
		- ref: [http://stackoverflow.com/a/17235906](http://stackoverflow.com/a/17235906)
1. prepare to push the servers/task scripts to live
1. setup linode server

----------------------------------------
#### 2015-10-21

##### Developments

1. soap (php) + restful (python) application - done for the infrastructure

----------------------------------------
#### 2015-10-20

##### Developments

1. must filter add-on items from amazon - done
1. patch to update all amazon pictures - done
1. notification workflow:
	1. receive solditem notification from ebay
	1. store information in db, and do follow-up action

1. if I use php soap server: - on progress
	- pro 
		- may use example - server should work fine...
	- cons 
		- need to maintain 2 different code bases
	- how to minimize the maintenance?
	- must make bridge system with php soap + python restful...
	- 
1. scrape watchcount.com
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com

----------------------------------------
#### 2015-10-19

##### Developments

1. soap server + handling ebay notifications - with *pysimplesoap* lib - not successful (no headers tag support)
1. scrape watchcount.com
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com


----------------------------------------
#### 2015-10-18

##### Developments

1. soap server + handling ebay notifications - failed to implement *spyne* lib 
1. scrape watchcount.com - cannot even started
	- with ebay_product_categories.category_id
	- search the title with google, then find same product from amazon.com

----------------------------------------
#### 2015-10-16

##### Bigger plans / todos

1. improve scraper, monitoring system
1. transfer to linode server
1. improve mapping amazon category/items to ebay category - improved with rake
1. soap server + handling ebay notifications
1. amazon ordring automation - casperjs

##### Developments

1. improve scraper and item monitering system
	- one scraper for just collect amazon asin - selenium / phantomjs
	- one scraper for go over all amazon detail screen - scrapy
1. need to find a way to mapping amazon category and ebay category - improved with RAKE (Rapid Automatic Keyword Extraction algorithm) - [https://pypi.python.org/pypi/python-rake/1.0.5](https://pypi.python.org/pypi/python-rake/1.0.5), [https://github.com/aneesha/RAKE](https://github.com/aneesha/RAKE)

----------------------------------------
#### 2015-10-15

##### Developments

1. setting up bakjin's application - improve application with site based
	- category/keyword based amazon item scraper - done
	- ebay application api with multiple users / tokens - done
	- setup linode servers - both application server, log server

----------------------------------------
#### 2015-10-14

##### ebay store marketing / accounting

1. list the vaccum on ebay - done
1. post a comment on redflagdeals.com - done
	- [http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963](http://forums.redflagdeals.com/costco-samsung-2-1-vacuum-199-97-449-99-bb-1751743/4/#post23860963)

##### Developments

1. setting up bakjin's application - improve application with site based
1. setup linode servers - both application server, log server


----------------------------------------
#### 2015-10-13

##### Developments

1. setting up bakjin's application - improve application with site based - on progress
1. setup linode servers - both application server, log server


----------------------------------------
#### 2015-10-10

##### ebay store marketing / accounting

1. proceed ebay item sold
	- questions: 
		- gyft.com cannot verify my mobile number. left a ticket - on process
		- amazon asks phone number of shipping information on checkout. may I give my phone number instead? - found buyer's phone number from **ebay.ca** management tool.

##### Developments

1. Auto-ordering - again...
	- soap with Spyne
	- navigate through amazon.com - must use casperjs, testing purpose. have to notify us as soon as possible


----------------------------------------
#### 2015-10-09

##### ebay store marketing

1. research more about sales tax

##### Developments

1. Auto-ordering
	- soap with Spyne
	- navigate through amazon.com


----------------------------------------
#### 2015-10-08

##### ebay store marketing

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

##### Developments

1. improve ebay api error handling - ebay\_trading\_api\_errors table - done

1. again... Auto-ordering, Auto-ordering, Auto-ordering!!!
	- soap is crazy... - understood pretty much
	- scrape and navigate amazon... - not yet


----------------------------------------
#### 2015-10-07

##### ebay store marketing

1. keep raising ebay feedbacks - 7 points so far

##### Developments

1. Auto-ordering, Auto-ordering, Auto-ordering!!!


----------------------------------------
#### 2015-10-06

##### ebay store marketing

1. keep raising ebay feedbacks - 4 points so far

##### Developments

1. update shipping policy template - done
	- add express shipping for $1.99 - extra money
	- make PO BOX available - but it will slow down your shipping - about 1-2 business days.

1. build automatic ordering system
	- check CasperJS
	- benchmark PriceYak


----------------------------------------
#### 2015-10-05

##### ebay Store / paypal business account

1. call paypal to verify bank account and credit card - not necessary

1. call ebay about my listings not searchable at ebay.com - done

1. switch linked paypal account at ebay.ca - not necessary

1. raising ebay feedbacks

1. go though ebay store marketing section

##### Developments

1. simplify amazon item monitoring system - merge amazon item price and amazon item status into a single process - need to test more

1. run the script on production


----------------------------------------
#### 2015-10-02

##### ebay Store

1. confirm Bank Account at paypal - done

2. subscribe to ebay Store Basic - done

3. work on ebay store settings
	- logo - done
	- search keywords - use google tool - done

##### Developments

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

