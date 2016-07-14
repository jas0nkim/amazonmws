var currentTab = null;
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    // since only one tab should be active and in the current window at once
    // the return variable should only have one entry
    currentTab = tabs[0];
});

chrome.tabs.sendMessage(currentTab.id, 
    { 
        'subject': 'automationJ.OrderAmazonItem'
    }, function(response) {
        // 1. get order data from response
        // 2. do automation
});