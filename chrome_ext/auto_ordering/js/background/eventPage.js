var _amazon_account_id = 2

var API_SERVER_URL = 'http://45.79.183.134:8091/api';
var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';
var AMAZON_ORDER_DETAIL_URL_PRIFIX = 'https://www.amazon.com/gp/aw/ya/?ie=UTF8&ac=od&ii=&noi=&of=&oi=&oid=';

var tabAutomationJ = null;
var tabsAmazonOrder = [];
var tabsAmazonOrderTracking = [];
var tabsFeedback = [];

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

function isAutomationJTab(tab) {
    if (tabAutomationJ == null || tabAutomationJ.id != tab.id) {
        return false;
    }
    return true;
}

function isTabRegistered(map, tab) {
    if (map.length < 1) {
        return false;
    }
    for (var i = 0; i < map.length; i++) {
        if (tab.id == map[i]['tabId']) {
            return true;
        }
    }
    return false;
}

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

function findEbayOrderByTabId(tabId, allOrders, map) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, map);
    if (ebayOrderId == null) {        
        return null;
    }    
    return findEbayOrderByEbayOrderId(ebayOrderId, allOrders);
}

function findEbayOrderIdByTabId(tabId, map) {
    for (var i = 0; i < map.length; i++) {
        if (map[i]['tabId'] == tabId) {
            return map[i]['ebayOrderId'];
        } else {
            continue;
        }
    }
    return null;
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

function setAmazonOrderIntoEbayOrderByTabId(tabId, amazonOrder, map) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, map);
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

function setOrderTrackingByEbayOrderId(ebayOrderId, trackingInfo) {
    // ebayOrders: global variable
    for (var i = 0; i < ebayOrders.length; i++) {
        if (ebayOrders[i]['order_id'] == ebayOrderId) {
            ebayOrders[i]['tracking'] = trackingInfo;
            return ebayOrders[i];
        } else {
            continue;
        }
    }
    return false;
}

function setAmazonOrderIdByTabId(tabId, amazonOrderId, map) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, map);
    if (ebayOrderId == null) {
        return false;
    }

    return setAmazonOrderIdByEbayOrderId(ebayOrderId, amazonOrderId);
}

function setOrderTrackingByTabId(tabId, trackingInfo, map) {
    var ebayOrderId = findEbayOrderIdByTabId(tabId, map);
    if (ebayOrderId == null) {
        return false;
    }

    return setOrderTrackingByEbayOrderId(ebayOrderId, trackingInfo);
}

function findCurrentUrlByTabId(tabId, map) {
    for (var i = 0; i < map.length; i++) {
        if (map[i]['tabId'] == tabId) {
            return map[i]['currentUrl'];
        } else {
            continue;
        }
    }
    return null

}

function updateCurrentUrlByTabId(tabId, currentUrl, map) {
    for (var i = 0; i < map.length; i++) {
        if (map[i]['tabId'] == tabId) {
            map[i]['currentUrl'] = currentUrl;
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

function proceedAmazonOrder(tab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateCurrentUrlByTabId(tab.id, tabChangeInfo.url, tabsAmazonOrder);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        var ebayOrder = findEbayOrderByTabId(tab.id, ebayOrders, tabsAmazonOrder);
        if (ebayOrder == null) {
            return false;
        }

        chrome.tabs.sendMessage(
            tab.id,
            {
                app: 'automationJ',
                task: 'proceedAmazonItemOrder',
                urlOnAddressBar: findCurrentUrlByTabId(tab.id, tabsAmazonOrder),
                order: ebayOrder,
                '_currentTab': tab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response)
            }
        );
    }
}

function proceedAmazonOrderTracking(tab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateCurrentUrlByTabId(tab.id, tabChangeInfo.url, tabsAmazonOrderTracking);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        chrome.tabs.sendMessage(
            tab.id,
            {
                app: 'automationJ',
                task: 'proceedAmazonOrderTracking',
                urlOnAddressBar: findCurrentUrlByTabId(tab.id, tabsAmazonOrderTracking),
                '_currentTab': tab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response)
            }
        );
    }
}

function proceedLeaveFeedback(tab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateCurrentUrlByTabId(tab.id, tabChangeInfo.url, tabsFeedback);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        chrome.tabs.sendMessage(
            tab.id,
            {
                app: 'automationJ',
                task: 'proceedLeaveFeedback',
                urlOnAddressBar: findCurrentUrlByTabId(tab.id, tabsFeedback),
                '_currentTab': tab,
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
        url: AUTOMATIONJ_SERVER_URL + '/orders',
    }, function(tab) {
        tabAutomationJ = tab;
    });
});

