var AMAZON_URL_PRIFIX = 'https://www.amazon.com';

function validateCurrentPage(currentUrl) {
    // var urlPattern_amazonOrderDetailsPage = /^https:\/\/www.amazon.com\/gp\/aw\/ya(.*$)?/;
    var urlPattern_amazonOrderSearchResultPage = /^https:\/\/www.amazon.com\/gp\/your\-account\/order\-history\/\?search(.*$)?/;

    // if (currentUrl.match(urlPattern_amazonOrderDetailsPage)) {
    //     return { validate: true, type: 'amazon_order_details' };
    if (currentUrl.match(urlPattern_amazonOrderSearchResultPage)) {
        return { validate: true, type: 'amazon_order_search_result' };
    }
    return false
}

function isDelivered() {
    var ret = false;
    // var $deliveryStatus = $('div.a-section:nth-of-type(3) div.a-box:nth-of-type(2) div.a-section:nth-of-type(1) h3');
    var $deliveryStatus = $('div#ordersContainer div.a-section:nth-of-type(1) div.a-row:nth-of-type(1) div.a-column:nth-of-type(2) span.a-text-bold');
    var deliveryStatus = null;
    if ($deliveryStatus.length) {
        deliveryStatus = $.trim($deliveryStatus.text());
        if (deliveryStatus.toLowerCase().indexOf('delivered') !== -1) {
            ret = true;
        }
    // } else {
    //     $deliveryStatus = $('div.a-section:nth-of-type(3) div.a-box:nth-of-type(1) div.a-section:nth-of-type(1) h3');
    //     if ($deliveryStatus.length) {
    //         deliveryStatus = $.trim($deliveryStatus.text());
    //         if (deliveryStatus.toLowerCase().indexOf('delivered') !== -1) {
    //             ret = true;
    //         }
    //     }
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
    if (page && page.type == 'amazon_order_search_result') { // on details page
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
