chrome.browserAction.onClicked.addListener(function(activeTab) {
    var url = "http://www.amazon.com";
    chrome.tabs.create({ url: url });
});