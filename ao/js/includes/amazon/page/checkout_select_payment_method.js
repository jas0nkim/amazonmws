var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.CheckoutSelectPaymentMethod = (function() {
    
    var instance;

    function init(casper) {

        // Singleton
        
        // Private methods and variables

        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;

        var _selector = {
            'form': 'form[name="continue"]',
            'use_gift_card': 'form[name="continue"] input[type="radio"][name="paymentMethod"][value="gcBalance"]',
            'submit': 'form[name="continue"] input[type="submit"]'
        };

        return {
            // Public methods and variables
            selectGiftCard: function() {
                _casper.waitForSelector(_selector.form, function() {
                    this.click(_selector.use_gift_card);
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
