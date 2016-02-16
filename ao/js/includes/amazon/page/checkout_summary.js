var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.CheckoutSummary = (function() {
    
    var instance;

    function init(casper) {

        // Singleton
        
        // Private methods and variables

        var _casper = casper;

        var _price_info = function () {
            return this.evaluate(function() {
                var summary = {};
                var label, price;
                $('#subtotals-marketplace-table table tbody tr').each(function() {
                    label = $.trim($(this).find('td:nth-of-type(1)').text());
                    price = $.trim($(this).find('td:nth-of-type(2)').text());
                    
                    if (label.indexOf("Items:") >= 0) {

                        summary['item_price'] = price;

                    } else if (label.indexOf("Shipping") >= 0) {

                        summary['shipping_and_handling'] = price;

                    } else if (label.indexOf("Estimated tax") >= 0) {

                        summary['tax'] = price;

                    } else if (label.indexOf("Total:") >= 0) {

                        summary['total'] = price;
                    }
                });
                return { 'order_summary': summary };
            });
        };

        var _selector = {
            'form': 'form#spc-form',
            'place_order': 'form#spc-form input[type="submit"]'
        };

        return {
            // Public methods and variables
            getPriceInfo: function() {
                return _price_info;
            },

            verifyCost: function() {
                return true;
            },

            verifyShippingAddress: function() {
                return true;
            },

            verifyPaymentMethod: function() {
                return true;
            },

            placeOrder: function() {
                if (this.verifyCost() && this.verifyShippingAddress() && this.verifyPaymentMethod()) {
                    _casper.click(_selector.place_order);
                }
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
