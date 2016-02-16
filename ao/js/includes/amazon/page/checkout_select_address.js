var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.CheckoutSelectAddress = (function() {
    
    var instance;

    function init(casper, buyer_name, buyer_addr_1, buyer_addr_2, buyer_city, buyer_state, buyer_zip, buyer_phone) {

        // Singleton
        
        // Private methods and variables

        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;
        var _buyer_name = buyer_name;
        var _buyer_addr_1 = buyer_addr_1;
        var _buyer_addr_2 = buyer_addr_2;
        var _buyer_city = buyer_city;
        var _buyer_state = buyer_state;
        var _buyer_zip = buyer_zip;
        var _buyer_phone = buyer_phone;

        var _url_new_address = 'https://www.amazon.com/gp/buy/addressselect/handlers/new.html/ref=ox_shipaddress_new_address?id=UTF&fromAnywhere=1&isBilling=&showBackBar=1&skipHeader=1';

        var _selector = {
            // new address form
            'new_address_form': 'form.checkout-page-form',
            'full_name_field': 'form.checkout-page-form input[name="enterAddressFullName"]',
            'address_1_field': 'form.checkout-page-form input[name="enterAddressAddressLine1"]',
            'address_2_field': 'form.checkout-page-form input[name="enterAddressAddressLine2"]',
            'city_field': 'form.checkout-page-form input[name="enterAddressCity"]',
            'state_field': 'form.checkout-page-form input[name="enterAddressStateOrRegion"]',
            'postal_code_field': 'form.checkout-page-form input[name="enterAddressPostalCode"]',
            'phone_number_field': 'form.checkout-page-form input[name="enterAddressPhoneNumber"]',
            'new_address_submit': 'form.checkout-page-form button[type="submit"]',

            // verify address form
            'verify_address_form': 'form',
            'original_address': 'form input[type="radio"][name="addr"][value="addr_0"]',
            'suggested_address': 'form input[type="radio"][name="addr"][value="addr_1"]',
            'verify_address_submit': 'form button[type="submit"]'
        };

        return {
            // Public methods and variables
            goToAddNewAddress: function() {
                _casper.thenOpen(_url_new_address);
            },

            addNewAddress: function() {
                _casper.waitForSelector(_selector.new_address_form, function() {
                    this.sendKeys(_selector.full_name_field, _buyer_name);
                    this.sendKeys(_selector.address_1_field, _buyer_addr_1);
                    this.sendKeys(_selector.address_2_field, _buyer_addr_2);
                    this.sendKeys(_selector.city_field, _buyer_city);
                    this.sendKeys(_selector.state_field, _buyer_state);
                    this.sendKeys(_selector.postal_code_field, _buyer_zip);
                    this.sendKeys(_selector.phone_number_field, _buyer_phone);
                    this.click(_selector.new_address_submit);
                });
            },

            verifyAddress: function() {
                _casper.waitFor(function check() {
                    return this.evaluate(function() {
                        return $.trim($('h1').text()).toLowerCase() == 'vefiry your shipping address';
                    });
                }, function then() {
                    this.click(_selector.original_address);
                    this.click(_selector.verify_address_submit);
                }, function onTimeout() {
                    return false
                }, 1000
            }
        };
    }

    return {
        
        // Get the Singleton instance if one exists or create one if it doesn't
        getInstance: function(casper, buyer_name, buyer_addr_1, buyer_addr_2, buyer_city, buyer_state, buyer_zip, buyer_phone) {
            if (!instance) {
                instance = init(casper, buyer_name, buyer_addr_1, buyer_addr_2, buyer_city, buyer_state, buyer_zip, buyer_phone);
            }

            return instance;
        }
    }
    
})();
