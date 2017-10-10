var _amazon_account_id = 14; // kylelawn.196070@yandex.com
var _cc = '5584790000125244'; // MC BUSINESS COR
var _cc_position = '0';

// var _amazon_account_id = 15; // chrishamoto.197172@yandex.com
// var _cc = '5584790000127687'; // MC BUSINESS EMP
// var _cc_position = '0';

// var _amazon_account_id = 16; // tomhashimoto.1969@yandex.com
// var _cc = '4085860004814411'; // VISA PERSONAL
// var _cc_position = '0';

// var _amazon_account_id = 17; // mattmashiro.1963@gmail.com
// var _cc = '4085860004814411'; // VISA PERSONAL
// var _cc_position = '0';

// var _amazon_account_id = 18; // nelsonfeng4934@gmail.com
// var _cc = '5584790000125244'; // MC BUSINESS COR
// var _cc_position = '0';


var API_SERVER_URL = 'http://45.79.183.134:8091/api';
var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';
var AMAZON_ITEM_VARIATION_URL_POSTFIX = '/?th=1&psc=1';
var AMAZON_ORDER_DETAIL_URL_PRIFIX = 'https://www.amazon.com/gp/aw/ya/?ie=UTF8&ac=od&ii=&noi=&of=&oi=&oid=';
// var AMAZON_ORDER_SEARCH_RESULT_URL_PRIFIX = 'https://www.amazon.com/gp/your-account/order-history/?search=';

var tabAutomationJ = null;
var tabsAmazonOrder = [];
var tabsAmazonOrderTracking = [];
var tabsFeedback = [];
var tabsAmazonOrderReturnRequesting = [];

var ebayOrders = [];
var ebayOrderReturns = [];
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

function updateAndGetShoppingcartAddedAsinsByTabId(tabId) {
    // map = tabsAmazonOrder
    for (var i = 0; i < tabsAmazonOrder.length; i++) {
        if (tabsAmazonOrder[i]['tabId'] == tabId) {
            tabsAmazonOrder[i]['shoppingcartAddedAsins'].push(tabsAmazonOrder[i]['currentAsin'])
            return tabsAmazonOrder[i]['shoppingcartAddedAsins'];
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

function setAmazonOrderReturnIntoEbayOrderReturnByTabId(tabId, amazonOrderReturn, map) {
    var eorId = null;
    var eor = findEbayOrderReturnByTabId(tabId, map);
    if (eor == null) {
        return false;
    } else {
        eorId = eor['return_id'];
    }

    // ebayOrderReturns: global variable
    for (var i = 0; i < ebayOrderReturns.length; i++) {
        if (ebayOrderReturns[i]['order_id'] == eorId) {
            ebayOrderReturns[i]['amazon_order_return'] = amazonOrderReturn;
            return true;
        } else {
            continue;
        }
    }
    return false;
}

function getCurrentAsinByTabId(tabId) {
    // map = tabsAmazonOrder
    for (var i = 0; i < tabsAmazonOrder.length; i++) {
        if (tabsAmazonOrder[i]['tabId'] == tabId) {
            if (typeof tabsAmazonOrder[i]['currentAsin'] != 'undefined') {
                return tabsAmazonOrder[i]['currentAsin'];
            } else {
                return null;
            }
        } else {
            continue;
        }
    }
    return null;
}

function setCurrentAsinIntotabsAmazonOrderByTabId(tabId, asin) {
    // map = tabsAmazonOrder
    for (var i = 0; i < tabsAmazonOrder.length; i++) {
        if (tabsAmazonOrder[i]['tabId'] == tabId) {
            tabsAmazonOrder[i]['currentAsin'] = asin;
            return true;
        } else {
            continue;
        }
    }
    return false;
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

function findEbayOrderReturnByTabId(tabId, map) {
    // global variable: ebayOrderReturns
    for (var i = 0; i < map.length; i++) {
        if (map[i]['tabId'] == tabId) {
            for (var j = 0; j < ebayOrderReturns.length; j++) {
                if (map[i]['ebayOrderReturnId'] == ebayOrderReturns[j]['return_id']) {
                    return ebayOrderReturns[j];
                } else {
                    continue;
                }
            }
        } else {
            continue;
        }
    }
    return null;
}


function getAmazonItems(ebayOrder) {
    var asins = []
    var items = ebayOrder['items'];
    var is_variation = false;
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++) {
            if (typeof items[i].sku != 'undefined') {
                is_variation = (typeof items[i].is_variation != 'undefined' && items[i].is_variation == true) ? true : false;
                asins.push({
                    'sku': items[i].sku,
                    'is_variation': is_variation,
                });
            }
        }
    }
    return asins;
}

function getNextOrderingAmazonItem(ebayOrder, shoppingcartAddedAsins) {
    var a_items = getAmazonItems(ebayOrder);
    if (shoppingcartAddedAsins.length == 0) {
        return a_items[0];
    }
    for (var i = 0; i < a_items.length; i++) {
        if ($.inArray(a_items[i].sku, shoppingcartAddedAsins) < 0) {
            return a_items[i]
        }
    }
    return null
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
                cc: _cc,
                cc_position: _cc_position,
                '_currentTab': tab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response);
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
                console.log(response);
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
                console.log(response);
            }
        );
    }
}

