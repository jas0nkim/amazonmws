var REFRESH_TABLE_BUTTON = '<div class="pull-right" style="padding:20px 0px;"><button id="refresh-table-button" class="btn btn-primary">Refresh</button></div>'

var ORDER_TABLE_BODY_TEMPLATE = '\
<table id="order-table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Record number</th>\
            <th>Action</th>\
            <th>Buyer username (email)</th>\
            <th>Item</th>\
            <th>Total price</th>\
            <th>Shipping price</th>\
            <th>eBay order status</th>\
            <th>eBay order received at</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><b><%= order.record_number %></b></td> \
    <td class="order-individual"><%= order.order_button %></td> \
    <td class="order-individual"><%= order.buyer_user_id %><br><i><%= order.buyer_email %></i></td> \
    <td class="order-individual"><% _.each(order.items, function(item) { print(\'<div><span>\'+item.ebid+\'</span><br><span>\'+item.title+\'</span><br><span>\'+item.sku+\'</span></div>\') }); %></td> \
    <td class="order-individual">$<%= order.total_price %></td> \
    <td class="order-individual">$<%= order.shipping_cost %></td> \
    <td class="order-individual"><%= order.checkout_status_verbose %></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
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

function updateOrderNowButton(ebayOrderId, amazonOrderId) {
    $('.order-individual-button[data-orderid="' + ebayOrderId + '"]').replaceWith('<b>' + amazonOrderId + '</b>');
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
            updateOrderNowButton(message.ebayOrderId, message.amazonOrderId);
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
