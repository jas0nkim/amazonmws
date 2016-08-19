var ORDER_TABLE_BODY_TEMPLATE = '\
<table id="order-table">\
    <thead>\
        <tr>\
            <th>Action</th>\
            <th>Record number</th>\
            <th>Buyer email</th>\
            <th>Buyer username</th>\
            <th>Item</th>\
            <th>Total price</th>\
            <th>Shipping price</th>\
            <th>Checkout status</th>\
            <th>Creation time</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><a href="javascript:void(0)" class="order-individual-button" data-orderid="<%= order.order_id %>">Order Now</a></td> \
    <td class="order-individual"><%= order.record_number %></td> \
    <td class="order-individual"><%= order.buyer_email %></td> \
    <td class="order-individual"><%= order.buyer_user_id %></td> \
    <td class="order-individual"><% _.each(order.items, function(item) { print(\'<div><span>\'+item.ebid+\'</span>&nbsp;&nbsp;<span>\'+item.title+\'</span><br><span>\'+item.sku+\'</span></div>\') }); %></td> \
    <td class="order-individual"><%= order.total_price %></td> \
    <td class="order-individual"><%= order.shipping_cost %></td> \
    <td class="order-individual"><%= order.checkout_status %></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
</tr>';

// function escapeHtml(string) {
//     return $('<div />').text(string).html();
// }

function initOrderTable() {
    $('body').append(ORDER_TABLE_BODY_TEMPLATE);
}

function getOrderTableBody() {
    return $('body').find('#order-table tbody');
}

var refreshOrderTable = function(response) {
    console.log('refreshOrderTable response', response);
    if (response.success != true) {
        return false;
    }
    var orders = response.orders;
    if (orders.length > 0) {
        var $order_table_body = getOrderTableBody();
        $order_table_body.empty();
        for (var i = 0; i < orders.length; i++) {
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
initOrderTable();
chrome.runtime.sendMessage({
    app: "automationJ",
    task: "fetchOrders"
}, refreshOrderTable);

// onclick 'order now' button
var $order_table_body = getOrderTableBody();
$order_table_body.on('click', '.order-individual-button', orderAmazonItem);

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
