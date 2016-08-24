var REFRESH_TABLE_BUTTON = '<div class="pull-right" style="padding:20px 0px;"><button id="refresh-table-button" class="btn btn-primary">Refresh</button></div>'

var ORDER_TABLE_BODY_TEMPLATE = '\
<table id="order-table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Record number</th>\
            <th>Buyer username (email)</th>\
            <th>Item</th>\
            <th>Total price</th>\
            <th>Shipping price</th>\
            <th>eBay order status</th>\
            <th>eBay order received at</th>\
            <th>Action / Amazon Order ID</th>\
            <th>Amazon Cost</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><b><%= order.record_number %></b></td> \
    <td class="order-individual" style="width: 10%;"><a href="javascript:void(0);" title="<%= order.buyer_email %>"><%= order.buyer_user_id %></a></td> \
    <td class="order-individual" style="width: 15%;"><% _.each(order.items, function(item) { print(\'<div><a href="https://www.ebay.com/itm/\'+item.ebid+\'" target="_blank">\'+item.ebid+\'</a><br><span>\'+item.title+\'</span><br><a href="https://www.amazon.com/dp/\'+item.sku+\'" target="_blank">\'+item.sku+\'</a></div>\') }); %></td> \
    <td class="order-individual">$<%= order.total_price %></td> \
    <td class="order-individual">$<%= order.shipping_cost %></td> \
    <td class="order-individual"><%= order.checkout_status_verbose %></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
    <td class="order-individual"><%= order.order_button %></td> \
    <td class="order-individual"><%= order.amazon_cost %></td> \
</tr>';

// function escapeHtml(string) {
//     return $('<div />').text(string).html();
// }

function initDom() {
    $('body').append('<div id="main-container" class="container"></div>');
    $('body #main-container').append(REFRESH_TABLE_BUTTON);
    $('body #main-container').append(ORDER_TABLE_BODY_TEMPLATE);
}

function getOrderTableBody() {
    return $('body').find('#order-table tbody');
}

function updateAmazonOrder(ebayOrderId, amazonOrderId, amazonOrderTotal) {
    $('.order-individual-button[data-orderid="' + ebayOrderId + '"]').replaceWith('<b>' + amazonOrderId + '</b>');
    $('.order-individual-amazon-cost[data-orderid="' + ebayOrderId + '"]').replaceWith('$' + amazonOrderTotal);

}

function refreshOrderTable() {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchOrders"
    }, _refreshOrderTable);
}

var _refreshOrderTable = function(response) {
    console.log('refreshOrderTable response', response);
    if (response.success != true) {
        return false;
    }
    var orders = response.orders;
    if (orders.length > 0) {
        var $order_table_body = getOrderTableBody();
        $order_table_body.empty();
        for (var i = 0; i < orders.length; i++) {
            // order_button
            if (orders[i].amazon_order == null) {
                orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-info order-individual-button" data-orderid="' + orders[i].order_id + '">Order Now</a></td>';
            } else {
                orders[i]['order_button'] = '<b>' + orders[i].amazon_order.order_id + '</b>';
            }
            // checkout_status_verbose
            if (orders[i].checkout_status == 'CheckoutComplete') {
                orders[i]['checkout_status_verbose'] = 'Completed';
            } else {
                orders[i]['checkout_status_verbose'] = 'In Process';
            }
            // cost amazon
            if (orders[i].amazon_order == null) {
                orders[i]['amazon_cost'] = '<span class="order-individual-amazon-cost" data-orderid="' + orders[i].order_id + '">-</span>';
            } else {
                orders[i]['amazon_cost'] = '<span class="order-individual-amazon-cost" data-orderid="' + orders[i].order_id + '">$' + orders[i].amazon_order.total + '</span>';
            }
            $order_table_body.append(_.template(ORDER_TABLE_ROW_TEMPLATE)({ order: orders[i] }));
        }
    }
};

var orderAmazonItem = function(e) {
    var $this = $(this);
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "orderAmazonItem",
        ebayOrderId: $this.attr('data-orderid')
    }, function(response) {
        console.log('orderAmazonItem response', response);
    });
    return false;
};

// verify automationj page/tab to background
// chrome.runtime.sendMessage({
//     app: "automationJ",
//     task: "validateAutomationJPage"
// }, function(response) {
//     console.log(response);
// });

// refresh/initialize order table
initDom();
refreshOrderTable();

// jquery event listeners
var $order_table_body = getOrderTableBody();
$order_table_body.on('click', '.order-individual-button', orderAmazonItem);
$('body').on('click', '#refresh-table-button', function() {
    refreshOrderTable();
});

// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log('onMessage: message', message);
    if (message.app == 'automationJ') { switch(message.task) {
        case 'succeededAmazonOrdering':
            updateAmazonOrder(message.ebayOrderId, message.amazonOrderId, message.amazonOrderTotal);
            break;
        case 'failedAmazonOrdering':
            // updateOrderNowButton(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});


// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//     // check this request from tab created via this screen
//     if (automationTabIds.indexOf(sender.tab.id) > 0) {
//         // 1. check message
//         // 2. send data
//         if (message['subject'] == 'automationJ.OrderAmazonItem') {
//             sendResponse(orderData);
//         }
//     }
// });
