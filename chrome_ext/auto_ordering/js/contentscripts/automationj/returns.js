var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var EBAY_ITEM_URL_PRIFIX = 'https://www.ebay.com/itm/';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';
var AMAZON_ITEM_VARIATION_URL_POSTFIX = '/?th=1&psc=1';
var AMAZON_RETURN_LABEL_URL_PRIFIX = 'https://www.amazon.com/returns/label/';
var AMAZON_RETURN_LABEL_URL_POSTFIX = '?printerFriendly=1';

var NAVBAR = '<nav class="navbar navbar-default navbar-fixed-top"> \
    <div class="container-fluid"> \
        <!-- Brand and toggle get grouped for better mobile display --> \
        <div class="navbar-header"> \
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false"> \
                <span class="sr-only">Toggle navigation</span> \
                <span class="icon-bar"></span> \
                <span class="icon-bar"></span> \
                <span class="icon-bar"></span> \
            </button> \
            <a class="navbar-brand" href="' + AUTOMATIONJ_SERVER_URL + '">AutomationJ</a> \
        </div> \
        <!-- Collect the nav links, forms, and other content for toggling --> \
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1"> \
            <ul class="nav navbar-nav"> \
                <li class="dropdown"> \
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Orders <span class="caret"></span></a> \
                    <ul class="dropdown-menu"> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/all">All orders</a></li> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/unsourced">Unsourced orders</a></li> \
                    </ul> \
                </li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/returns">Returns</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales report</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
            </ul> \
            <div class="navbar-form navbar-left"> \
                <div class="form-group"> \
                    <input type="text" class="form-control" id="selected-amazon-account" placeholder="Amazon Account..."> \
                </div> \
                <button type="button" class="btn btn-info disabled" id="track-all-button">Track All Orders</button> \
            </div> \
        </div><!-- /.navbar-collapse --> \
    </div> \
</nav>';

var MAIN_CONTAINER = '<div id="main-container" class="container-fluid"></div>';

var REFRESH_TABLE_BUTTON = '<div class="pull-right" style="padding:20px 0px;"><button id="refresh-table-button" class="btn btn-success">Refresh</button></div>'

var RETURN_TABLE_BODY_TEMPLATE = '\
<table id="main-table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Return ID / eBay item / Buyer username (email)</th>\
            <th>Amazon item / Amazon order ID / Account</th>\
            <th>eBay return state / Status / Amazon status</th>\
            <th>eBay refund / Amazon refund</th>\
            <th>Shipping label</th>\
            <th>Action</th>\
            <th>Buyer requested at</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
    <tfoot>\
        <tr>\
            <td colspan="7">\
                <button id="load-more-returns-button" class="btn btn-success" style="width: 100%">Load More Returns</button>\
            </td>\
        </tr>\
    </tfoot>\
</table>';

var RETURN_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="return-individual"><b><%= ret.return_id %></b><br><small><%= ret.item_id %></small> <a href="<%= ebay_item_url_prefix+ret.item_id %>" target="_blank"><small>link</small></a><br><a href="javascript:void(0);" title="<%= ret.ebay_order.buyer_email %>"><%= ret.buyer_username %></a></td> \
    <td class="return-individual"><small><%= ret.ebay_order_item.sku %></small> <a href="<%= amz_item_url_prefix+ret.ebay_order_item.sku+amz_item_v_url_postfix %>" target="_blank"><small>link</small></a><br><%= ret.amazon_order_id %><br><small class="related-amazon-account"><%= ret.related_amazon_account %></small></td> \
    <td class="return-individual"><%= ret.state %><br><%= ret.status %><br><%= ret.amazon_return_status %></td> \
    <td class="return-individual"><%= ret.ebay_refund %><br><%= ret.amazon_refund %></td> \
    <td class="return-individual"><%= ret.amazon_shipping_label %></td> \
    <td class="return-individual"><%= ret.amazon_return_action %></td> \
    <td class="return-individual"><%= ret.creation_time %></td> \
</tr>';

$('body').css({ "padding-top": "70px" });

function initDom() {
    $('body').append(NAVBAR);
    $('body').append(MAIN_CONTAINER);
    $('body #main-container').append(REFRESH_TABLE_BUTTON);
    $('body #main-container').append(RETURN_TABLE_BODY_TEMPLATE);
}

