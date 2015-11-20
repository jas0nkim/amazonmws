var options = {
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        javascriptEnabled: true,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    },
    waitTimeout: 20000, // max timeout: default is 5 sec. increased to 20 sec here
    onError: function(self, m) {
        ss();
        // self.exit();
    },
    __takeScreenshots: true,
    __screenshotsFolder: '../../ss/',    
}

var casper = require('casper').create(options);

var input = {
    // amazon item
    asin: casper.cli.get("asin"),

    // amazon auth
    amazon_user: casper.cli.get("amazon_user"),
    amazon_pass: casper.cli.get("amazon_pass"),
    
    // buyer shipping info
    buyer_name: casper.cli.get("buyer_name"),
    buyer_addr_1: casper.cli.get("buyer_addr_1"),
    buyer_addr_2: casper.cli.get("buyer_addr_2"),
    buyer_city: casper.cli.get("buyer_city"),
    buyer_state: casper.cli.get("buyer_state"),
    buyer_zip: casper.cli.get("buyer_zip"),
    buyer_country_code: casper.cli.get("buyer_country_code"),
    buyer_phone: casper.cli.get("buyer_phone"),
};

var fail, ss;

fail = function(message) {
    var timestamp;
    casper.test.fail(message);
    if (casper.options.__takeScreenshots) {
        timestamp = new Date().getTime();
        return casper.capture(casper.options.__screenshotsFolder + ['casperjs_fail', timestamp, 'png'].join('.'));
    }
};

ss = function() {
    if (casper.options.__takeScreenshots) {
        timestamp = new Date().getTime();
        return casper.capture(casper.options.__screenshotsFolder + ['casperjs_fail', timestamp, 'png'].join('.'));
    }        
};


casper.start('http://www.amazon.com/dp/' + input.asin, function() {

    //
    // screen 1: Amazon Item
    // 
    this.then(function() {
        
        this.log('screen 1: Amazon Item', 'info');

        // click 'Add to Cart' button
        this.waitForSelector('#add-to-cart-button', function() {
            this.click('#add-to-cart-button');
            this.log('"Add to Cart" button clicked', 'info');
        });
    });

    //
    // screen 2: Shopping Cart
    // 
    this.then(function() {

        this.log('screen 2: Shopping Cart', 'info');

        // click 'Proceed to checkout' button
        this.waitForSelector('#hlb-ptc-btn-native', function() {
            this.click('#hlb-ptc-btn-native');
            this.log('"Proceed to checkout" button clicked', 'info');
        });
    });

    //
    // screen 3: Sign In
    // 
    this.then(function() {

        this.log('screen 3: Sign In', 'info');

        this.waitForSelector('form[name="signIn"]', function() {
            this.fill('form[name="signIn"]', {
                'email': input.amazon_user,
                'password': input.amazon_pass,
            }, true);

            this.log('Logging In...', 'info');
        });
    });

    //
    // screen 4: Checkout
    // 

    // 4.1. Choose a shipping address
    this.then(function() {

        this.log('screen 4: Checkout', 'info');
        this.log('4.1. Choose a shipping address', 'info');

        this.waitForSelector('#add-address-popover-link', function() {
            this.click('#add-address-popover-link');

            this.then(function() {
                this.waitForSelector('form#domestic-address-popover-form', function() {
                    this.fill('form#domestic-address-popover-form', {
                        'enterAddressFullName': input.buyer_name,
                        'enterAddressAddressLine1': input.buyer_addr_1,
                        'enterAddressAddressLine2': input.buyer_addr_2,
                        'enterAddressCity': input.buyer_city,
                        'enterAddressStateOrRegion': input.buyer_state,
                        'enterAddressPostalCode': input.buyer_zip,
                        // 'input[name="enterAddressCountryCode"]': input.buyer_country_code,
                        'enterAddressPhoneNumber': input.buyer_phone,
                    }, false);

                    this.log('Filling shipping address information...', 'info');
                    this.click('div.a-popover-footer > div > span:nth-child(1) > span.a-button.a-button-primary');
                });
            });
        });
    });

    // 4.2. Choose a payment method
    this.then(function() {

        this.log('4.2. Choose a payment method', 'info');

        this.waitForSelector('#existing-payment-methods', function() {

            this.click('#existing-balance input#pm_gc_radio');

            this.log('Choosing amazon gift card as a payment methods...', 'info');
            this.click('#useThisPaymentMethodButtonId');
        });
    });

    // 4.3. Review items and shipping
    this.then(function() {

        this.log('4.3. Review items and shipping', 'info');

        this.waitForSelector('#spc-orders', function() {

            // select FREE Two-Day Shipping
            this.click('#spc-orders div.shipping-speed.ship-option input[type="radio"][value="second"]');

            this.thenBypassUnless(function() {
                return this.exists('#spc-orders span.gift-popover-link a')
            }, 1)

            // gift card option
            this.thenClick('#spc-orders span.gift-popover-link', function() {
                this.waitForSelector('.popover-gift.checkout', function() {
                    this.evaluate(function(term) {
                        document.querySelector('textarea[name="gift-message-text"]').setAttribute('value', term);
                    }, ''); // set blank

                    this.then(function() {
                        this.click('li.popover-gift-bottom > span > span.a-button.set-gift-options-button');
                    });
                });
            });
        });
    });

    // 4.4. Place your order
    this.then(function() {

        this.log('4.4. Place your order', 'info');

        this.waitForSelector('#submitOrderButtonId', function() {
            this.click('#submitOrderButtonId');
        });
    });

    // 5. Thank you, your order has been placed.
    this.then(function() {

        this.log('5. Thank you, your order has been placed.', 'info');

        this.waitForText('your order has been placed', function() {
            var order_number = this.getElementInfo('h5 > span.a-text-bold').text;

            this.log(order_number, 'info');
        });
    });

}).on("url.changed", function() {
    
    this.then(function() {
        this.log('[url] ' + this.getCurrentUrl(), 'info');
        this.log('[page title] ' + this.getTitle(), 'info');
    });

}).on("error", function(msg, backtrace) {
    
    ss();
    this.log(msg, 'error');
    this.log(backtrace, 'error');

}).run();
