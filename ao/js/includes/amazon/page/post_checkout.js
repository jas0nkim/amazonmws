var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.PostCheckout = (function() {
    
    var instance;

    function init(casper) {

        // Singleton
        
        // Private methods and variables

        var _casper = casper;

        var _order_number = function() {
            return this.evaluate(function() {
                var o_number = '';
                var order_detail_link = $('#thank-you-box-wrapper a').attr('href');
                var query = new URI(order_detail_link).query(true);
                if ('oid' in query) {
                    o_number = query['oid'];
                }
                return { 'order_number': o_number };
            });
        };

        var _selector = {
            'form': 'form#spc-form',
            'place_order': 'form#spc-form input[type="submit"]'
        };

        return {
            // Public methods and variables
            getOrderNumber: function() {
                var ret = null;
                _casper.waitForSelector('#thank-you-box-wrapper a', function() {
                    ret = _order_number;
                });
                return ret;
            }
        };
    }

    return {
        
        // Get the Singleton instance if one exists or create one if it doesn't
        getInstance: function(casper) {
            if (!instance) {
                instance = init(casper);
            }

            return instance;
        }
    }
    
})();
