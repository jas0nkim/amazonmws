var Amazon = Amazon || {};
Amazon.Page = Amazon.Page || {};

Amazon.Page.Login = (function() {
    
    var instance;

    function init(casper, username, password) {

        // Singleton
        
        // Private methods and variables

        // function privateMethod() {

        //     console.log( "I am private" );
        // }

        var _casper = casper;
        var _username = username;
        var _password = password;

        var _url = 'https://www.amazon.com/gp/sign-in.html';

        var _selector = {
            'signin_form': 'form[name="signIn"]',
            'email_field': 'form[name="signIn"] input[name="email"]',
            'password_field': 'form[name="signIn"] input[name="password"]',
            'submit': 'form[name="signIn"] input[type="submit"]'
        };

        return {
            // Public methods and variables
            goTo: function() {
                _casper.thenOpen(_url);
            },

            login: function() {
                _casper.waitForSelector(_selector.signin_form, function() {
                    this.sendKeys(_selector.email_field, _username);
                    this.sendKeys(_selector.password_field, _password);
                    this.click(_selector.submit);
                });
            }
        };
    }

    return {
        
        // Get the Singleton instance if one exists or create one if it doesn't
        getInstance: function(casper, username, password) {
            if (!instance) {
                instance = init(casper, username, password);
            }

            return instance;
        }
    }
    
})();
