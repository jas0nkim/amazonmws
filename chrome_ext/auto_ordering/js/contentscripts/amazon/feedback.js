var AMAZON_URL_PRIFIX = 'https://www.amazon.com';

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderDetailsPage = /^https:\/\/www.amazon.com\/gp\/aw\/ya(.*$)?/;
    // var urlPattern_amazonOrderSearchResultPage = /^https:\/\/www.amazon.com\/gp\/your\-account\/order\-history\/\?search(.*$)?/;
    var urlPattern_amazonOrderShippingTrackingPage_2 = /^https:\/\/www.amazon.com\/progress\-tracker\/package(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderDetailsPage)) {
        return { validate: true, type: 'amazon_order_details' };
    // if (currentUrl.match(urlPattern_amazonOrderSearchResultPage)) {
    //     return { validate: true, type: 'amazon_order_search_result' };
    } else if (currentUrl.match(urlPattern_amazonOrderShippingTrackingPage_2)) {
        return { validate: true, type: 'amazon_order_shipping_tracking_2' };
    }
    return false
}

function goToTrackShipment() {
    var ret = false;
    $('.a-box-group:nth-of-type(1) a').each(function() {
        var link = $(this).attr('href');
        if (link.indexOf('ship-track') > -1 || link.indexOf('progress-tracker') > -1) {
            ret = true;
            window.open(AMAZON_URL_PRIFIX + link + '&aj=feedback', '_self');
        }
    });
    return ret
}

function isDelivered() {
    var ret = false;
    var deliveryStatus = null;

    var $deliveryStatus = $('#primaryStatus');
    // var $deliveryStatus = $('div#ordersContainer div.a-section:nth-of-type(1) div.a-row:nth-of-type(1) div.a-column:nth-of-type(2) span.a-text-bold');
    if ($deliveryStatus.length) {
        deliveryStatus = $.trim($deliveryStatus.text());
        if (deliveryStatus.toLowerCase().indexOf('delivered') !== -1) {
            ret = true;
        }
    } else {
        $deliveryStatus = $('div.a-container > div.a-section:eq(1) > div.a-box-group > div.a-box:eq(0) > div.a-box-inner > div.a-section:eq(0) > h3');
        if ($deliveryStatus.length) {
            deliveryStatus = $.trim($deliveryStatus.text());
            if (deliveryStatus.toLowerCase().indexOf('delivered') !== -1) {
                ret = true;
            }
        }
    }
    return ret
}

function flagDelivered(isDelivered) {
    if (typeof isDelivered == 'undefined') {
        isDelivered = false;
    }
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "flagDelivered",
        isDelivered: isDelivered,
    }, function(response) {
        console.log('flagDelivered response', response);
    });
}

var automateCheckDelivered = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);

    if (page && page.type == 'amazon_order_details') { // on details page
    // if (page && page.type == 'amazon_order_search_result') { // on search page
        if (!goToTrackShipment()) {
            flagDelivered(false);
        }
    } else if (page && page.type == 'amazon_order_shipping_tracking_2') { // on order shipping tracking page
        flagDelivered(isDelivered());
    } else {
        console.log('validateCurrentPage', page);
    }
};


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'proceedLeaveFeedback':
            automateCheckDelivered(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
