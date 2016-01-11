var options = {
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        loadImages: true,
        loadPlugins: true,
        javascriptEnabled: true,
        webSecurityEnabled: false,
        userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4",
    },
    viewportSize: {
        width: 375,
        height: 667
    },
    // waitTimeout: 20000, // max timeout: default is 5 sec. increased to 20 sec here
    onError: function(self, m) {
        ss();
        // self.exit();
    },
    clientScripts: [
        "includes/jquery-1.11.3.min.js",
        "includes/URI.min.js"
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
    this.waitForSelector('#sc-mini-buy-box button', function() {
        this.click('#sc-mini-buy-box button');
        this.log('"Proceed to checkout" button clicked', 'info');
    });

}).then(function() {
    
    this.log('screen 3: Sign In', 'info');
    
    this.waitForSelector('form[name="signIn"]', function() {
        this.fill('form[name="signIn"]', {
            'email': input.amazon_user,
            'password': input.amazon_pass,
        }, true);
        this.log('Signing In...', 'info');
    });

}).then(function() {

    this.log('screen 4: Checkout', 'info');
    this.log('4.1. Select a shipping address', 'info');

    this.waitForSelector('#checkoutDisplayPage .address-book', function() {

        this.open('https://www.amazon.com/gp/buy/addressselect/handlers/new.html/ref=ox_shipaddress_new_address?id=UTF&fromAnywhere=1&isBilling=&showBackBar=1&skipHeader=1')
        this.log('move to Add a New Address link...', 'info');
    });

}).then(function() {

    this.log('4.2. add new address', 'info');

    this.waitForSelector('form.checkout-page-form', function() {
        
        this.fill('form.checkout-page-form', {
            'enterAddressFullName': input.buyer_name,
            'enterAddressAddressLine1': input.buyer_addr_1,
            'enterAddressAddressLine2': input.buyer_addr_2,
            'enterAddressCity': input.buyer_city,
            'enterAddressStateOrRegion': input.buyer_state,
            'enterAddressPostalCode': input.buyer_zip,
            'enterAddressPhoneNumber': input.buyer_phone,
            // 'input[name="enterAddressCountryCode"]': input.buyer_country_code,
        }, true);

        this.log('Submitting new shipping address information...', 'info');
    });

}).then(function() {

    this.log('4.3. choose your shipping options', 'info');

    this.waitForSelector('form#shippingOptionFormId', function() {
        
        this.evaluate(function() {
            $('form#shippingOptionFormId input[type=radio][value=second]').prop('checked', true);
            $('form#shippingOptionFormId').submit();
            return true;
        });

        this.log('Submitting free two-day shipping option...', 'info');
    });

}).then(function() {

    this.log('4.4. select a payment method', 'info');

    this.waitForSelector('#select-payments-view form[name=continue]', function() {
        
        this.evaluate(function() {
            $('#select-payments-view form[name=continue] input[type=radio][value=gcBalance]').prop('checked', true);
            $('#select-payments-view form[name=continue]').submit();
            return true;
        });

        this.log('Submitting free two-day shipping option...', 'info');
    });

}).then(function() {

    this.log('4.5.1 Order Summary', 'info');

    this.waitForSelector('#subtotals-marketplace-table table tbody', function() {
        var order_summary = this.evaluate(function() {
            var summary = []
            var label, price
            $('#subtotals-marketplace-table table tbody tr').each(function() {
                label = $.trim($(this).find('td:nth-of-type(1)').text());
                price = $.trim($(this).find('td:nth-of-type(2)').text());
                
                if (label.indexOf("Items:") >= 0) {

                    summary.push({ 'item_price': price });

                } else if (label.indexOf("Shipping") >= 0) {

                    summary.push({ 'shipping_and_handling': price });

                } else if (label.indexOf("Estimated tax") >= 0) {

                    summary.push({ 'tax': price });

                } else if (label.indexOf("Total:") >= 0) {

                    summary.push({ 'total': price });
                }
            });
            return summary;
        });

        this.echo(JSON.stringify(order_summary));
    });

}).then(function() {

    this.log('4.5.2 Place your order', 'info');

    this.waitForSelector('form#spc-form input[type=submit]:nth-of-type(1)', function() {

        this.click('form#spc-form input[type=submit]:nth-of-type(1)');

        this.log("Placing your order...", 'warning');
    });

}).then(function() {

    this.log('5. Thank you, your order has been placed.', 'info');

    this.waitForSelector('#thank-you-box-wrapper a', function() {

        var order_number = this.evaluate(function() {
            var o_number = '';
            var order_detail_link = $('#thank-you-box-wrapper a').attr('href');
            var query = new URI(order_detail_link).query(true);
            if ('oid' in query) {
                o_number = query['oid'];
            }
            return o_number;
        });

        this.echo(order_number);
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

}).on('remote.message', function(msg) {
    
    this.log('remote message caught: ' + msg, 'warning');

}).run();
