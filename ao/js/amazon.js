var casper = require('casper').create({
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        javascriptEnabled: true,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    },
    
    __takeScreenshots: true,
    __screenshotsFolder: '../../ss/',

});


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
            this.fillSelectors('form[name="signIn"]', {
                'input[name="email"]': 'xxxx',
                'input[name="password"]': 'xxxx',
            });

            this.echo('Logging In...');
            this.click('form[name="signIn"] input#signInSubmit');
        });
    });

    //
    // screen 4: Checkout
    // 
    this.then(function() {
        this.waitForSelector('#bottomsubtotals', function() {
            // screenshot taken
            ss();
        }, function() {
            // max timeout: default is 5 sec. increased to 20 sec here
            return 20000;
        });
    });

}).on("url.changed", function() {
    
    this.then(function() {
        this.echo('[url] ' + this.getCurrentUrl());
        this.echo('[page title] ' + this.getTitle());
    });

}).run();

