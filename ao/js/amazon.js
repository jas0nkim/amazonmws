var options = {
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        javascriptEnabled: true,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    },
    
    __takeScreenshots: true,
    __screenshotsFolder: '../../ss/',    
}

var casper = require('casper').create(options);

var input = {
    // amazon auth
    amazon_user: casper.cli.get("amazon_user"),
    amazon_pass: casper.cli.get("amazon_pass"),
    
    // buyer shipping info
    buyer_name: casper.cli.get("buyer_name"),
    buyer_shipping_address_1: casper.cli.get("buyer_shipping_address_1"),
    buyer_shipping_address_2: casper.cli.get("buyer_shipping_address_2"),
    buyer_shipping_city: casper.cli.get("buyer_shipping_city"),
    buyer_shipping_state: casper.cli.get("buyer_shipping_state"),
    buyer_shipping_zip: casper.cli.get("buyer_shipping_zip"),
    buyer_shipping_country: casper.cli.get("buyer_shipping_country"),
    buyer_shipping_phone: casper.cli.get("buyer_shipping_phone"),
};

// function getLinks() {
//     var links = document.querySelectorAll('h3.r a');
//     return Array.prototype.map.call(links, function(e) {
//         return e.getAttribute('href');
//     });
// }

casper.start('http://www.amazon.com/dp/B00KKV86MI', function() {
    var fail, ss;
    var _casper = this;

    fail = function(message) {
        var timestamp;
        _casper.test.fail(message);
        if (_casper.options.__takeScreenshots) {
            timestamp = new Date().getTime();
            return _casper.capture(_casper.options.__screenshotsFolder + ['casperjs_fail', timestamp, 'png'].join('.'));
        }
    };

    ss = function() {
        if (_casper.options.__takeScreenshots) {
            timestamp = new Date().getTime();
            return _casper.capture(_casper.options.__screenshotsFolder + ['casperjs_fail', timestamp, 'png'].join('.'));
        }        
    };


    //
    // screen 1: amazon item
    // 
    this.then(function() {
        // click 'Add to Cart' button
        this.waitForSelector('#add-to-cart-button', function() {
            this.click('#add-to-cart-button');
            this.echo('"Add to Cart" button clicked');
        });
    });

    //
    // screen 2: Shopping Cart
    // 
    this.then(function() {
        // click 'Proceed to checkout' button
        this.waitForSelector('#hlb-ptc-btn-native', function() {
            this.echo('hlb-ptc-btn-native selector found');
            this.click('#hlb-ptc-btn-native');
            this.echo('"Proceed to checkout" button clicked');
        });
    });

    //
    // screen 3: Sign In
    // 
    this.then(function() {
        this.waitForSelector('form[name="signIn"]', function() {
            this.fill('form[name="signIn"]', {
                'email': input.amazon_user,
                'password': input.amazon_pass,
            }, true);

            this.echo('Logging In...');
        });
    });

    //
    // screen 4: Checkout
    // 

    // 4.1. Choose a shipping address
    this.then(function() {
        this.waitForSelector('#add-address-popover-link', function() {
            // screenshot taken
            // ss();

            this.thenClick('#add-address-popover-link', function() {
                this.waitForSelector('form#domestic-address-popover-form', function() {
                    this.fill('form#domestic-address-popover-form', {
                        'enterAddressFullName': input.buyer_name,
                        'enterAddressAddressLine1': input.buyer_shipping_address_1,
                        'enterAddressAddressLine2': input.buyer_shipping_address_2,
                        'enterAddressCity': input.buyer_shipping_city,
                        'enterAddressStateOrRegion': input.buyer_shipping_state,
                        'enterAddressPostalCode': input.buyer_shipping_zip,
                        // 'input[name="enterAddressCountryCode"]': input.buyer_shipping_country,
                        'enterAddressPhoneNumber': input.buyer_shipping_phone,
                    }, false);

                    this.echo('Filling shipping address information...');
                    this.click('.a-popover-footer input[type="submit"]');
                });
            });
        }, function() {
            // max timeout: default is 5 sec. increased to 10 sec here
            return 10000;
        });

    });

    // 4.2. Choose a payment method
    this.then(function() {
        this.waitForSelector('#existing-payment-methods', function() {

            this.click('#existing-balance input#pm_gc_radio');

            this.echo('Filling shipping address information...');
            this.click('#useThisPaymentMethodButtonId input#continue-top');
        });
    });

    // 4.3. Review items and shipping
    this.then(function() {
        this.waitForSelector('#spc-orders', function() {

            this.thenBypassUnless(function() {
                return this.exists('#spc-orders span.gift-popover-link a')
            }, 1)

            // gift card option
            this.thenClick('#spc-orders span.gift-popover-link a', function() {
                this.waitForSelector('.popover-gift.checkout', function() {
                    this.evaluate(function(term) {
                        document.querySelector('textarea[name="gift-message-text"]').setAttribute('value', term);
                    }, ''); // set blank

                    this.then(function() {
                        this.click('.set-gift-options-button input[type="submit"]');
                    });
                });
            });
        });
    });

    // 4.4. Place your order
    this.then(function() {
        this.click('input[name="placeYourOrder1"]');
    });

    // 5. Thank you, your order has been placed.
    this.then(function() {
        this.waitForText('your order has been placed', function() {
            var order_number = this.getElementInfo('h5 > span.a-text-bold').text;
            this.echo(order_number)
        }, 10000);
    },);


}).on("url.changed", function() {
    
    this.then(function() {
        this.echo('[url] ' + this.getCurrentUrl());
        this.echo('[page title] ' + this.getTitle());
    });

}).run();

