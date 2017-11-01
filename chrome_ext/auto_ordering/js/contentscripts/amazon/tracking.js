var AMAZON_URL_PRIFIX = 'https://www.amazon.com';

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderDetailsPage = /^https:\/\/www.amazon.com\/gp\/aw\/ya(.*$)?/;
    // var urlPattern_amazonOrderSearchResultPage = /^https:\/\/www.amazon.com\/gp\/your\-account\/order\-history\/\?search(.*$)?/;
    var urlPattern_amazonOrderShippingTrackingPage = /^https:\/\/www.amazon.com\/gp\/your\-account\/ship\-track(.*$)?/;
    var urlPattern_amazonOrderShippingTrackingPage_2 = /^https:\/\/www.amazon.com\/progress\-tracker\/package(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderDetailsPage)) {
        return { validate: true, type: 'amazon_order_details' };
    // if (currentUrl.match(urlPattern_amazonOrderSearchResultPage)) {
        // return { validate: true, type: 'amazon_order_search_result' };
    } else if (currentUrl.match(urlPattern_amazonOrderShippingTrackingPage)) {
        return { validate: true, type: 'amazon_order_shipping_tracking' };
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
            window.open(AMAZON_URL_PRIFIX + link + '&aj=tracking', '_self');
        }
    });
    return ret
}

function retrieveTrackingInfo(page) {
    var info = { 'carrier': '', 'tracking_number': '' };
    var $trackingInfoBox = null;
    var carrierLabel = null;
    var trackingLabel = null;
    var carrierValue = null;
    var trackingValue = null;
    
    // var $trackingInfoBox = $('.a-container:nth-of-type(1) .a-box:nth-of-type(2)');
    // for christmas special screen
    if (page == '2') {

        $trackingInfoBox = $('#carrierRelatedInfo-container');

        if ($trackingInfoBox.length) {
            info['carrier'] = $.trim($trackingInfoBox.find('h1').text().replace('Shipped with', ''));
            info['trackingNumber'] = $.trim($trackingInfoBox.find('a.carrierRelatedInfo-trackingId-text').text().replace('Tracking ID', ''));
        } else {
            return false;
        }

    } else {

        $trackingInfoBox = $('.a-container div.a-box-group:eq(0) div.a-box:eq(1)');

        carrierLabel = $.trim($trackingInfoBox.find('span:nth-of-type(1)').text());
        trackingLabel = $.trim($trackingInfoBox.find('span:nth-of-type(2)').text());
        carrierValue = $.trim($trackingInfoBox.find('p:nth-of-type(1)').text());
        trackingValue = $.trim($trackingInfoBox.find('p:nth-of-type(2)').text());

        if (carrierLabel == 'Carrier' && trackingLabel == 'Tracking #') {
            info['carrier'] = carrierValue;
            info['trackingNumber'] = trackingValue;
        } else {
            return false;
        }
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
    // if (page && page.type == 'amazon_order_search_result') { // on search page

        if (!goToTrackShipment()) {
            storeOrderTrackingInfo(null, null);
        }

    } else if (page && (page.type == 'amazon_order_shipping_tracking' || page.type == 'amazon_order_shipping_tracking_2')) { // on order shipping tracking page
        var trackingInfo = null;
        if (page.type == 'amazon_order_shipping_tracking_2') {
            trackingInfo = retrieveTrackingInfo('2');
        } else {
            trackingInfo = retrieveTrackingInfo('1');
        }

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
