var currentTabId = null;
chrome.runtime.sendMessage({
    app: "automationJ",
    subject: "getCurrentTabId" 
}, function(response) {
    currentTabId = response.currentTabId;
});
var i = 0;
while (currentTabId != null && i < 10) {
    // try 5 seconds: .5 x 10
    setTimeout(function() { console.log('currentTabId is null... wait a sec...'); }, 500);
    i++;
}
if (currentTabId == null) {
    console.log('unable to set currentTabId.... something wrong');
}

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
    if (currentTabId == null) {

        alert("something wrong... currentTabId is NULL");
    }

    var $this = $(this);
    var orderData = JSON.parse($this.attr('data-orderdata'));
    
    alert('Order ID', $this.attr('data-orderid'));
    alert('Order Object', orderData);
    
    var asins = get_asins(orderData.items);

    chrome.runtime.sendMessage({ 
        app: "automationJ",
        subject: "getCurrentTabId" 
    }, function(response) {        
        // open a new tab to order
        currentTabId = response.currentTabId;
    });


    chrome.runtime.sendMessage({ 
        app: "automationJ",
        subject: "openNewTab",
        url: 'https://www.amazon.com/dp/' + asins[0],
        openerTabId: currentTabId
    }, function(response) {
        currentTabId = response.currentTabId;
    });

    chrome.tabs.create({
        url: 'https://www.amazon.com/dp/' + asins[0], 
        openerTabId: currentTab.id,
    }, function(automationTab) {
        automationTabIds.push(automationTab.id);
    });
    return false;
});

