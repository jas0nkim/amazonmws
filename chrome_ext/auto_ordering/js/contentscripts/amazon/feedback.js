var AMAZON_URL_PRIFIX = 'https://www.amazon.com';

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderDetailsPage = /^https:\/\/www.amazon.com\/gp\/aw\/ya(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderDetailsPage)) {
        return { validate: true, type: 'amazon_order_details' };
    }
    return false
}

function isDelivered() {
    var ret = false;
    var $deliveryStatus = $('div.a-section:nth-of-type(3) div.a-box:nth-of-type(2) div.a-section:nth-of-type(1) h3');
    var deliveryStatus = null;
    if ($deliveryStatus.length) {
        deliveryStatus = $.trim($deliveryStatus.text());
        if (deliveryStatus.toLowerCase().indexOf('delivered') !== -1) {
            ret = true;
        }
    }

    return ret
}

// function retrieveTrackingInfo() {
//     var info = { 'carrier': '', 'tracking_number': '' };

//     var carrierLabel = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) span:nth-of-type(1)').text());
//     var trackingLabel = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) span:nth-of-type(2)').text());
//     var carrierValue = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) p:nth-of-type(1)').text());
//     var trackingValue = $.trim($('.a-container:nth-of-type(1) .a-box:nth-of-type(2) p:nth-of-type(2)').text());

//     if (carrierLabel == 'Carrier' && trackingLabel == 'Tracking #') {
//         info['carrier'] = carrierValue;
//         info['trackingNumber'] = trackingValue;
//     } else {
//         alert("automationJ message: NO TRACK INFO YET!!");
//         return false;
//     }

//     return info;
// }

function flagDelivered() {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "flagDelivered",
    }, function(response) {
        console.log('flagDelivered response', response);
    });
}

var automateCheckDelivered = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);

    if (page && page.type == 'amazon_order_details') { // on details page

        if (isDelivered()) {
            // alert('automationJ message: PACKAGE DELIVERED!!');
            flagDelivered();
        } else {
            alert('automationJ message: PACKAGE HASN\'T DELIVERED YET!!');
        }

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
