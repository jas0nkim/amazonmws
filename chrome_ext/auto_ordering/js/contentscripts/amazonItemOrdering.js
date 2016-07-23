function validateCurrentPage(currentUrl) {
    var urlPattern_amazonItemPage_mobile = /^https?:\/\/www.amazon.com\/gp\/aw\/d\/([A-Z0-9]{10})(.*$)?/;
    var urlPattern_amazonItemPage_desktop = /^https?:\/\/www.amazon.com\/([^\/]+\/[^\/]+|dp)\/([A-Z0-9]{10})(\/.*$)?/;
    var urlPattern_amazonShoppingCartPage = /^https:\/\/www.amazon.com\/gp\/aw\/c(.*$)?/;
    var urlPattern_amazonCheckoutAddressSelectPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/display\.html(.*$)?/;
    var urlPattern_amazonCheckoutAddNewAddressPage = /^https:\/\/www.amazon.com\/gp\/buy\/addressselect\/handlers\/new\.html(.*$)?/;
    var urlPattern_amazonCheckoutChooseShippingPage = /^https:\/\/www.amazon.com\/gp\/buy\/shipoptionselect\/handlers\/display\.html(.*$)?/;

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

var automateAmazonOrder = function(response) {
    console.log('automateAmazonOrder response', response);

    if (response.success == false) {
        return false;
    }

    var page = validateCurrentPage(response['_currentTab']['url']);

    if (page && page.type == 'amazon_item') { // on Item page
        // TODO: validate amazon item
        
        addItemToCart();

    } else if (page && page.type == 'amazon_shopping_cart') { // on Shopping Cart page
        // TODO: validate amazon item and quantity
        
        proceedToCheckout();

    } else if (page && page.type == 'amazon_checkout_address_select') { // on Checkout: Address Select
        
        goToAddNewAddress();

    } else if (page && page.type == 'amazon_checkout_add_new_address') { // on Checkout: Add New Address
        
        addNewAddress(response.order);
    
    } else if (page && page.type == 'amazon_checkout_choose_shipping') { // on Checkout: Choose shipping option
        
        chooseFreeTwoDayShipping();
        // chooseFreeOneDayShipping();
    }
};

chrome.runtime.sendMessage({
    app: "automationJ",
    task: "getEbayOrder"
}, automateAmazonOrder);
