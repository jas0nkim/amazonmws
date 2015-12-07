var options = {
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        loadImages: true,
        loadPlugins: true,
        javascriptEnabled: true,
        webSecurityEnabled: false,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    },
    waitTimeout: 20000, // max timeout: default is 5 sec. increased to 20 sec here
    onError: function(self, m) {
        ss();
        // self.exit();
    },
    clientScripts: [
        "includes/jquery-1.11.3.min.js"
    ],
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


casper.start('http://www.amazon.com/dp/' + input.asin).then(function() {

    this.log('screen 1: Amazon Item', 'info');
    // click 'Add to Cart' button
    this.waitForSelector('#add-to-cart-button', function() {
        this.click('#add-to-cart-button');
        this.log('"Add to Cart" button clicked', 'info');
    });

}).then(function() {

    this.log('screen 2: Shopping Cart', 'info');
    // click 'Proceed to checkout' button
    this.waitForSelector('#hlb-ptc-btn-native', function() {
        this.click('#hlb-ptc-btn-native');
        this.log('"Proceed to checkout" button clicked', 'info');
    });

}).then(function() {
    
    this.log('screen 3: Sign In', 'info');
    
    this.waitForSelector('form[name="signIn"]', function() {
        this.fill('form[name="signIn"]', {
            'email': input.amazon_user,
            'password': input.amazon_pass,
        }, true);
        this.log('Logging In...', 'info');
    });

}).then(function() {

    this.log('screen 4: Checkout', 'info');
    this.log('4.1. Choose a shipping address', 'info');

    this.waitForSelector('#add-address-popover-link', function() {
        this.click('#add-address-popover-link');
    });

// }).then(function() {

//     this.log('4.2. new address modal shown', 'info');
//     ss();

//     this.waitForVisible('div.a-modal-scroller.a-declarative', function() {
//         this.log("new address modal shown", 'warning');
//         ss();
//     });

}).then(function() {

    this.log('4.3. fill and submit new address form', 'info');

    this.waitForSelector('form#domestic-address-popover-form', function() {
        
        this.log('Filling shipping address information...', 'info');
        
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
    });

}).then(function() {

    this.log('4.4. close modal', 'info');

    var self = this;
    this.evaluate(function() {
        // click 'Use this address' button to submit
        var $button = $('form#domestic-address-popover-form').closest('div.a-popover.a-popover-modal').find('div.a-popover-footer span.a-button.a-button-primary');
        self.log($button.html(), 'warning');
        $button.click();

        return true;
    });

// }).then(function() {

//     this.log('4.4. close modal', 'info');

//     this.waitForSelector('div.a-popover.a-popover-modal div.a-popover-footer > div > span:nth-of-type(1) > span.a-button', function() {

//         var test = this.getHTML('div.a-popover.a-popover-modal div.a-popover-footer > div > span:nth-of-type(1) > span.a-button');                    
//         this.log(test, 'warning');

//         this.click('div.a-popover.a-popover-modal div.a-popover-footer > div > span:nth-of-type(1) > span.a-button');
//     });

}).then(function() {

    this.log('4.5. Shipping information entered, and displayed', 'info');

    this.waitForSelector('div.displayAddressDiv', function() {
        this.log("new address entered and displayed", 'warning');
    });

    // this.waitFor(function check() {
    //     return this.evaluate(function() {

    //         return document.querySelectorAll('ul.your-list li').length > 2;
    //     });
    // });
    // this.evaluate(function() {
    //     // click 'Use this address' button to submit
    //     var $button = $('form#domestic-address-popover-form').closest('div.a-popover.a-popover-modal').find('div.a-popover-footer span.a-button.a-button-primary');
    //     self.log($button.html(), 'warning');
    //     $button.click();

    //     return true;
    // });

}).then(function() {

    this.log('4.6. Choose a payment method', 'info');

    this.waitForSelector('span#useThisPaymentMethodButtonId', function() {
        this.log('Choosing amazon gift card as a payment methods...', 'info');
        this.click('span#useThisPaymentMethodButtonId');
    });

}).then(function() {

    this.waitWhileSelector('div#existing-payment-methods', function() {
        this.log("payment method finished", 'warning');
    });

}).then(function() {

    this.log('4.7. Review items and shipping. Click two-day shipping', 'info');

    this.waitForSelector('spc-orders div.shipping-speed.ship-option input[type="radio"][value="second"]', function() {

        // select FREE Two-Day Shipping
        this.click('#spc-orders div.shipping-speed.ship-option input[type="radio"][value="second"]');
    });

}).thenBypassUnless(function() {

    this.log('4.7.1 bypass if gift option already applied', 'info');

    return this.exists('#spc-orders span.gift-popover-link a');

}, 4).then(function() {

    this.log('4.7.2 open gift option', 'info');

    this.click('#spc-orders span.gift-popover-link');

}).then(function() {

    this.log('4.7.3 remove any messages', 'info');

    this.waitForSelector('.popover-gift.checkout', function() {
        this.evaluate(function(term) {
            document.querySelector('textarea[name="gift-message-text"]').setAttribute('value', term);
        }, ''); // set blank
    });

}).then(function() {

    this.log('4.7.3 remove any messages', 'info');

    this.click('li.popover-gift-bottom > span > span.a-button.set-gift-options-button');

}).then(function() {

    this.log('4.7.4 gift option modal disappeared', 'info');

    this.waitWhileVisible('div.a-modal-scroller.a-declarative', function() {
        this.log("gift option modal disappeared", 'warning');
    });

}).then(function() {

    this.log('4.8. Place your order', 'info');

    this.waitForSelector('#submitOrderButtonId', function() {
        this.click('#submitOrderButtonId');
    });

}).then(function() {

    this.log('5. Thank you, your order has been placed.', 'info');

    this.waitForText('your order has been placed', function() {
        var order_number = this.getElementInfo('h5 > span.a-text-bold').text;

        this.log(order_number, 'info');
    });

}).on("url.changed", function() {
    
    this.then(function() {
        this.log('[url] ' + this.getCurrentUrl(), 'info');
        this.log('[page title] ' + this.getTitle(), 'info');
    });

}).on("error", function(msg, backtrace) {
    
    ss();

}).on("resource.error", function(resourceError) {

    this.echo(JSON.stringify(resourceError));

}).run();
