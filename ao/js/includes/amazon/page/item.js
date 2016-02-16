var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.Item = (function() {
    
    var instance;

    function init(casper, asin) {
        // Singleton

        // Private methods and variables
        
        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;
        var _asin = asin;

        var _url_prefix = 'https://www.amazon.com/dp/';

        var _selector = {
            'add_to_cart': '#add-to-cart-button'
        };

        return {
            // Public methods and variables
            goTo: function() {
                _casper.thenOpen(_url_prefix + _asin);
            },

            addToCart: function() {
                _casper.thenClick(_selector.add_to_cart);
            }
        };
    }

    return {
        
        // Get the Singleton instance if one exists or create one if it doesn't
        getInstance: function(casper, asin) {
            if (!instance) {
                instance = init(casper, asin);
            }

            return instance;
        }
    }

})();
