function openAmazonLanding(link) {
    console.log(link);
    // alert(link);
    chrome.runtime.sendMessage({
        app: "automationJ-affiliating",
        task: "openAmazonLanding",
        url: link
    }, function(response) {
        console.log('openAmazonLanding response', response);
    });
    return false;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function getAffiliateLink() {
    var affiliateLink = null;
    var affiliationId = 'affiliationsh-20';

    if ($('a').length) {
        $('a').each(function() {
            if ($(this).attr('href').indexOf(affiliationId) !== -1) {
                affiliateLink = $(this).attr('href');
            }
        });
    } else if ($('area').length) {
        $('area').each(function() {
            if ($(this).attr('href').indexOf(affiliationId) !== -1) {
                affiliateLink = $(this).attr('href');
            }
        });
    }

    return affiliateLink;
}

var wait = getRandomInt(3000, 4000);
var affLink = getAffiliateLink();

console.log('affiliateLink', affLink);
setTimeout(function() {
    openAmazonLanding(affLink);
}, wait);

// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ-affiliating') { switch(message.task) {
        case 'succeededAmazonLanding':
            location.reload(); // refresh screen to reload iframe (banner)
            break;
        case 'failedAmazonOrdering':
            // updateOrderNowButton(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
