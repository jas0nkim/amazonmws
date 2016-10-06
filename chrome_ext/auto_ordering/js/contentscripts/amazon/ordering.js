function validateCurrentPage(currentUrl) {
    var urlPattern_amazonItemPage_mobile = /^https?:\/\/www.amazon.com\/gp\/aw\/d\/([A-Z0-9]{10})(.*$)?/;
    var urlPattern_amazonItemPage_desktop = /^https?:\/\/www.amazon.com\/([^\/]+\/[^\/]+|dp)\/([A-Z0-9]{10})(\/.*$)?/;
    var urlPattern_amazonShoppingCartPage = /^https:\/\/www.amazon.com\/gp\/aw\/c(.*$)?/;
    var urlPattern_amazonCheckoutAddressSelectPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutAddNewAddressPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/new\.html(.*$)?/;
    var urlPattern_amazonCheckoutChooseShippingPage = /^https:\/\/www.amazon.com\/gp\/buy\/shipoptionselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutChoosePaymentMethodPage = /^https:\/\/www.amazon.com\/gp\/buy\/payselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutChooseGiftOptionPage = /^https:\/\/www.amazon.com\/gp\/buy\/gift\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutSummaryPage = /^https:\/\/www.amazon.com\/gp\/buy\/spc\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutThankYouPage = /^https:\/\/www.amazon.com\/gp\/buy\/thankyou\/handlers\/display\.html(.*$)?/;

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
    } else if (currentUrl.match(urlPattern_amazonCheckoutChooseGiftOptionPage)) {
        return { validate: true, type: 'amazon_checkout_choose_gift_option' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutSummaryPage)) {
        return { validate: true, type: 'amazon_checkout_summary' };
    } else if (currentUrl.match(urlPattern_amazonCheckoutThankYouPage)) {
        return { validate: true, type: 'amazon_checkout_thank_you' };
    }
    return false
}

function isFBA() {
    var $primeIcon = $('table#price i.a-icon-prime');
    var $priceInfo = $('#priceBadging_feature_div');
    var $merchantInfo = $('#merchant-info');
    return ($primeIcon.length && $primeIcon.is(':visible')) || ($priceInfo.length && $.trim($priceInfo.text()).indexOf('Prime') !== -1) || ($merchantInfo.length && ($.trim($merchantInfo.text()).indexOf('sold by Amazon.com') !== -1 || $.trim($merchantInfo.text()).indexOf('Fulfilled by Amazon') !== -1));
}

function checkOneTimePurchaseIfExists() {
    var $oneTimeBuyBox = $('#oneTimeBuyBox');
    if ($oneTimeBuyBox.length) {
        $oneTimeBuyBox.click();
        setTimeout(null, 1500); // then wait
    }
}

function addItemToCart() {
    $('#add-to-cart-button').click();
}

function proceedToCheckout() {
    $('#sc-mini-buy-box button').click();
}

function verifyShippingAddress() {
    if ($.trim($('h1').text()) != 'Verify your shipping address') {
        return false;
    }
    var $verifyShippingAddressForm = $('.a-container form');
    $verifyShippingAddressForm.find('input[type="radio"][name="addr"][value="addr_0"]').click();
    $verifyShippingAddressForm.find('input[type="submit"][name="useSelectedAddress"]').click();
    return true
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
    $newAddressForm.find('input[name="enterAddressPhoneNumber"]').val(order.buyer_shipping_phone != '' ? order.buyer_shipping_phone : Math.floor(100000000 + Math.random() * 900000000) + '');
    $newAddressForm.find('input[type="submit"][name="shipToThisAddress"]').click();
}

function chooseFreeTwoDayShipping() {
    var $chooseShippingForm = $('form#shippingOptionFormId');
    $chooseShippingForm.find('input[type="radio"][name="order_0_ShippingSpeed"][value="second"]').click();
    $chooseShippingForm.find('input[type="submit"]').click();
}

// function chooseFreeOneDayShipping() {}

function _waitAndSubmitCreditCardPayment(count) {
    if (typeof count == 'undefined') {
        count = 0
    }

    if (count > 10) { // break infinit loop
        // TODO: error code/message
        return false;
    }

    var $continuePaymentMethodButtons = $('#select-payments-view form[data-action="submit-payment-form"] input#continueButton[type="submit"]:not(:disabled)');

    if ($continuePaymentMethodButtons.length) {
        // wait for loading image removed
        setTimeout(function() { $continuePaymentMethodButtons.first().click(); }, 1500);
    } else {
        count++
        setTimeout(function() { _waitAndSubmitCreditCardPayment(count) }, 500);
    }
}

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

        _waitAndSubmitCreditCardPayment();
    }
}

