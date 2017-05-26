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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Trackings & Feedbacks</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/returns">Returns</a></li> \
                <li class="dropdown"> \
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Reports <span class="caret"></span></a> \
                    <ul class="dropdown-menu"> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales</a></li> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/bestsellers">Best sellers</a></li> \
                    </ul> \
                </li> \
                <!-- \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
                --> \
            </ul> \
            <div class="navbar-form navbar-left"> \
                <div class="form-group"> \
                    <input type="text" class="form-control" id="selected-amazon-account" placeholder="Amazon Account..."> \
                </div> \
                <button type="button" class="btn btn-info" id="update-all-button">Update All Returns</button> \
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
            <th>Return ID - eBay item / Buyer username / Email</th>\
            <th>Amazon item / Amazon order ID / Account</th>\
            <th>eBay return status (state) / Amazon status / Amazon received</th>\
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
    <td class="return-individual"><b><%= ret.return_id %>-<%= ret.item_id %></b><br><a href="<%= ebay_item_url_prefix+ret.item_id %>" target="_blank"><small>ebay item link</small></a><br><%= ret.buyer_username %><br><small><%= ret.ebay_order.buyer_email %></small></td> \
    <td class="return-individual"><small><%= ret.ebay_order_item.sku %></small> <a href="<%= amz_item_url_prefix+ret.ebay_order_item.sku+amz_item_v_url_postfix %>" target="_blank"><small>link</small></a><br><%= ret.amazon_order_id %><br><small class="related-amazon-account"><%= ret.related_amazon_account %></small></td> \
    <td class="return-individual"><%= ret.ebay_return_status %><br><small>(<%= ret.state %>)</small><br><br><%= ret.amazon_return_status %><br><%= ret.amazon_received %></td> \
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
            returns[i]['ebay_return_status'] = returns[i].state;
            returns[i]['amazon_return_status'] = '<span class="amazon-return-status-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-<span>';
            returns[i]['amazon_received'] = '<span class="amazon-returned-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-<span>';
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
                // ebay_return_status
                if (returns[i].state == 'ITEM_DELIVERED') {
                    returns[i]['ebay_return_status'] = '<strong class="text-danger">' + returns[i].state + '</strong>';
                }
                // amazon_return_status
                if (returns[i].amazon_order_return != null) {
                    returns[i]['amazon_return_status'] = '<span class="amazon-return-status-individual" data-ebayorderreturnid="' + returns[i].return_id + '">' + returns[i].amazon_order_return.status + '<span>';
                }
                // amazon_received
                if (returns[i].amazon_order_return != null && returns[i].amazon_order_return.returned_date != null) {
                    returns[i]['amazon_received'] = '<span class="amazon-returned-individual text-warning" data-ebayorderreturnid="' + returns[i].return_id + '">Received on ' + returns[i].amazon_order_return.returned_date + '<span>';
                }
                // amazon_shipping_label
                if (returns[i].amazon_order_return == null) {
                    returns[i]['amazon_shipping_label'] = '<div class="amazon-shipping-label-individual" data-ebayorderreturnid="' + returns[i].return_id + '">-</div>';
                } else {
                    returns[i]['amazon_shipping_label'] ='<div class="amazon-shipping-label-individual" data-ebayorderreturnid="' + returns[i].return_id + '">' + AMAZON_RETURN_LABEL_URL_PRIFIX + returns[i].amazon_order_return.return_id + AMAZON_RETURN_LABEL_URL_POSTFIX + ' <a href="' + AMAZON_RETURN_LABEL_URL_PRIFIX + returns[i].amazon_order_return.return_id + AMAZON_RETURN_LABEL_URL_POSTFIX + '" target="_blank">link</a><br>' + returns[i].tracking_number + '<br>' + returns[i].amazon_order_return.rma + '</div>';
                }
                // amazon_return_action
                if (returns[i].amazon_order_return == null) {
                    if (returns[i].state == 'CLOSED' || returns[i].state == 'REPLACEMENT_CLOSED') {
                        returns[i]['amazon_return_action'] = '<span class="text-success">eBay Return Closed</span>'
                    } else {
                        returns[i]['amazon_return_action'] = '<a href="javascript:void(0)" class="btn btn-warning return-request-individual-button request-return-individual-button" data-ebayorderreturnid="' + returns[i].return_id + '" data-amazonorderid="' + amazon_order_id + '" data-asin="' + returns[i].ebay_order_item.sku + '">Request Amazon Return</a>';
                    }
                } else {
                    if (returns[i].amazon_order_return.status == 'REFUNDED' && returns[i].amazon_order_return.returned_date != null) {
                        returns[i]['amazon_return_action'] = '<span class="text-info">Returned and refunded from Amazon</span>'
                    } else {
                        returns[i]['amazon_return_action'] = '<a href="javascript:void(0)" class="btn btn-info return-request-individual-button update-return-individual-button" data-ebayorderreturnid="' + returns[i].return_id + '" data-amazonorderid="' + amazon_order_id + '" data-asin="' + returns[i].ebay_order_item.sku + '">Update Amazon Return</a>';
                    }
                }
                // ebay_refund
                if (returns[i].act_refund_amount != null) {
                    returns[i]['ebay_refund'] = '<strong class="text-danger">$' + returns[i].act_refund_amount.toFixed(2) + '</strong>';
                }
                // ebay_refund
                if (returns[i].amazon_order_return != null && returns[i].amazon_order_return.refunded_amount != null) {
                    returns[i]['amazon_refund'] = '<strong class="amazon-refunded-amount-individual text-info" data-ebayorderreturnid="' + returns[i].return_id + '">$' + returns[i].amazon_order_return.refunded_amount.toFixed(2) + '</strong>';
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
    $('.return-request-individual-button[data-ebayorderreturnid="' + ebayOrderReturnId + '"]').removeClass('disabled').removeClass('btn-warning').addClass('btn-info').text('Update Amazon Return');
}

var RETURN_QUEUE = [];

function requestNextAmazonOrderReturn() {
    var data = RETURN_QUEUE.pop(); // pop from the last: LIFO
    if (typeof data == 'undefined') {
        return false;
    }
    $('.return-request-individual-button[data-ebayorderreturnid="' + data.ebayOrderReturnId + '"]').addClass('disabled').text('Proceeding...');
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
$('body').on('click', '#update-all-button', function(e) {
    var amazon_account = $('#selected-amazon-account').val();
    if (amazon_account == '' || amazon_account == null) {
        alert('please enter Amazon Account');
    } else {
        RETURN_QUEUE = [] // clear existing queue
        $main_table_body.find('tr').each(function(e) {
            if ($.trim($(this).find('.related-amazon-account').text()) == $.trim(amazon_account)) {
                var $updateReturnButton = $(this).find('.update-return-individual-button');
                if ($updateReturnButton.length && !$updateReturnButton.hasClass('disabled')) {
                    RETURN_QUEUE.push({
                        ebayOrderReturnId: $updateReturnButton.attr('data-ebayorderreturnid'),
                        amazonOrderId: $updateReturnButton.attr('data-amazonorderid'),
                        asin: $updateReturnButton.attr('data-asin')
                    });
                }
            }
        });
        requestNextAmazonOrderReturn();
    }
});
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
            requestNextAmazonOrderReturn();
            break;
        case 'tabClosedWithError':
            requestNextAmazonOrderReturn();
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
