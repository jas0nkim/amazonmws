var tabAutomationJ = null;
var tabsAmazonOrder = [];

// sample ebay orders
var ebayOrders = [];
ebayOrders.push({
    "record_number": '123',
    "order_id": '123-3KNFUI12349-124',
    "items": [ 
        {
            'item_id': '282037440221',
            'item_title': 'Lightning Cable Syncwire Nylon Braided iPhone Charger [Apple MFi C..., FAST SHIP',
            'asin': 'B01CCRDHF8'
        }
    ],
    "total_price": '52.99',
    "shipping_cost": '0.00',
    "buyer_email": 'srgates@verizon.net',
    "buyer_user_id": 'stacy3656',
    "buyer_status": '',
    "buyer_shipping_name": 'Elisa Jones',
    "buyer_shipping_street1": '921 Oak Dr',
    "buyer_shipping_street2": '',
    "buyer_shipping_city_name": 'Gas City',
    "buyer_shipping_state_or_province": 'IN',
    "buyer_shipping_postal_code": '46933-2157',
    "buyer_shipping_country": 'US',
    "buyer_shipping_phone": '765-243-0301',
    "checkout_status": 'CheckoutComplete',
    "creation_time": '27-Jul-16',
    "paid_time": '27-Jul-16'
});


function findEbayOrderByEbayOrderId(ebayOrderId, allOrders) {
    for (var i = 0; i < allOrders.length; i++) {
        if (allOrders[i]['order_id'] == ebayOrderId) {
            return allOrders[i];
        } else {
            continue;
        }
    }
    return null;
}

function findEbayOrderByTabId(tabId, allOrders, ebayOrderIdTabIdMap) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, ebayOrderIdTabIdMap);
    if (ebayOrderId == null) {        
        return null;
    }    
    return findEbayOrderByEbayOrderId(ebayOrderId, allOrders);
}

function findEbayOrderIdByTabId(tabId, ebayOrderIdTabIdMap) {
    for (var i = 0; i < ebayOrderIdTabIdMap.length; i++) {
        if (ebayOrderIdTabIdMap[i]['AmazonOrderTabId'] == tabId) {
            return ebayOrderIdTabIdMap[i]['ebayOrderId'];
        } else {
            continue;
        }
    }
    return null
}

function findAmazonCurrentUrlByTabId(tabId, ebayOrderIdTabIdMap) {
    for (var i = 0; i < ebayOrderIdTabIdMap.length; i++) {
        if (ebayOrderIdTabIdMap[i]['AmazonOrderTabId'] == tabId) {
            return ebayOrderIdTabIdMap[i]['currentUrl'];
        } else {
            continue;
        }
    }
    return null

}

function updateAmazonOrderCurrentUrlByTabId(tabId, currentUrl, ebayOrderIdTabIdMap) {
    for (var i = 0; i < ebayOrderIdTabIdMap.length; i++) {
        if (ebayOrderIdTabIdMap[i]['AmazonOrderTabId'] == tabId) {
            ebayOrderIdTabIdMap[i]['currentUrl'] = currentUrl;
            return true;
        } else {
            continue;
        }
    }
    return false;
}

function getASINs(ebayOrder) {
    asins = []
    var items = ebayOrder['items'];
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++) {
            if (typeof items[i].asin != 'undefined') {
                asins.push(items[i].asin);
            }
        }
    }
    return asins;
}

function proceedAmazonOrder(amazonOrderTab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateAmazonOrderCurrentUrlByTabId(amazonOrderTab.id, tabChangeInfo.url, tabsAmazonOrder);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        var ebayOrder = findEbayOrderByTabId(amazonOrderTab.id, ebayOrders, tabsAmazonOrder);
        if (ebayOrder == null) {
            return false;
        }

        chrome.tabs.sendMessage(
            amazonOrderTab.id,
            {
                app: 'automationJ',
                task: 'proceedAmazonItemOrder',
                urlOnAddressBar: findAmazonCurrentUrlByTabId(amazonOrderTab.id, tabsAmazonOrder),
                order: ebayOrder,
                '_currentTab': amazonOrderTab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response)
            }
        );
    }
}

// onclick extension icon
chrome.browserAction.onClicked.addListener(function(activeTab) {
    var automationjUrl = "http://45.79.183.134:8092/";
    chrome.tabs.create({
        url: automationjUrl,
    }, function(tab) {
        tabAutomationJ = tab;
    });
});

// on tab updated
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    proceedAmazonOrder(tab, changeInfo);
    return true;
});


// message listener
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'validateAutomationJPage':
            if (tabAutomationJ == null) {
                sendResponse({ success: false,
                    '_currentTab': sender.tab,
                    '_errorMessage': 'Invalid AutomationJ Screen - not registered' 
                });
            } else {
                if (tabAutomationJ.id == sender.tab.id) {
                    sendResponse({ success: true,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                } else {
                    sendResponse({ success: false,
                        '_currentTab': sender.tab,
                        '_errorMessage': 'Invalid AutomationJ Screen - Automation J already opened on another tab'
                    });
                }
            }
            break;

        case 'fetchOrders':
            // $.ajax({
            //     url: "https://api.ipify.org/orders",
            //     dataType: "json",
            //     success: function(data, textStatus, jqXHR) {
            //         console.log(data);
            //     }
            // });
            
            sendResponse({ success: true, orders: ebayOrders,
                '_currentTab': sender.tab,
                '_errorMessage': null
            });
            break;

        case 'orderAmazonItem':
            var ebayOrder = findEbayOrderByEbayOrderId(message.ebayOrderId, ebayOrders);
            var asins = getASINs(ebayOrder);
            chrome.tabs.create({
                url: 'http://www.amazon.com/dp/' + asins[0],
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonOrder.push({ 
                    'ebayOrderId': ebayOrder.order_id, 
                    'AmazonOrderTabId': tab.id,
                    'currentUrl': tab.url
                });
                sendResponse({ success: true, 
                    amazonItemOrderingTab: tab,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
            });
            break;

        case 'getEbayOrder':
            var ebayOrder = findEbayOrderByTabId(sender.tab.id, ebayOrders, tabsAmazonOrder);
            if (ebayOrder == null) {
                sendResponse({ success: false, 
                    '_currentTab': sender.tab, 
                    '_errorMessage': 'no ebay order found' 
                });
            } else {
                sendResponse({ success: true, order: ebayOrder, 
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
            }
            break;
        default:
            sendResponse({ success: false, 
                '_currentTab': sender.tab,
                '_errorMessage': 'invalid task: ' + message.task
            });
            break;
    }}
    return true;
});



