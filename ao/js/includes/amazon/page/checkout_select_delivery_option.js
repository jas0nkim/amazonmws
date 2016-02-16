var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.CheckoutSelectDeliveryOption = (function() {
    
    var instance;

    function init(casper) {

        // Singleton
        
        // Private methods and variables

        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;

        var _selector = {
            'form': 'form#shippingOptionFormId',
            'free_two_day_shipping': 'form#shippingOptionFormId input[type="radio"][name="order_0_ShippingSpeed"][value="second"]',
            'submit': 'form#shippingOptionFormId input[type="submit"]'
        };

        return {
            // Public methods and variables
            selectFreeTwoDayShipping: function() {
                _casper.waitForSelector(_selector.form, function() {
                    this.click(_selector.free_two_day_shipping);
                    this.click(_selector.submit);
                });
            },
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
