function validateCurrentPage(currentUrl) {
    var urlPattern_amazonItemPage_mobile = /^https?:\/\/www.amazon.com\/gp\/aw\/d\/([A-Z0-9]{10})(.*$)?/;
    var urlPattern_amazonItemPage_desktop = /^https?:\/\/www.amazon.com\/([^\/]+\/[^\/]+|dp)\/([A-Z0-9]{10})(\/.*$)?/;
    var urlPattern_amazonShoppingCartPage = /^https:\/\/www.amazon.com\/gp\/aw\/c(.*$)?/;
    var urlPattern_amazonCheckoutAddressSelectPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutAddNewAddressPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/new\.html(.*$)?/;
    var urlPattern_amazonCheckoutChooseShippingPage = /^https:\/\/www.amazon.com\/gp\/buy\/shipoptionselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutChoosePaymentMethodPage = /^https:\/\/www.amazon.com\/gp\/buy\/payselect\/handlers\/display\.html(.*$)?/;

    if (currentUrl.match(urlPattern_amazonItemPage_mobile)) {
        return { validate: true, type: 'amazon_item', env: 'mobile' };
    } else if (currentUrl.match(urlPattern_amazonItemPage_desktop)) {
        return { validate: true, type: 'amazon_item', env: 'desktop' };
    } else if (currentUrl.match(urlPattern_amazonShoppingCartPage)) {
        return { validate: true, type: 'amazon_shopping_cart' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutAddressSelectPage)) {
        return { validate: true, type: 'amazon_checkout_address_select' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutAddNewAddressPage)) {
        return { validate: true, type: 'amazon_checkout_add_new_address' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutChooseShippingPage)) {
        return { validate: true, type: 'amazon_checkout_choose_shipping' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutChoosePaymentMethodPage)) {
        return { validate: true, type: 'amazon_checkout_choose_payment_method' };
    }
    return false
}

function addItemToCart() {
    $('#add-to-cart-button').click();
}

function proceedToCheckout() {
    $('#sc-mini-buy-box button').click();
}

function goToAddNewAddress() {
    var url_amazonAddNewShippingAddress = 'https://www.amazon.com/gp/buy/addressselect/handlers/new.html/ref=ox_shipaddress_new_address?id=UTF&fromAnywhere=1&isBilling=&showBackBar=1&skipHeader=1';
    
    window.open(url_amazonAddNewShippingAddress, '_self');
}

function addNewAddress(order) {
    var $newAddressForm = $('form.checkout-page-form');
    $newAddressForm.find('input[name="enterAddressFullName"]').val(order.buyer_shipping_name);
    $newAddressForm.find('input[name="enterAddressAddressLine1"]').val(order.buyer_shipping_street1);
    $newAddressForm.find('input[name="enterAddressAddressLine2"]').val(order.buyer_shipping_street2);
    $newAddressForm.find('input[name="enterAddressCity"]').val(order.buyer_shipping_city_name);
    $newAddressForm.find('input[name="enterAddressStateOrRegion"]').val(order.buyer_shipping_state_or_province);
    $newAddressForm.find('input[name="enterAddressPostalCode"]').val(order.buyer_shipping_postal_code);
    $newAddressForm.find('input[name="enterAddressPhoneNumber"]').val(order.buyer_shipping_phone);
    $newAddressForm.find('input[type="submit"][name="shipToThisAddress"]').click();
}

function chooseFreeTwoDayShipping() {
    var $chooseShippingForm = $('form#shippingOptionFormId');
    $chooseShippingForm.find('input[type="radio"][name="order_0_ShippingSpeed"][value="second"]').click();
    $chooseShippingForm.find('input[type="submit"]').click();
}

// function chooseFreeOneDayShipping() {}

function chooseCreditCardPayment() {
    var $choosePaymentMethodForm = $('#select-payments-view form[data-action="submit-payment-form"]');
    var $continuePaymentMethodButtons = $choosePaymentMethodForm.find('input#continueButton[type="submit"]:not(:disabled)');

    // check master card is confirmed
    if ($continuePaymentMethodButtons.length) {
        console.log('continueButton exists');
        $continuePaymentMethodButtons.first().click();

    } else {
        console.log('NO!! continueButton');
        $choosePaymentMethodForm.find('input[type="radio"][name="paymentMethod"]:nth-of-type(1)').click();
        $choosePaymentMethodForm.find('input#addCreditCardNumber[type="text"]').val('5192696007817127');
        $choosePaymentMethodForm.find('span#confirm-card input[type="submit"]').click();
    }

    // TODO: listen event continuePaymentMethodButtons enabled
}

var automateAmazonOrder = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);

    if (page && page.type == 'amazon_item') { // on Item page
        // TODO: validate amazon item
        
        addItemToCart();

    } else if (page && page.type == 'amazon_shopping_cart') { // on Shopping Cart page
        // TODO: validate amazon item and quantity
        
        proceedToCheckout();

    } else if (page && page.type == 'amazon_checkout_address_select') { // on Checkout: Address Select
        
        goToAddNewAddress();

    } else if (page && page.type == 'amazon_checkout_add_new_address') { // on Checkout: Add New Address
        
        addNewAddress(message.order);
    
    } else if (page && page.type == 'amazon_checkout_choose_shipping') { // on Checkout: Choose shipping option
        
        chooseFreeTwoDayShipping();
        // chooseFreeOneDayShipping();

    } else if (page && page.type == 'amazon_checkout_choose_payment_method') { // on Checkout: Choose payment method

        chooseCreditCardPayment();

    } else {
        console.log('validateCurrentPage', page);
    }
};


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log('onMessage: message', message);
    if (message.app == 'automationJ') { switch(message.task) {
        case 'proceedAmazonItemOrder':
            automateAmazonOrder(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