function proceedAmazonOrderReturnRequesting(tab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateCurrentUrlByTabId(tab.id, tabChangeInfo.url, tabsAmazonOrderReturnRequesting);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        var ebayOrderReturn = findEbayOrderReturnByTabId(tab.id, tabsAmazonOrderReturnRequesting);
        chrome.tabs.sendMessage(
            tab.id,
            {
                app: 'automationJ',
                task: 'proceedAmazonOrderReturnRequesting',
                urlOnAddressBar: findCurrentUrlByTabId(tab.id, tabsAmazonOrderReturnRequesting),
                amazonOrderId: ebayOrderReturn['amazon_order']['order_id'],
                asin: ebayOrderReturn['ebay_order_item']['sku'],
                ebayOrderReturnId: ebayOrderReturn['return_id'],
                quantity: ebayOrderReturn['ebay_order_item']['quantity'],
                '_currentTab': tab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response);
            }
        );
    }

}

function calculateEbayFinalFee(ebayOrderTotal) {
    return (ebayOrderTotal * 0.0915).toFixed(2);
}

function calculatePayPalFee(ebayOrderTotal) {
    return (ebayOrderTotal * 0.037 + 0.30).toFixed(2);
}

function calculateMargin(ebayOrderTotal, amazonOrderTotal) {
    return (ebayOrderTotal.toFixed(2) - amazonOrderTotal.toFixed(2) - calculateEbayFinalFee(ebayOrderTotal) - calculatePayPalFee(ebayOrderTotal)).toFixed(2);
}

// onclick extension icon
chrome.browserAction.onClicked.addListener(function(activeTab) {
    chrome.tabs.create({
        url: AUTOMATIONJ_SERVER_URL + '/orders/all',
    }, function(tab) {
        tabAutomationJ = tab;
    });
});

