var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';
var AMAZON_ITEM_VARIATION_URL_POSTFIX = '/?th=1&psc=1';

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
                <li class="active dropdown"> \
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Orders <span class="caret"></span></a> \
                    <ul class="dropdown-menu"> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/all">All orders</a></li> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/unsourced">Unsourced orders</a></li> \
                    </ul> \
                </li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales report</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
            </ul> \
        </div><!-- /.navbar-collapse --> \
    </div> \
</nav>';

var MAIN_CONTAINER = '<div id="main-container" class="container-fluid"></div>';

var REFRESH_TABLE_BUTTON = '<div class="pull-right" style="padding:20px 0px;"><button id="refresh-table-button" class="btn btn-success">Refresh</button></div>'

var ORDER_TABLE_BODY_TEMPLATE = '\
<table id="order-table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Record number / eBay order ID</th>\
            <th>Buyer username (email) / Item</th>\
            <th>Total / Shipping price</th>\
            <th>eBay order received at</th>\
            <th>Action / Amazon order ID</th>\
            <th>Amazon cost</th>\
            <th>eBay final fee (est.)</th>\
            <th>PayPal fee (est.)</th>\
            <th>Margin (est.)</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
    <tfoot>\
        <tr>\
            <td colspan="9">\
                <button id="load-more-orders-button" class="btn btn-success" style="width: 100%">Load More Orders</button>\
            </td>\
        </tr>\
    </tfoot>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr class="<% order.order_status_simplified == \'cancelled\' ? print(\'warning\') : order.order_status_simplified == \'case_opened\' ? print(\'danger\') : order.order_status_simplified == \'pending\' ? print(\'info\') : print(\'\') %>"> \
    <td class="order-individual"><b><%= order.record_number %></b><br><small><%= order.order_id %></small></td> \
    <td class="order-individual" style="width: 10%;"><a href="javascript:void(0);" title="<%= order.buyer_email %>"><%= order.buyer_user_id %></a><br><br><% _.each(order.items, function(item) { print(\'<div><a href="https://www.ebay.com/itm/\'+item.ebid+\'" target="_blank">\'+item.ebid+\'</a><br><span>\'+item.title+\'</span><br><a href="\'+amz_item_url_prefix+item.sku+(item.is_variation ? amz_item_v_url_postfix : "")+\'" target="_blank">\'+item.sku+\'</a></div>\') }); %></td> \
    <td class="order-individual"><b>$<%= order.total_price.toFixed(2) %></b><br><small>$<%= order.shipping_cost.toFixed(2) %></small></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
    <td class="order-individual"><%= order.order_button %></td> \
    <td class="order-individual"><%= order.amazon_cost %></td> \
    <td class="order-individual"><%= order.ebay_final_fee %></td> \
    <td class="order-individual"><%= order.paypal_fee %></td> \
    <td class="order-individual"><%= order.margin %></td> \
</tr>';

var ORDER_CONDITION = null;

// function escapeHtml(string) {
//     return $('<div />').text(string).html();
// }

$('body').css({ "padding-top": "70px" });

function initDom() {
    $('body').append(NAVBAR);
    $('body').append(MAIN_CONTAINER);
    $('body #main-container').append(REFRESH_TABLE_BUTTON);
    $('body #main-container').append(ORDER_TABLE_BODY_TEMPLATE);
}

function getOrderTableBody() {
    return $('body').find('#order-table tbody');
}
function getOrderTable() {
    return $('body').find('#order-table');
}

var _lastOrderRecordNumber = -1;
var _loadMoreOrders = function(response) {
    if (response.success != true) {
        return false;
    }
    var orders = response.orders;
    if (orders.length > 0) {
        var $order_table_body = getOrderTableBody();
        var margin, merginPercentage, alertTag;
        for (var i = 0; i < orders.length; i++) {
            // order_status / payment_status
            if (orders[i].payment_status == 'Pending' || orders[i].payment_status == 'Failed') {
                orders[i]['order_status_simplified'] = 'pending';
            } else if (orders[i].order_status == 'Cancelled' || orders[i].order_status == 'CancelPending') {
                orders[i]['order_status_simplified'] = 'cancelled';
            } else if (orders[i].order_status == 'Active') {
                orders[i]['order_status_simplified'] = 'case_opened';
            } else {
                orders[i]['order_status_simplified'] = 'completed';
            }
            // order_button
            if (orders[i].amazon_order == null) {
                if (orders[i].order_status_simplified == 'cancelled') {
                    orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default order-individual-button disabled" data-orderid="' + orders[i].order_id + '">Order Cancelled</a>';
                } else if (orders[i].order_status_simplified == 'case_opened') {
                    orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default order-individual-button disabled" data-orderid="' + orders[i].order_id + '">Case Opened</a>';
                } else if (orders[i].order_status_simplified == 'pending') {
                    orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default order-individual-button disabled" data-orderid="' + orders[i].order_id + '">Payment Pending</a>';
                } else {
                    orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-info order-individual-button" data-orderid="' + orders[i].order_id + '">Order Now</a>';
                }
            } else {
                orders[i]['order_button'] = '<b>' + orders[i].amazon_order.order_id + '</b>';
            }
            // cost amazon
            if (orders[i].amazon_order == null) {
                orders[i]['amazon_cost'] = '<span class="order-individual-amazon-cost" data-orderid="' + orders[i].order_id + '">-</span>';
            } else {
                orders[i]['amazon_cost'] = '<span class="order-individual-amazon-cost" data-orderid="' + orders[i].order_id + '">$' + orders[i].amazon_order.total.toFixed(2) + '</span>';
            }
            // ebay final fee (9%)
            orders[i]['ebay_final_fee'] = '$' + calculateEbayFinalFee(orders[i].total_price);

            // paypal fee (4.5%)
            orders[i]['paypal_fee'] = '$' + calculatePayPalFee(orders[i].total_price);

            // margin
            if (orders[i].amazon_order == null) {
                orders[i]['margin'] = '<span class="order-individual-margin" data-orderid="' + orders[i].order_id + '">-</span>';
            } else {
                margin = calculateMargin(orders[i].total_price, orders[i].amazon_order.total);
                merginPercentage = calculateMarginPercentage(orders[i].total_price, orders[i].amazon_order.total);
                alertTag = margin > 0 ? 'text-info' : 'text-danger';
                orders[i]['margin'] = '<span class="order-individual-margin ' + alertTag + '" data-orderid="' + orders[i].order_id + '"><b>$' + margin + '</b><br><small>' + merginPercentage + '%</small></span>';
            }

            $order_table_body.append(_.template(ORDER_TABLE_ROW_TEMPLATE)({ order: orders[i], amz_item_url_prefix: AMAZON_ITEM_URL_PRIFIX, amz_item_v_url_postfix: AMAZON_ITEM_VARIATION_URL_POSTFIX }));
            _lastOrderRecordNumber = orders[i].record_number;
        }
    }
    $('#refresh-table-button').removeClass('disabled').text('Refresh');
    $('#load-more-orders-button').removeClass('disabled').text('Load More Orders');
};

function refreshOrderTable() {
    if (ORDER_CONDITION == null) {
        return false;
    }
    var $order_table_body = getOrderTableBody();
    $order_table_body.empty();
    loadMoreOrders(-1);
}

function loadMoreOrders(lastOrderRecordNumber) {
    $('#refresh-table-button').addClass('disabled').text('Loading...');
    $('#load-more-orders-button').addClass('disabled').text('Loading...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchOrders",
        perPage: 200,
        lastOrderRecordNumber: lastOrderRecordNumber,
        orderCondition: ORDER_CONDITION
    }, _loadMoreOrders);
}

function getTotalPriceAlertTag(ebayTotalPrice, amazonTotalCost) {
    if (ebayTotalPrice <= amazonTotalCost) {
        return 'text-danger';
    } else {
        return 'text-info';
    }
}

function calculateEbayFinalFee(ebayOrderTotal) {
    return (ebayOrderTotal * 0.09).toFixed(2);
}

function calculatePayPalFee(ebayOrderTotal) {
    return (ebayOrderTotal * 0.037 + 0.30).toFixed(2);
}

function calculateMargin(ebayOrderTotal, amazonOrderTotal) {
    return (ebayOrderTotal.toFixed(2) - amazonOrderTotal.toFixed(2) - calculateEbayFinalFee(ebayOrderTotal) - calculatePayPalFee(ebayOrderTotal)).toFixed(2);
}

function calculateMarginPercentage(ebayOrderTotal, amazonOrderTotal) {
    return ((ebayOrderTotal.toFixed(2) - amazonOrderTotal.toFixed(2) - calculateEbayFinalFee(ebayOrderTotal) - calculatePayPalFee(ebayOrderTotal)) / ebayOrderTotal.toFixed(2) * 100).toFixed(1);
}

function updateAmazonOrder(ebayOrderId, amazonOrderId, amazonOrderTotal, ebayOrderTotal) {
    // order button
    $('.order-individual-button[data-orderid="' + ebayOrderId + '"]').replaceWith('<b>' + amazonOrderId + '</b>');

    // amazon cost
    $('.order-individual-amazon-cost[data-orderid="' + ebayOrderId + '"]').text('$' + amazonOrderTotal.toFixed(2)).addClass(alertTag);

    // margin
    var margin = calculateMargin(ebayOrderTotal, amazonOrderTotal);
    var marginPercentage = calculateMarginPercentage(ebayOrderTotal, amazonOrderTotal);
    var alertTag = margin > 0 ? 'text-info' : 'text-danger';
    $('.order-individual-margin[data-orderid="' + ebayOrderId + '"]').html('<b>$' + margin + '</b><br><small>' + marginPercentage + '%</small>').addClass(alertTag);
}

var orderAmazonItem = function(e) {
    var $this = $(this);
    $this.addClass('disabled').text('Proceeding...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "orderAmazonItem",
        ebayOrderId: $this.attr('data-orderid')
    }, function(response) {
        console.log('orderAmazonItem response', response);
    });
    return false;
};

// TODO: verify automationj page/tab to background

// initialize order table
initDom();

// jquery event listeners
var $order_table = getOrderTable();
var $order_table_body = getOrderTableBody();
$('body').on('click', '#refresh-table-button', function(e) {
    refreshOrderTable();
});
$order_table_body.on('click', '.order-individual-button', orderAmazonItem);
$order_table.on('click', '#load-more-orders-button', function(e){
    loadMoreOrders(_lastOrderRecordNumber);
});

// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'initOrders':
            ORDER_CONDITION = message.order_condition;
            refreshOrderTable();
            break;
        case 'succeededAmazonOrdering':
            updateAmazonOrder(message.ebayOrderId, message.amazonOrderId, message.amazonOrderTotal, message.ebayOrderTotal);
            break;
        case 'failedAmazonOrdering':
            // updateOrderNowButton(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