// on tab updated
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (isAutomationJTab(tab)) { // automationj tab
        if (changeInfo.status == "complete") {
            if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/orders\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/orders.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/trackings\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/trackings.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/feedbacks\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/feedbacks.js' });
            }
        }
    } else if (isTabRegistered(tabsAmazonOrder, tab)) { // amazon order tab
        proceedAmazonOrder(tab, changeInfo);
    } else if (isTabRegistered(tabsAmazonOrderTracking, tab)) { // amazon order tracking tab
        proceedAmazonOrderTracking(tab, changeInfo);
    } else if (isTabRegistered(tabsFeedback, tab)) { // feedback tab
        proceedLeaveFeedback(tab, changeInfo);
    }
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
                url: AMAZON_ITEM_URL_PRIFIX + asins[0],
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonOrder.push({
                    'ebayOrderId': ebayOrder.order_id,
                    'tabId': tab.id,
                    'currentUrl': tab.url
                });
                sendResponse({ success: true,
                    amazonItemOrderingTab: tab,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
            });
            break;

        case 'trackAmazonOrder':
            chrome.tabs.create({
                url: AMAZON_ORDER_DETAIL_URL_PRIFIX + message.amazonOrderId + '&aj=tracking',
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonOrderTracking.push({
                    'ebayOrderId': message.ebayOrderId,
                    'tabId': tab.id,
                    'currentUrl': tab.url
                });
                sendResponse({ success: true, 
                    amazonOrderTrackingTab: tab,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
            });
            break;

        case 'leaveFeedback':
            chrome.tabs.create({
                url: AMAZON_ORDER_DETAIL_URL_PRIFIX + message.amazonOrderId + '&aj=feedback',
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsFeedback.push({
                    'ebayOrderId': message.ebayOrderId,
                    'tabId': tab.id,
                    'currentUrl': tab.url
                });
                sendResponse({ success: true, 
                    amazonOrderTrackingTab: tab,
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
            var order = setAmazonOrderIdByTabId(sender.tab.id, message.amazonOrderId, tabsAmazonOrder)

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

        case 'storeOrderTrackingInfo':
            if (!message.carrier || !message.trackingNumber) {
                var order = findEbayOrderByTabId(sender.tab.id, ebayOrders, tabsAmazonOrderTracking);
                sendResponse({ success: true,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
                chrome.tabs.sendMessage(
                    tabAutomationJ.id,
                    {
                        app: 'automationJ',
                        task: 'failedOrderTracking',
                        ebayOrderId: order.order_id,
                        amazonOrderId: order.amazon_order.order_id,
                        carrier: null,
                        trackingNumber: null,
                        '_currentTab': tabAutomationJ,
                        '_errorMessage': null,
                    }, function(response) {
                        console.log(response)
                    }
                );
            } else {
                var trackingInfo = {
                    'carrier': message.carrier,
                    'tracking_number': message.trackingNumber
                };

                var order = setOrderTrackingByTabId(sender.tab.id,
                    trackingInfo,
                    tabsAmazonOrderTracking);

                $.ajax({
                    url: API_SERVER_URL + '/orders/trackings/',
                    method: 'POST',
                    dataType: 'json',
                    data: {
                        'ebay_order_id': order.order_id,
                        'carrier': message.carrier,
                        'tracking_number': message.trackingNumber
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
                                    task: 'succeededOrderTracking',
                                    ebayOrderId: order.order_id,
                                    amazonOrderId: order.amazon_order.order_id,
                                    carrier: message.carrier,
                                    trackingNumber: message.trackingNumber,
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
            }
            break;

        case 'flagDelivered':
            var order = findEbayOrderByTabId(sender.tab.id, ebayOrders, tabsFeedback);
            if (!message.isDelivered) {
                sendResponse({ success: true,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
                chrome.tabs.sendMessage(
                    tabAutomationJ.id,
                    {
                        app: 'automationJ',
                        task: 'failedFeedbackLeaving',
                        ebayOrderId: order.order_id,
                        amazonOrderId: order.amazon_order.order_id,
                        '_currentTab': tabAutomationJ,
                        '_errorMessage': null,
                    }, function(response) {
                        console.log(response)
                    }
                );
            } else {
                $.ajax({
                    url: API_SERVER_URL + '/orders/' + order.order_id,
                    method: 'PUT',
                    dataType: 'json',
                    data: {
                        'feedback_left': true,
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
                                    task: 'succeededFeedbackLeaving',
                                    ebayOrderId: order.order_id,
                                    amazonOrderId: order.amazon_order.order_id,
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



