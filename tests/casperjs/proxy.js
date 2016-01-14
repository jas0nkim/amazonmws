var options = {
    verbose: true,
    logLevel: "debug",
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

casper.userAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4");

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

casper.start('http://www.itsitonline.com').on("url.changed", function() {
    
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