function getMainTableBody() {
    return $('body').find('#main-table tbody');
}
function getMainTable() {
    return $('body').find('#main-table');
}

var _lastReturnId = -1;
var _loadMoreReturns = function(response) {
    console.log('response', response)
    if (response.success != true) {
        return false;
    }
    var returns = response.returns;
    if (returns.length > 0) {
        var $main_table_body = getMainTableBody();
        for (var i = 0; i < returns.length; i++) {
            returns[i]['amazon_order_id'] = '-';
            returns[i]['related_amazon_account'] = '-';
            returns[i]['amazon_return_status'] = '<span class="amazon-return-status-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-<span>';
            returns[i]['amazon_shipping_label'] = '<div class="amazon-shipping-label-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-</div>';
            returns[i]['amazon_return_action'] = '-';
            returns[i]['ebay_refund'] = '<strong>-</strong>';
            returns[i]['amazon_refund'] = '<strong class="amazon-refunded-amount-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-<strong>';
            // amazon_order
            if (returns[i].amazon_order != null) {
                // amazon_order_id
                amazon_order_id = returns[i].amazon_order.order_id;
                returns[i]['amazon_order_id'] = '<span class="return-individual-amazon-order-id" data-ebayorderreturnid="' + returns[i].return_id + '" data-amazonorderid="' + amazon_order_id + '">' + amazon_order_id + '</span>';
                // related amazon account
                returns[i]['related_amazon_account'] = returns[i].amazon_order.amazon_account_email;
                // amazon_return_status
                if (returns[i].amazon_order_return != null) {
                    returns[i]['amazon_return_status'] = '<span class="amazon-return-status-individual" data-ebayorderreturnid="' + returns[i].return_id + '">' + returns[i].amazon_order_return.status + '<span>';
                }
                // amazon_shipping_label
                if (returns[i].amazon_order_return == null) {
                    returns[i]['amazon_shipping_label'] = '<div class="amazon-shipping-label-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-</div>';
                } else {
                    returns[i]['amazon_shipping_label'] ='<div class="amazon-shipping-label-individual" data-ebayorderreturnid="' + returns[i].return_id + '">' + AMAZON_RETURN_LABEL_URL_PRIFIX + returns[i].amazon_order_return.return_id + AMAZON_RETURN_LABEL_URL_POSTFIX + ' <a href="' + AMAZON_RETURN_LABEL_URL_PRIFIX + returns[i].amazon_order_return.return_id + AMAZON_RETURN_LABEL_URL_POSTFIX + '" target="_blank">link</a><br>' + returns[i].amazon_order_return.tracking_number + '<br>' + returns[i].amazon_order_return.rma + '</div>';
                }
                // amazon_return_action
                returns[i]['amazon_return_action'] = '<a href="javascript:void(0)" class="btn btn-info return-request-individual-button" data-ebayorderreturnid="' + returns[i].return_id + '" data-amazonorderid="' + amazon_order_id + '" data-asin="' + returns[i].ebay_order_item.sku + '">Update Amazon Return</a>'
                // ebay_refund
                if (returns[i].act_refund_amount != null) {
                    returns[i]['ebay_refund'] = '<strong class="text-danger">$' + returns[i].act_refund_amount + '</strong>';
                }
                // ebay_refund
                if (returns[i].amazon_order_return != null && returns[i].amazon_order_return.refunded_amount != null) {
                    returns[i]['amazon_refund'] = '<strong class="amazon-refunded-amount-individual text-info" data-ebayorderreturnid="' + returns[i].return_id + '">$' + returns[i].amazon_order_return.refunded_amount + '</strong>';
                }
            }
            $main_table_body.append(_.template(RETURN_TABLE_ROW_TEMPLATE)({ ret: returns[i], ebay_item_url_prefix: EBAY_ITEM_URL_PRIFIX, amz_item_url_prefix: AMAZON_ITEM_URL_PRIFIX, amz_item_v_url_postfix: AMAZON_ITEM_VARIATION_URL_POSTFIX }));
            _lastReturnId = returns[i].return_id;
        }
    }
    $('#refresh-table-button').removeClass('disabled').text('Refresh');
    $('#load-more-returns-button').removeClass('disabled').text('Load More Returns');
};

function refreshReturnTable() {
    var $main_table_body = getMainTableBody();
    $main_table_body.empty();
    loadMoreReturns(-1);
}

