function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function automateAmazonLandingClickThrough(message) {
    chrome.runtime.sendMessage({
        app: "automationJ-affiliating",
        task: "closeAmazonLanding"
    }, function(response) {
        console.log('storeAmazonOrderId response', response);
    });    
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log('onMessage: message', message);
    if (message.app == 'automationJ-affiliating') { switch(message.task) {
        case 'proceedAmazonLanding':
            var wait = getRandomInt(2000, 3000);
            setTimeout(function() {
                automateAmazonLandingClickThrough(message);
            }, wait);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
