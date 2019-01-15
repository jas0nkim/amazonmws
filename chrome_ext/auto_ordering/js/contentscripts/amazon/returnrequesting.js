var AMAZON_DOMAIN = 'https://www.amazon.com';
var _DATA = {
    amazonOrderId: null,
    asin: null,
    amazonOrderReturnId: null,
    ebayOrderReturnId: null,
    quantity: null,
    rma: null,
    refundedAmount: null,
    refundedDate: null,
    returnedDate: null
};

function validateCurrentPage(currentUrl) {
    var urlPattern_amazonOrderSearchResultPage = /^https?:\/\/www.amazon.com\/gp\/your\-account\/order\-history\/\?search=(.*$)?/;
    var urlPattern_amazonOrderReturnReasonPage = /^https?:\/\/www.amazon.com\/returns\/order\/(.*$)?/;
    var urlPattern_amazonOrderReturnResolutionPage = /^https?:\/\/www.amazon.com\/returns\/resolution\/(.*$)?/;
    var urlPattern_amazonOrderReturnMethodPage = /^https?:\/\/www.amazon.com\/returns\/method\/(.*$)?/;
    var urlPattern_amazonOrderReturnMethodPage_2 = /^https?:\/\/www.amazon.com\/spr\/returns\/contract\/(.*$)?/;
    var urlPattern_amazonOrderReturnAllInOneStepPage = /^https?:\/\/www.amazon.com\/spr\/returns\/cart\?(.*$)?/;

    var urlPattern_amazonOrderReturnConfirmationPage = /^https?:\/\/www.amazon.com\/returns\/confirmation\/(.*$)?/;

    if (currentUrl.match(urlPattern_amazonOrderSearchResultPage)) {
        return { validate: true, type: 'amazon_order_search_result' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnReasonPage)) {
        return { validate: true, type: 'amazon_order_return_reason' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnResolutionPage)) {
        return { validate: true, type: 'amazon_order_return_resolution' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnMethodPage)) {
        return { validate: true, type: 'amazon_order_return_method' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnMethodPage_2)) {
        return { validate: true, type: 'amazon_order_return_method_2' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnAllInOneStepPage)) {
        return { validate: true, type: 'amazon_order_return_all_in_one_step' };
    } else if (currentUrl.match(urlPattern_amazonOrderReturnConfirmationPage)) {
        return { validate: true, type: 'amazon_order_return_confirmation' };
    }
    return false;
}

function goToReturnItem() {
    var $container = $('#ordersContainer');
    var itemFound = false;
    // get correct item
    $container.find('div.js-item').each(function(e) {
        var $this = $(this);
        if ($this.find('div.item-view-left-col-inner a').attr('href').match(_DATA['asin'])) {
            itemFound = true;
            if ($this.find('a[href^="/returns/label/"]').length) {
                var q = $this.find('a[href^="/returns/label/"]').attr('href').split('/');
                var amazonOrderReturnId = q[3];
                _DATA['rma'] = q[5];
                storeAmazonOrderReturn(amazonOrderReturnId);
            } else if ($this.find('a[href^="/returns/order/"]').length) {
                $this.find('a[href^="/returns/order/"]')[0].click();
            } else { // no return button (option) found
                closeTabWithError('No return button (option) found');
            }
        }
    });
    if (itemFound == false) {
        closeTabWithError('Returning Amazon item cannot found');
    }
}