// on tab updated
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (isAutomationJTab(tab)) { // automationj tab
        if (changeInfo.status == "complete") {
            if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/orders\/all\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/orders.js' },
                    function() {
                        chrome.tabs.sendMessage(
                            tab.id,
                            {
                                app: 'automationJ',
                                task: 'initOrders',
                                order_condition: 'any',
                                per_page: 200,
                                '_currentTab': tab,
                                '_errorMessage': null,
                            }, function(response) {
                                console.log(response);
                            }
                        );
                    });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/orders\/unsourced\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/orders.js' },
                    function() {
                        chrome.tabs.sendMessage(
                            tab.id,
                            {
                                app: 'automationJ',
                                task: 'initOrders',
                                order_condition: 'unsourced',
                                per_page: 1000,
                                '_currentTab': tab,
                                '_errorMessage': null,
                            }, function(response) {
                                console.log(response);
                            }
                        );
                    });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/trackings\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/trackings.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/feedbacks\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/feedbacks.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/bestsellers\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/bestsellers.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/performances\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/performances.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/reports\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/reports.js' });
            } else if (tab.url.match(/^http:\/\/45\.79\.183\.134:8092\/returns\//)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/returns.js' });
            }
        }
    } else if (isTabRegistered(tabsAmazonOrder, tab)) { // amazon order tab
        proceedAmazonOrder(tab, changeInfo);
    } else if (isTabRegistered(tabsAmazonOrderTracking, tab)) { // amazon order tracking tab
        proceedAmazonOrderTracking(tab, changeInfo);
    } else if (isTabRegistered(tabsFeedback, tab)) { // feedback tab
        proceedLeaveFeedback(tab, changeInfo);
    } else if (isTabRegistered(tabsAmazonOrderReturnRequesting, tab)) { // feedback tab
        proceedAmazonOrderReturnRequesting(tab, changeInfo);
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
                url: API_SERVER_URL + '/orders/' + message.orderCondition + '/' + (parseInt(message.lastOrderRecordNumber) - 1) + '/' + message.perPage,
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    if (message.lastOrderRecordNumber < 0) {
                        ebayOrders = response.data;
                    } else {
                        Array.prototype.push.apply(ebayOrders, response.data);
                    }
                    sendResponse({ success: true, orders: response.data,
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
            var shoppingcartAddedAsins = [];
            var a_item = getNextOrderingAmazonItem(ebayOrder, shoppingcartAddedAsins);
            var amazon_url = AMAZON_ITEM_URL_PRIFIX + a_item['sku'] + AMAZON_ITEM_VARIATION_URL_POSTFIX;
            chrome.tabs.create({
                url: amazon_url,
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonOrder.push({
                    'ebayOrderId': ebayOrder.order_id,
                    'tabId': tab.id,
                    'currentUrl': tab.url,
                    'currentAsin': a_item['sku'],
                    'shoppingcartAddedAsins': shoppingcartAddedAsins
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
                    leaveFeedbackTab: tab,
                    '_currentTab': sender.tab,
                    '_errorMessage': null
                });
            });
            break;

        case 'requestAmazonOrderReturn':
            chrome.tabs.create({
                url: AMAZON_ORDER_DETAIL_URL_PRIFIX + message.amazonOrderId + '&aj=returnrequesting',
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonOrderReturnRequesting.push({
                    'ebayOrderReturnId': message.ebayOrderReturnId,
                    'tabId': tab.id,
                    'currentUrl': tab.url
                });
                sendResponse({ success: true,
                    amazonOrderReturnRequestingTab: tab,
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
            var order = setAmazonOrderIdByTabId(sender.tab.id, message.amazonOrderId, tabsAmazonOrder);

            var a_items = getAmazonItems(order);

            $.ajax({
                url: API_SERVER_URL + '/orders/amazon_orders/',
                method: 'POST',
                dataType: 'json',
                data: {
                    'amazon_account_id': _amazon_account_id,
                    'amazon_order_id': order.amazon_order.order_id,
                    'ebay_order_id': order.order_id,
                    'items': JSON.stringify(a_items),
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
                                console.log(response);
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
                        console.log(response);
                        chrome.tabs.remove(sender.tab.id);
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
                                    console.log(response);
                                    chrome.tabs.remove(sender.tab.id);
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
                        console.log(response);
                        chrome.tabs.remove(sender.tab.id);
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
                                    console.log(response);
                                    chrome.tabs.remove(sender.tab.id);
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

        case 'fetchItemPerformanceResults':
            $.ajax({
                url: API_SERVER_URL + '/items/performances/' + message.days,
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    performances = response.data;
                    sendResponse({ success: true, performances: performances,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                },
                error: function() {
                    performances = []
                    sendResponse({ success: false, performances: performances,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
            break;

        case 'fetchReports':
            $.ajax({
                url: API_SERVER_URL + '/orders/reports/' + message.durationtype,
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    reports = response.data;
                    sendResponse({ success: true, reports: reports,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                },
                error: function() {
                    reports = []
                    sendResponse({ success: false, reports: reports,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
            break;

        case 'fetchBestSellers':
            $.ajax({
                url: API_SERVER_URL + '/items/bestsellers/' + message.days,
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    bestsellers = response.data;
                    sendResponse({ success: true, bestsellers: bestsellers,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                },
                error: function() {
                    bestsellers = []
                    sendResponse({ success: false, bestsellers: bestsellers,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
            break;

        case 'hasMoreAmazonItemToOrder':
            var ebayOrder = findEbayOrderByTabId(sender.tab.id, ebayOrders, tabsAmazonOrder);
            var shoppingcartAddedAsins = updateAndGetShoppingcartAddedAsinsByTabId(sender.tab.id);
            var a_item = getNextOrderingAmazonItem(ebayOrder, shoppingcartAddedAsins);
            var nextAmazonItemUrl = null;
            if (a_item != null) {
                nextAmazonItemUrl = AMAZON_ITEM_URL_PRIFIX + a_item['sku'] + AMAZON_ITEM_VARIATION_URL_POSTFIX;
                setCurrentAsinIntotabsAmazonOrderByTabId(sender.tab.id, a_item['sku']);
            }
            sendResponse({ success: true,
                nextAmazonItemUrl: nextAmazonItemUrl,
                margin: calculateMargin(ebayOrder.total_price, (parseFloat(message.price) * 1.07)),
                '_currentTab': sender.tab,
                '_errorMessage': null
            });
            break;

        case 'validateAmazonItem':
            var _isValid = false;
            var _currentAsin = getCurrentAsinByTabId(sender.tab.id);
            if (_currentAsin && message.asin == _currentAsin) {
                _isValid = true;
            }
            sendResponse({ success: true,
                isValid: _isValid,
                '_currentTab': sender.tab,
                '_errorMessage': null
            });
            break;

        case 'fetchReturns':
            $.ajax({
                url: API_SERVER_URL + '/returns/' + (parseInt(message.lastReturnId) - 1) + '/' + message.perPage,
                dataType: "json",
                success: function(response, textStatus, jqXHR) {
                    if (message.lastReturnId < 0) {
                        ebayOrderReturns = response.data;
                    } else {
                        Array.prototype.push.apply(ebayOrderReturns, response.data);
                    }
                    sendResponse({ success: true, returns: response.data,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                },
                error: function() {
                    ebayOrderReturns = [];
                    sendResponse({ success: false, returns: ebayOrderReturns,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });
                }
            });
            break;

        case 'storeAmazonOrderReturn':
            var amazonOrderReturn = {
                'amazon_account_id': _amazon_account_id,
                'order_id': message.amazonOrderId,
                'asin': message.asin,
                'return_id': message.amazonOrderReturnId,
                'ebay_return_id': message.ebayOrderReturnId,
                'quantity': message.quantity,
                'rma': message.rma,
                'refunded_amount': message.refundedAmount,
                'refunded_date': message.refundedDate,
                'returned_date': message.returnedDate
            };

            $.ajax({
                url: API_SERVER_URL + '/returns/amazon_returns/',
                method: 'POST',
                dataType: 'json',
                data: amazonOrderReturn,
                success: function(response, textStatus, jqXHR) {
                    var result = setAmazonOrderReturnIntoEbayOrderReturnByTabId(sender.tab.id, amazonOrderReturn, tabsAmazonOrderReturnRequesting);
                    sendResponse({ success: result,
                        '_currentTab': sender.tab,
                        '_errorMessage': null
                    });

                    if (tabAutomationJ != null) {
                        console.log('storeAmazonOrderReturn', response);
                        chrome.tabs.sendMessage(
                            tabAutomationJ.id,
                            {
                                app: 'automationJ',
                                task: 'succeededAmazonOrderReturnRequesting',
                                ebayOrderReturnId: amazonOrderReturn.ebay_return_id,
                                amazonOrderReturnId: amazonOrderReturn.return_id,
                                amazonOrderId: amazonOrderReturn.order_id,
                                asin: amazonOrderReturn.asin,
                                amazonOrderReturnStatus: response.data.status,
                                amazonOrderReturnRefundedAmount: response.data.refunded_amount,
                                trackingNumber: response.data.tracking_number,
                                rma: response.data.rma,
                                '_currentTab': tabAutomationJ,
                                '_errorMessage': null,
                            }, function(response) {
                                console.log(response);
                                chrome.tabs.remove(sender.tab.id);
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

        case 'closeTabWithError':
            chrome.tabs.sendMessage(
                tabAutomationJ.id,
                {
                    app: 'automationJ',
                    task: 'tabClosedWithError',
                    '_currentTab': tabAutomationJ,
                    '_errorMessage': message.errorMessage,
                }, function(response) {
                    console.log(response);
                    chrome.tabs.remove(sender.tab.id);
                }
            );
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



