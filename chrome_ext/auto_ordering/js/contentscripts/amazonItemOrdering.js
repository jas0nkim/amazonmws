function clickAddToCartButton() {
    // click add to cart button
}

var automateAmazonOrder = function(response) {
    console.log('automateAmazonOrder response', response);
};

chrome.runtime.sendMessage({
    app: "automationJ",
    task: "getEbayOrder"
}, automateAmazonOrder);