function getRefundInfo($refundIssuedOn, $returnReceivedOn) {
    if ($refundIssuedOn && $refundIssuedOn.length) {
        _DATA['refundedAmount'] = $refundIssuedOn.find('font').text().trim().replace('$', '');
        _DATA['refundedDate'] = $refundIssuedOn.contents().last().text().replace(/refund issued on/ig, '').replace('.', '').replace(',', '').replace(':', '').trim();
    }
    if ($returnReceivedOn && $returnReceivedOn.length) {
        _DATA['returnedDate'] = $returnReceivedOn.contents().last().text().replace(/return received on/ig, '').replace('.', '').replace(',', '').replace(':', '').trim();
    }
    storeAmazonOrderReturn(null);
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

function chooseRefundResolution(page) {
    var $form = null;
    if (page == '2') {
        $form = $('#resolutionSectionForm');
        if ($form.length) {
            $form.find('a.a-accordion-row span:contains("ending in")').closest('a')[0].click();
            $('#resolutions-section-continue-button')[0].click();
            setTimeout(function() {
                chooseRefundMethod(page);
            }, 3000);
        }
    } else {
        $form = $('#resolutionForm');
        // select refund accorion
        $form.find('a#Refund-accordion')[0].click();
        var $refundContainer = $form.find('div#Refund');
        if ($refundContainer.length) {
            $refundContainer.find('li span:contains("Original payment method")').closest('button')[0].click();
            $refundContainer.find('a#Refund-continue-announce')[0].click();
        }
    }
}

function chooseRefundMethod(page) {
    var $form = null;
    if (page == '2') {
        $form = $('#methodSectionForm');
        if ($form.length < 1) {
            chooseRefundResolution('2');
            return false;
        }
    } else{
        $form = $('#parentForm');
    }
    var $selectedAccordion = null;
    if ($form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff"):not(:contains("no box or label needed"))').length) {
        $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff"):not(:contains("no box or label needed"))').closest('a.a-accordion-row')[0].click();
        $selectedAccordion = $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("UPS Dropoff"):not(:contains("no box or label needed"))').closest('div.a-accordion-row-container');
    } else if ($form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').length) {
        $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').closest('a.a-accordion-row')[0].click();
        $selectedAccordion = $form.find('div.a-accordion-row-container div.a-accordion-row-a11y span:contains("USPS (US Postal Service) Dropoff")').closest('div.a-accordion-row-container');
    }
    if ($selectedAccordion) {
        if (page == '2') {
            if ($('#methodsSectionContinueButton input[type=submit]').length) {
                $('#methodsSectionContinueButton input[type=submit]')[0].click();
            } else if ($('#methods-continue-section input[type=submit]').length) {
                $('#methods-continue-section input[type=submit]')[0].click();
            }
        } else {
            $selectedAccordion.find('div.a-accordion-inner a:contains("Submit")')[0].click();
        }
    }
}

function chooseRefundAllInOneStep() {
    // choose reason
    var $form = $('#itemSectionForm');
    if ($form.length) {
        if ($form.find('h4:contains("already requested a return of this item")').length) {
            // already return requested - checking return status
            var $refundIssuedOn = null;
            var $returnReceivedOn = null;
            if ($form.find('span:contains("refund issued on")').length) {
                $refundIssuedOn = $form.find('span:contains("refund issued on")');
            } else if ($form.find('span:contains("Refund issued on")').length) {
                $refundIssuedOn = $form.find('span:contains("Refund issued on")');
            }
            if ($form.find('span:contains("return received on")').length) {
                $returnReceivedOn = $form.find('span:contains("return received on")');
            } else if ($form.find('span:contains("Return received on")').length) {
                $returnReceivedOn = $form.find('span:contains("Return received on")');
            }
            if ($refundIssuedOn || $returnReceivedOn) {
                getRefundInfo($refundIssuedOn, $returnReceivedOn);
            }
        } else {
            // step 1. click 'see all reasons' button/link
            var $seeAllReasonsButton = $form.find('a:contains("SEE ALL REASONS")');
            if ($seeAllReasonsButton.length) {
                $seeAllReasonsButton[0].click();
            }
            // step 2. select 'Item defective or doesn’t work'
            $('span.a-text-bold:contains("Item defective")').closest('label').find('input[type=radio]')[0].click();
            // step 3. click continue button
            $('#items-section-continue-button')[0].click();
            setTimeout(function() {
                chooseRefundResolution('2');
            }, 3000);
        }
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
        rma: _DATA['rma'],
        refundedAmount: _DATA['refundedAmount'],
        refundedDate:_DATA['refundedDate'],
        returnedDate:_DATA['returnedDate']
    }, function(response) {
        console.log('storeAmazonOrderReturn response', response);
    });
}

function closeTabWithError(errorMessage) {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "closeTabWithError",
        errorMessage: errorMessage
    }, function(response) {
        console.log('closeTabWithError response', response);
    });
}

// TODO: need to improve
function retrieveReturnIdFromUrl(url) {
    return url.replace('https://www.amazon.com/returns/confirmation/', '').replace('?ref_=m_orc_spr_mthd_post', '');
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
            var $refundIssuedOn = null;
            var $returnReceivedOn = null;
            if ($('span:contains("refund issued on")').length) {
                $refundIssuedOn = $('span:contains("refund issued on")');
            } else if ($('span:contains("Refund issued on")').length) {
                $refundIssuedOn = $('span:contains("Refund issued on")');
            }
            if ($('span:contains("return received on")').length) {
                $returnReceivedOn = $('span:contains("return received on")');
            } else if ($('span:contains("Return received on")').length) {
                $returnReceivedOn = $('span:contains("Return received on")');
            }
            if ($refundIssuedOn || $returnReceivedOn) {
                getRefundInfo($refundIssuedOn, $returnReceivedOn);
            } else {
                chooseReturnReason();
            }
        }, 1000);
    } else if (page && page.type == 'amazon_order_return_resolution') { // amazon order return resolution page
        setTimeout(function() {
            chooseRefundResolution('1');
        }, 1000);
    } else if (page && page.type == 'amazon_order_return_method') { // amazon order return method page
        setTimeout(function() {
            chooseRefundMethod('1');
        }, 1500);
    } else if (page && page.type == 'amazon_order_return_method_2') { // amazon order return method page
        setTimeout(function() {
            chooseRefundMethod('2');
        }, 1500);
    } else if (page && page.type == 'amazon_order_return_all_in_one_step') {
        setTimeout(function() {
            chooseRefundAllInOneStep();
        }, 1500);
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
