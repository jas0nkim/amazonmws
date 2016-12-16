var AMAZON_URL_PRIFIX = 'https://www.amazon.com';

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderDetailsPage = /^https:\/\/www.amazon.com\/gp\/aw\/ya(.*$)?/;
    var urlPattern_amazonOrderShippingTrackingPage = /^https:\/\/www.amazon.com\/gp\/your\-account\/ship\-track(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderDetailsPage)) {
        return { validate: true, type: 'amazon_order_details' };
    } else if (currentUrl.match(urlPattern_amazonOrderShippingTrackingPage)) {
        return { validate: true, type: 'amazon_order_shipping_tracking' };
    }
    return false
}

function goToTrackShipment() {
    var ret = false;
    $('.a-box-group:nth-of-type(1) a').each(function() {
        var link = $(this).attr('href');
        if (link.indexOf('ship-track') > -1) {
            ret = true;
            window.open(AMAZON_URL_PRIFIX + link, '_self');
        }
    });
    return ret
}

function retrieveTrackingInfo() {
    var info = { 'carrier': '', 'tracking_number': '' };
    
    // var $trackingInfoBox = $('.a-container:nth-of-type(1) .a-box:nth-of-type(2)');
    // for christmas special screen
    var $trackingInfoBox = $('.a-container div.a-box-group:eq(0) div.a-box:eq(1)');

    var carrierLabel = $.trim($trackingInfoBox.find('span:nth-of-type(1)').text());
    var trackingLabel = $.trim($trackingInfoBox.find('span:nth-of-type(2)').text());
    var carrierValue = $.trim($trackingInfoBox.find('p:nth-of-type(1)').text());
    var trackingValue = $.trim($trackingInfoBox.find('p:nth-of-type(2)').text());

    if (carrierLabel == 'Carrier' && trackingLabel == 'Tracking #') {
        info['carrier'] = carrierValue;
        info['trackingNumber'] = trackingValue;
    } else {
        return false;
    }

    return info;
}

function storeOrderTrackingInfo(carrier, trackingNumber) {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "storeOrderTrackingInfo",
        carrier: carrier,
        trackingNumber: trackingNumber
    }, function(response) {
        console.log('storeOrderTrackingInfo response', response);
    });
}

var automateOrderTracking = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);

    if (page && page.type == 'amazon_order_details') { // on details page

        if (!goToTrackShipment()) {
            storeOrderTrackingInfo(null, null);
        }

    } else if (page && page.type == 'amazon_order_shipping_tracking') { // on order shipping tracking page

        var trackingInfo = retrieveTrackingInfo();
        if (trackingInfo) {
            storeOrderTrackingInfo(trackingInfo.carrier, trackingInfo.trackingNumber);
        } else {
            storeOrderTrackingInfo(null, null);
        }

    } else {
        console.log('validateCurrentPage', page);
    }
};


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'proceedAmazonOrderTracking':
            automateOrderTracking(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
