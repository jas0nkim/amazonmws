// var API_SERVER_URL = 'http://172.104.12.103:8091/api';
var AUTOMATIONJ_SERVER_URL = 'http://affiliationship.com';

var tabAutomationJ = null;
var tabsAmazonLanding = [];

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


function proceedAmazonLanding(tab, tabChangeInfo) {
    if (typeof tabChangeInfo.url != 'undefined') {
        updateCurrentUrlByTabId(tab.id, tabChangeInfo.url, tabsAmazonLanding);
    }

    if (typeof tabChangeInfo.status != 'undefined' && tabChangeInfo.status == 'complete') {
        chrome.tabs.sendMessage(
            tab.id,
            {
                app: 'automationJ-affiliating',
                task: 'proceedAmazonLanding',
                urlOnAddressBar: findCurrentUrlByTabId(tab.id, tabsAmazonLanding),
                '_currentTab': tab,
                '_errorMessage': null,
            }, function(response) {
                console.log(response);
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
    if (isAutomationJTab(tab)) { // automationJ-affiliating tab
        if (changeInfo.status == "complete") {
            if (tab.url.match(/^http:\/\/affiliationship\.com/)) {
                chrome.tabs.executeScript(tabId, { file: 'js/contentscripts/automationj/banners.js' });
            }
        }
    } else if (isTabRegistered(tabsAmazonLanding, tab)) { // amazon landing tab
        proceedAmazonLanding(tab, changeInfo);
    }
    return true;
});

// message listener
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {

    if (message.app == 'automationJ-affiliating') { switch(message.task) {
        // case 'validateAutomationJPage':
        //     if (tabAutomationJ == null) {
        //         sendResponse({ success: false,
        //             '_currentTab': sender.tab,
        //             '_errorMessage': 'Invalid AutomationJ Screen - not registered' 
        //         });
        //     } else {
        //         if (tabAutomationJ.id == sender.tab.id) {
        //             sendResponse({ success: true,
        //                 '_currentTab': sender.tab,
        //                 '_errorMessage': null
        //             });
        //         } else {
        //             sendResponse({ success: false,
        //                 '_currentTab': sender.tab,
        //                 '_errorMessage': 'Invalid AutomationJ Screen - Automation J already opened on another tab'
        //             });
        //         }
        //     }
        //     break;

        case 'openAmazonLanding':
            chrome.tabs.create({
                url: message.url + '&aj=affiliating',
                openerTabId: tabAutomationJ.id,
            }, function(tab) {
                tabsAmazonLanding.push({
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

        case 'closeAmazonLanding':
            chrome.tabs.sendMessage(
                tabAutomationJ.id,
                {
                    app: 'automationJ-affiliating',
                    task: 'succeededAmazonLanding',
                    '_currentTab': tabAutomationJ,
                    '_errorMessage': null,
                }, function(response) {
                    console.log(response);
                    chrome.tabs.remove(sender.tab.id);
                }
            );
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



