var currentTab = null;
var automationTabIds = [];

var $ORDER_TABLE_BODY = $('#order-table tbody');

function get_asins(items) {
    asins = []
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++) {
            if (typeof items[i].asin != 'undefined') {
                asins.push(items[i].asin);
            }
        }
    }
    return asins;
}

chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    // since only one tab should be active and in the current window at once
    // the return variable should only have one entry
    currentTab = tabs[0];
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // check this request from tab created via this screen
    if (automationTabIds.indexOf(sender.tab.id) > 0) {
        // 1. check message
        // 2. send data
        if (message['subject'] == 'automationJ.OrderAmazonItem') {
            sendResponse(orderData);
        }
    }
});

$ORDER_TABLE_BODY.on('click', '.order-individual-button', function(e) {

    if (currentTab == null) {
        alert("something wrong... currentTab is NULL");
    }

    var $this = $(this);
    var orderData = JSON.parse($this.attr('data-orderdata'));
    
    alert('Order ID', $this.attr('data-orderid'));
    alert('Order Object', orderData);
    
    var asins = get_asins(orderData.items);

    // open a new tab to order
    chrome.tabs.create({
        url: 'http://www.amazon.com/dp/' + asins[0], 
        openerTabId: currentTab.id,
    }, function(automationTab) {
        automationTabIds.push(automationTab.id);
    });
    return false;
});

