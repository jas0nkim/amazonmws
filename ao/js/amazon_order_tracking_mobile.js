var options = {
    verbose: true,
    logLevel: "error",
    pageSettings: {
        loadImages: true,
        loadPlugins: true,
        javascriptEnabled: true,
        webSecurityEnabled: false,
        // userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4",
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
    clientScripts: [],
    __takeScreenshots: true,
    __screenshotsFolder: '',
}

var PREFIX_OUTPUT = '<<<';
var POSTFIX_OUTPUT = '>>>';

var casper = require('casper').create(options);

var input = {
    // auth_key
    auth_key: casper.cli.get("auth_key"),

    // app root path: i.e. /applications/amazonmws - without tailing slash (/)
    root_path: casper.cli.get("root_path"),

    // user agent
    user_agent: casper.cli.get("user_agent"),

    // amazon order id
    order_id: casper.cli.get("order_id"),

    // amazon auth
    amazon_user: casper.cli.get("amazon_user"),
    amazon_pass: casper.cli.get("amazon_pass"),    
};

casper.userAgent(input.user_agent);

casper.options.clientScripts.push(input.root_path + '/ao/js/includes/jquery-1.11.3.min.js');
casper.options.clientScripts.push(input.root_path + '/ao/js/includes/URI.min.js');
casper.options.__screenshotsFolder = input.root_path + '/ss/';

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

var crawlera_fatch_api = 'http://' + input.auth_key + ':@proxy.crawlera.com:8010/fetch?url=';

var start_url = encodeURIComponent('https://www.amazon.com/gp/aw/ya/?ie=UTF8&ac=od&ii=&noi=&of=&oi=&oid=' + input.order_id);

// order detail screen link
casper.start(crawlera_fatch_api + start_url).then(function() {

    this.log('screen 1: Sign In', 'info');
    
    this.waitForSelector('form[name="signIn"]', function() {
        this.fill('form[name="signIn"]', {
            'email': input.amazon_user,
            'password': input.amazon_pass,
        }, true);
        this.log('Signing In...', 'info');
    });

}).then(function() {

    this.log('screen 2: View Order Details', 'info');
    // click 'Add to Cart' button
    this.waitForSelector('.a-box-group:nth-of-type(1)', function() {
        var tracking_link = this.evaluate(function() {
            var t_link = null
            $('.a-box-group:nth-of-type(1) a').each(function() {
                var link = $(this).attr('href');
                if (link.indexOf('ship-track') > -1) {
                    t_link = encodeURIComponent('https://www.amazon.com' + link);
                }
            });
            return t_link;
        });

        if (tracking_link != null) {
            this.open(crawlera_fatch_api + tracking_link)
            this.log('move to tracking link...', 'info');
        }
    });

}).then(function() {

    this.log('screen 3: Tracking Information', 'info');
    // click 'Proceed to checkout' button
    this.waitForSelector('.a-container:nth-of-type(1)', function() {
        var tracking_info = this.evaluate(function() {
            var info = {}

            var carrier_label = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) span:nth-of-type(1)').text());
            var tracking_label = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) span:nth-of-type(2)').text());
            var carrier_value = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) p:nth-of-type(1)').text());
            var tracking_value = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) p:nth-of-type(2)').text());

            if (carrier_label == 'Carrier' && tracking_label == 'Tracking #') {
                info['carrier'] = carrier_value;
                info['tracking_number'] = tracking_value;
            }

            return { 'tracking_info': info };
        });

        this.echo(PREFIX_OUTPUT + JSON.stringify(tracking_info) + POSTFIX_OUTPUT);
    });

}).on("url.changed", function() {
    
    this.then(function() {
        this.log('[url] ' + this.getCurrentUrl(), 'info');
        this.log('[page title] ' + this.getTitle(), 'info');
    });

}).on("error", function(msg, backtrace) {
    
    ss();

}).on("resource.error", function(resourceError) {

    this.log(JSON.stringify(resourceError), 'error');

}).on('remote.message', function(msg) {
    
    this.log('remote message caught: ' + msg, 'warning');

}).run();