function loadMoreReturns(lastReturnId) {
    $('#refresh-table-button').addClass('disabled').text('Loading...');
    $('#load-more-returns-button').addClass('disabled').text('Loading...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchReturns",
        perPage: 200,
        lastReturnId: lastReturnId,
    }, _loadMoreReturns);
}

function updateAmazonOrderReturn(ebayOrderReturnId, amazonOrderReturnId, amazonOrderId, asin, amazonStatus, amazonRefundedAmount, trackingNumber, rma) {
    // amazon shipping label
    $('.amazon-shipping-label-individual[data-ebayorderreturnid="' + ebayOrderReturnId + '"]').html(AMAZON_RETURN_LABEL_URL_PRIFIX + amazonOrderReturnId + AMAZON_RETURN_LABEL_URL_POSTFIX + ' <a href="' + AMAZON_RETURN_LABEL_URL_PRIFIX + amazonOrderReturnId + AMAZON_RETURN_LABEL_URL_POSTFIX + '" target="_blank">link</a><br>' + trackingNumber + '<br>' + rma);
    // amazon return status
    $('.amazon-return-status-individual[data-ebayorderreturnid="' + ebayOrderReturnId + '"]').html(amazonStatus);
    // amazon refunded amount
    if (amazonRefundedAmount) {
        $('.amazon-refunded-amount-individual[data-ebayorderreturnid="' + ebayOrderReturnId + '"]').addClass('text-info').html('$' + amazonRefundedAmount);
    }

    // amazon return button
    $('.return-request-individual-button[data-ebayorderreturnid="' + ebayOrderReturnId + '"]').removeClass('disabled').text('Update Amazon Return');
}

var RETURN_QUEUE = [];

function requestNextAmazonOrderReturn() {
    var data = RETURN_QUEUE.pop(); // pop from the last: LIFO
    if (typeof data == 'undefined') {
        return false;
    }
    $('.return-request-individual-button[data-ebayorderreturnid="' + data.ebayOrderReturnId + '"][data-amazonorderid="' + data.amazonOrderId + '"][data-asin="' + data.asin + '"]').addClass('disabled').text('Proceeding...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "requestAmazonOrderReturn",
        ebayOrderReturnId: data.ebayOrderReturnId,
        amazonOrderId: data.amazonOrderId,
        asin: data.asin,
    }, function(response) {
        console.log('requestAmazonOrderReturn response', response);
    });
    return false;
}

// refresh/initialize order table
initDom();
refreshReturnTable();

var $main_table = getMainTable();
var $main_table_body = getMainTableBody();
$('body').on('click', '#refresh-table-button', function() {
    refreshReturnTable();
});
// $('body').on('click', '#track-all-button', function(e) {
//     var amazon_account = $('#selected-amazon-account').val();
//     if (amazon_account == '' || amazon_account == null) {
//         alert('please enter Amazon Account');
//     } else {
//         RETURN_QUEUE = [] // clear existing queue
//         $main_table_body.find('tr').each(function(e) {
//             if ($.trim($(this).find('.related-amazon-account').text()) == $.trim(amazon_account)) {
//                 var $trackNowButton = $(this).find('.return-request-individual-button');
//                 if ($trackNowButton.length && !$trackNowButton.hasClass('disabled')) {
//                     RETURN_QUEUE.push({
//                         ebayOrderReturnId: $this.attr('data-ebayorderreturnid'),
//                         amazonOrderId: $this.attr('data-amazonorderid'),
//                         asin: $this.attr('data-asin')
//                     });
//                 }
//             }
//         });
//         requestNextAmazonOrderReturn();
//     }
// });
$main_table_body.on('click', '.return-request-individual-button', function(e) {
    var $this = $(this);
    RETURN_QUEUE.push({
        ebayOrderReturnId: $this.attr('data-ebayorderreturnid'),
        amazonOrderId: $this.attr('data-amazonorderid'),
        asin: $this.attr('data-asin')
    });
    requestNextAmazonOrderReturn();
});
$main_table.on('click', '#load-more-returns-button', function(e){
    loadMoreReturns(_lastReturnId);
});


// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'succeededAmazonOrderReturnRequesting':
            updateAmazonOrderReturn(message.ebayOrderReturnId, message.amazonOrderReturnId, message.amazonOrderId, message.asin, message.amazonOrderReturnStatus, message.amazonOrderReturnRefundedAmount, message.trackingNumber, message.rma);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
