var automateAmazonOrderReturnRequest = function(message) {
    // console.log('AmazonOrderReturnRequest', message.urlOnAddressBar);
    // var page = validateCurrentPage(message.urlOnAddressBar);
};

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log('onMessage: message', message);
    if (message.app == 'automationJ') { switch(message.task) {
        case 'proceedAmazonOrderReturnRequesting':
            automateAmazonOrderReturnRequest(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
