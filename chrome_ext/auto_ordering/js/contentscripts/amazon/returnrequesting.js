var AMAZON_DOMAIN = 'https://www.amazon.com';
var _DATA = {
    amazonOrderId: null,
    asin: null,
    amazonOrderReturnId: null,
    ebayOrderReturnId: null,
    quantity: null
};

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderSearchResultPage = /^https?:\/\/www.amazon.com\/gp\/your\-account\/order\-history\/\?search=(.*$)?/;
    var urlPattern_amazonOrderReturnReasonPage = /^https?:\/\/www.amazon.com\/returns\/order\/(.*$)?/;
    var urlPattern_amazonOrderReturnResolutionPage = /^https?:\/\/www.amazon.com\/returns\/resolution\/(.*$)?/;
    var urlPattern_amazonOrderReturnMethodPage = /^https?:\/\/www.amazon.com\/returns\/method\/(.*$)?/;
    var urlPattern_amazonOrderReturnConfirmationPage = /^https?:\/\/www.amazon.com\/returns\/confirmation\/(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderSearchResultPage)) {
        return { validate: true, type: 'amazon_order_search_result' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnReasonPage)) {
        return { validate: true, type: 'amazon_order_return_reason' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnResolutionPage)) {
        return { validate: true, type: 'amazon_order_return_resolution' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnMethodPage)) {
        return { validate: true, type: 'amazon_order_return_method' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnConfirmationPage)) {
        return { validate: true, type: 'amazon_order_return_confirmation' };
    }
    return false;
}

function goToReturnItem() {
    var $container = $('#ordersContainer');
    // get correct item
    $container.find('div.js-item').each(function(e) {
        var $this = $(this);
        if ($this.find('div.item-view-left-col-inner a').attr('href').match(_DATA['asin'])) {
            $this.find('a[href^="/returns/order/"]')[0].click();
        }
    });
}

function chooseReturnReason() {
    var $form = $('#itemsForm');
    var $continueReturnButton = $form.find('#continueItemsPageButton:visible');

    if ($continueReturnButton.length) {
        $continueReturnButton.find('a#continueItemsPageButton-announce')[0].click();
    } else {
        if ($form.find('input#item_0-primaryQuestionSetId').length) {
            $form.find('input#item_0-primaryQuestionSetId').closest('div').find('a div.a-box-inner').first()[0].click();
        }
        // returning reason screen
        // click Item defective or doesn't work
        $('.a-popover:visible span:contains("Item defective")').closest('a.a-touch-link')[0].click();
    }
}

function chooseRefundResolution() {
    var $form = $('#resolutionForm');
    // select refund accorion
    $form.find('a#Refund-accordion')[0].click();
    var $refundContainer = $form.find('div#Refund');
    if ($refundContainer.length) {
        $refundContainer.find('li span:contains("Original payment method")').closest('button')[0].click();
        $refundContainer.find('a#Refund-continue-announce')[0].click();
    }
}

function chooseRefundMethod() {
    var $form = $('#parentForm');
    var $selectedAccordion = null
    if ($form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff")').length) {
        $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff")').closest('a.a-accordion-row')[0].click();
        $selectedAccordion = $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff")').closest('div.a-accordion-row-container');
    } else if ($form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').length) {
        $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').closest('a.a-accordion-row')[0].click();
        $selectedAccordion = $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').closest('div.a-accordion-row-container');
    }
    if ($selectedAccordion) {
        $selectedAccordion.find('div.a-accordion-inner a:contains("Submit")')[0].click();
    }
}

function storeAmazonOrderReturn(returnId) {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "storeAmazonOrderReturn",
        amazonOrderId: _DATA['amazonOrderId'],
        asin: _DATA['asin'],
        amazonOrderReturnId: returnId,
        ebayOrderReturnId: _DATA['ebayOrderReturnId'],
        quantity: _DATA['quantity'],
    }, function(response) {
        console.log('storeAmazonOrderReturn response', response);
    });
}

// TODO: need to improve
function retrieveReturnIdFromUrl(url) {
    return url.replace('https://www.amazon.com/returns/confirmation/', '');
}

var automateAmazonOrderReturnRequest = function(message) {
    var page = validateCurrentPage(message.urlOnAddressBar);
    _DATA['amazonOrderId'] = message.amazonOrderId;
    _DATA['asin'] = message.asin;
    _DATA['ebayOrderReturnId'] = message.ebayOrderReturnId;
    _DATA['quantity'] = message.quantity;

    if (page && page.type == 'amazon_order_search_result') { // amazon order search result page
        goToReturnItem();
    } else if (page && page.type == 'amazon_order_return_reason') { // amazon order return reason page
        setTimeout(function() {
            chooseReturnReason();
        }, 1000);
    } else if (page && page.type == 'amazon_order_return_resolution') { // amazon order return resolution page
        setTimeout(function() {
            chooseRefundResolution();
        }, 1000);
    } else if (page && page.type == 'amazon_order_return_method') { // amazon order return method page
        setTimeout(function() {
            chooseRefundMethod();
        }, 1000);
    } else if (page && page.type == 'amazon_order_return_confirmation') { // amazon order return confirmation page
        setTimeout(function() {
            var returnId = retrieveReturnIdFromUrl(message.urlOnAddressBar);
            storeAmazonOrderReturn(returnId);
        }, 1000);
    }
};

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'proceedAmazonOrderReturnRequesting':
            automateAmazonOrderReturnRequest(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
