var page_shopping_cart = require('../page/shopping_cart');

var Amazon = Amazon || {};
Amazon.Workflow = Amazon.Workflow || {};

Amazon.Workflow.Checkout = (function() {
    
    var instance;

    function init(casper) {

        // Singleton
        
        // Private methods and variables

        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;

        return {
            // Public methods and variables
            checkout: function() {
                _casper.thenOpen(_url);
            },

            // 1. must have only one(1) item in cart
            // 2. must have only one(1) quantity for the item
            validateCart: function() {
                return this.validateItemCount() && this.validateItemQuantity();
            },

            validateItemCount: function() {
                var items_count = _casper.evaluate(function() {
                    return $(_selector.items).length;
                });

                return items_count == 1;
            },

            validateItemQuantity: function() {
                var item_quantity = _casper.evaluate(function() {
                    return parseInt($.trim($(_selector.items).first().find(_selector.item_quantity).text()));
                });

                return item_quantity == 1;
            },

            proceedToCheckout: function() {
                _casper.waitForSelector(_selector.checkout, function() {
                    this.click(_selector.checkout);
                });
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