function addGiftReceipt() {
    var $summaryForm = $('form#spc-form');
    var $addGiftReceiptButton = $summaryForm.find('span.gift-options-button a');

    // add a gift receipt
    if ($addGiftReceiptButton.length && $.trim($addGiftReceiptButton.find('span:nth-of-type(1)').text()).match(/^add\sa\sgift\sreceipt(.*$)?/i)) {
        window.location.href = $addGiftReceiptButton.attr('href');
    } else {
        // TODO: error code/message - no gift receipt option available
        return false;
    }
}

function chooseGiftReceiptOption() {
    var $giftForm = $('form#giftForm');
    var $giftReceiptCheckbox = $giftForm.find('input#includeReceiptCheckbox-0[type="checkbox"]');
    var $giftMessageArea = $giftForm.find('textarea#message-area-0');
    
    // make sure gift receipt checkbox is checked
    if ($giftReceiptCheckbox.prop('checked') != true) {
        $giftReceiptCheckbox.prop('checked', true);
    }

    // set message empty
    $giftMessageArea.val('');

    // save gift option
    $giftForm.find('.save-gift-button-box input[type="submit"]').click();

    return true;
}

function placeOrder() {
    setTimeout(function() { // force wait for document loads
        var $summaryForm = $('form#spc-form');
        var label, price;
        var itemPrice = 0.00;
        var shippingHandling = 0.00;
        var tax = 0.00;
        var total = 0.00;

        $summaryForm.find('table#subtotals-marketplace-table tbody tr').each(function() {

            label = $.trim($(this).find('td:nth-of-type(1)').text());
            price = parseFloat($.trim($(this).find('td:nth-of-type(2)').text()).replace('$', ''));

            if (label.indexOf("Items:") >= 0) {
                itemPrice = price;
            } else if (label.indexOf("Shipping") >= 0) {
                shippingHandling = price;
            } else if (label.indexOf("Estimated tax") >= 0) {
                tax = price;
            } else if (label.indexOf("Order total:") >= 0) {
                total = price;
            }
        });

        chrome.runtime.sendMessage({
            app: "automationJ",
            task: "storeAmazonOrderPrice",
            itemPrice: itemPrice,
            shippingHandling: shippingHandling,
            tax: tax,
            total: total
        }, function(response) {
            $summaryForm.find('input[type="submit"][name="placeYourOrder1"]').first().click();
        });
    }, 1500);
}

function storeAmazonOrderId(orderId) {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "storeAmazonOrderId",
        amazonOrderId: orderId
    }, function(response) {
        console.log('storeAmazonOrderId response', response);
    });
}

function getParameterByName(name, url) {
    if (!url) {
        return false;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function retrieveOrderIdFromUrl(url) {
    return getParameterByName('orderId', url);
}

var automateAmazonOrder = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);

    if (page && page.type == 'amazon_item') { // on Item page
        // TODO: validate amazon item
        if (isFBA()) {
            checkOneTimePurchaseIfExists();
            addItemToCart();
        } else {
            alert('automationJ message: NOT A FBA ITEM!!');
        }

    } else if (page && page.type == 'amazon_shopping_cart') { // on Shopping Cart page
        // TODO: validate amazon item and quantity
        // check if there are more items to order
        chrome.runtime.sendMessage({
            app: "automationJ",
            task: "hasMoreAmazonItemToOrder"
        }, function(response) {
            if (response.nextAmazonItemUrl == null) {
                proceedToCheckout();
            } else {
                window.location.replace(response.nextAmazonItemUrl);
            }
        });
    } else if (page && page.type == 'amazon_checkout_address_select') { // on Checkout: Address Select
        
        var verifying = verifyShippingAddress();
        if (verifying == false) {
            goToAddNewAddress();
        }

    } else if (page && page.type == 'amazon_checkout_add_new_address') { // on Checkout: Add New Address
        
        addNewAddress(message.order);
    
    } else if (page && page.type == 'amazon_checkout_choose_shipping') { // on Checkout: Choose shipping option
        
        chooseFreeTwoDayShipping();
        // chooseFreeOneDayShipping();

    } else if (page && page.type == 'amazon_checkout_choose_payment_method') { // on Checkout: Choose payment method

        chooseCreditCardPayment();

    } else if (page && page.type == 'amazon_checkout_choose_gift_option') { // on Checkout: Choose gift option

        chooseGiftReceiptOption();

    } else if (page && page.type == 'amazon_checkout_summary') { // on Checkout: Summary

        // TODO: validate order
        //          - price
        //          - quantity
        //          - shipping address
        addGiftReceipt();
        placeOrder();

    } else if (page && page.type == 'amazon_checkout_thank_you') { // on Checkout: Thank you message

        var orderId = retrieveOrderIdFromUrl(message.urlOnAddressBar);
        storeAmazonOrderId(orderId);

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
