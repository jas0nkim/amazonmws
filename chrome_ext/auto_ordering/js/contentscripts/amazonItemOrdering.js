var automateAmazonOrder = function(response) {
    console.log(response);
};

chrome.runtime.sendMessage({
    app: "automationJ",
    task: "getEbayOrder"
}, automateAmazonOrder);
