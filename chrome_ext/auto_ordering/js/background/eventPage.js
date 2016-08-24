var _amazon_account_id = 2

var API_SERVER_URL = 'http://45.79.183.134:8091/api';
var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';

var tabAutomationJ = null;
var tabsAmazonOrder = [];
var ebayOrders = [];
/*************************
i.e. amazon_order object
{
    order_id: '234-234',
    item_price: 12.99,
    shipping_and_handling: 0.00,
    tax: 1.08,
    total: 14.07
}
**************************/

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

function setAmazonOrderIntoEbayOrderByEbayOrderId(ebayOrderId, amazonOrder) {
    // ebayOrders: global variable
    for (var i = 0; i < ebayOrders.length; i++) {
        if (ebayOrders[i]['order_id'] == ebayOrderId) {
            ebayOrders[i]['amazon_order'] = amazonOrder;
            return true;
        } else {
            continue;
        }
    }
    return false;
}

function setAmazonOrderIntoEbayOrderByTabId(tabId, amazonOrder, ebayOrderIdTabIdMap) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, ebayOrderIdTabIdMap);
    if (ebayOrderId == null) {
        return false;
    }

    return setAmazonOrderIntoEbayOrderByEbayOrderId(ebayOrderId, amazonOrder);
}

function setAmazonOrderIdByEbayOrderId(ebayOrderId, amazonOrderId) {
    // ebayOrders: global variable
    for (var i = 0; i < ebayOrders.length; i++) {
        if (ebayOrders[i]['order_id'] == ebayOrderId) {
            if (typeof ebayOrders[i]['amazon_order'] == 'undefined') {
                ebayOrders[i]['amazon_order'] = {};
            }
            ebayOrders[i]['amazon_order']['order_id'] = amazonOrderId;
            return ebayOrders[i];
        } else {
            continue;
        }
    }
    return false;
}

function setAmazonOrderIdByTabId(tabId, amazonOrderId, ebayOrderIdTabIdMap) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, ebayOrderIdTabIdMap);
    if (ebayOrderId == null) {
        return false;
    }

    return setAmazonOrderIdByEbayOrderId(ebayOrderId, amazonOrderId);
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
            if (typeof items[i].sku != 'undefined') {
                asins.push(items[i].sku);
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
    chrome.tabs.create({
        url: AUTOMATIONJ_SERVER_URL,
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
            $.ajax({
                url: API_SERVER_URL + '/orders/',
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    ebayOrders = response.data;
                    sendResponse({ success: true, orders: ebayOrders,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                },
                error: function() {
                    ebayOrders = []
                    sendResponse({ success: false, orders: ebayOrders,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
            
            break;

        case 'orderAmazonItem':
            var ebayOrder = findEbayOrderByEbayOrderId(message.ebayOrderId, ebayOrders);
            var asins = getASINs(ebayOrder);
            chrome.tabs.create({
                url: 'https://www.amazon.com/dp/' + asins[0],
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

        case 'storeAmazonOrderPrice':
            console.log('automationJ storeAmazonOrderPrice:', message);
            var amazonOrder = {
                'order_id': null,
                'item_price': message.itemPrice,
                'shipping_and_handling': message.shippingHandling,
                'tax': message.tax,
                'total': message.total
            };
            var result = setAmazonOrderIntoEbayOrderByTabId(sender.tab.id, amazonOrder, tabsAmazonOrder);
            sendResponse({ success: result,
                '_currentTab': sender.tab,
                '_errorMessage': null
            });
            break;
        
        case 'storeAmazonOrderId':
            console.log('automationJ storeAmazonOrderId:', message);
            var order = setAmazonOrderIdByTabId(sender.tab.id, message.amazonOrderId, tabsAmazonOrder)
            console.log('ebay-amazon order', order);

            asins = getASINs(order);

            $.ajax({
                url: API_SERVER_URL + '/orders/amazon_orders/',
                method: 'POST',
                dataType: 'json',
                data: {
                    'amazon_account_id': _amazon_account_id,
                    'amazon_order_id': order.amazon_order.order_id,
                    'ebay_order_id': order.order_id,
                    'asin': asins[0],
                    'item_price': order.amazon_order.item_price,
                    'shipping_and_handling': order.amazon_order.shipping_and_handling,
                    'tax': order.amazon_order.tax,
                    'total': order.amazon_order.total
                },
                success: function(response, textStatus, jqXHR) {
                    sendResponse({ success: true,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });

                    if (tabAutomationJ != null) {
                        chrome.tabs.sendMessage(
                            tabAutomationJ.id,
                            {
                                app: 'automationJ',
                                task: 'succeededAmazonOrdering',
                                ebayOrderId: order.order_id,
                                amazonOrderId: order.amazon_order.order_id,
                                amazonOrderTotal: order.amazon_order.total,
                                ebayOrderTotal: order.total_price,
                                '_currentTab': tabAutomationJ,
                                '_errorMessage': null,
                            }, function(response) {
                                console.log(response)
                            }
                        );
                    }
                },
                error: function() {
                    sendResponse({ success: false,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
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



