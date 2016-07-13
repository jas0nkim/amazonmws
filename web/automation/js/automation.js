var $ORDER_TABLE_BODY = $('#order-table tbody');

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><a href="javascript:void(0)" class="order-individual-button" data-orderid="<%= data.order_id %>" data-orderdata=<%= escapedData %>>Order Now</a></td> \
    <td class="order-individual"><%= data.record_number %></td> \
    <td class="order-individual"><%= data.buyer_email %></td> \
    <td class="order-individual"><%= data.buyer_user_id %></td> \
    <td class="order-individual"><% _.each(data.items, function(item) { print(\'<div><span>\'+item.item_id+\'</span>&nbsp;&nbsp;<span>\'+item.item_title+\'</span><br><span>\'+item.asin+\'</span></div>\') }); %></td> \
    <td class="order-individual"><%= data.total_price %></td> \
    <td class="order-individual"><%= data.shipping_cost %></td> \
    <td class="order-individual"><%= data.checkout_status %></td> \
    <td class="order-individual"><%= data.creation_time %></td> \
</tr>';

function escapeHtml(string) {
    return $('<div />').text(string).html();
}

function buildOrderTable(data) {
    if (data.length > 0) {
        for (var i = 0; i < data.length; i++) {
            $ORDER_TABLE_BODY.append(_.template(ORDER_TABLE_ROW_TEMPLATE)({ data: data[i], escapedData: escapeHtml(data[i]) }));
        }
    }
}

// test
var testData = [];
testData.push({ 
    "record_number": '123',
    "order_id": '123-3KNFUI12349-124',
    "items": [ 
        {
            'item_id': '281924483794',
            'item_title': 'Diamond Select Toys Back to The Future: Time Machine Mark I Car',
            'asin': 'B00OSO7S6I'
        }
    ],
    "total_price": '52.99',
    "shipping_cost": '0.00',
    "buyer_email": 'srgates@verizon.net',
    "buyer_user_id": 'stacy3656',
    "buyer_status": '',
    "buyer_shipping_name": 'Stacy Gates',
    "buyer_shipping_street1": '304 Gates Mountain Rd',
    "buyer_shipping_street2": '',
    "buyer_shipping_city_name": 'Howard',
    "buyer_shipping_state_or_province": 'PA',
    "buyer_shipping_postal_code": '16841-2720',
    "buyer_shipping_country": 'US',
    "buyer_shipping_phone": '814-883-0451',
    "checkout_status": 'CheckoutComplete',
    "creation_time": '12-Jul-16',
    "paid_time": '12-Jul-16'
});

buildOrderTable(testData);

$ORDER_TABLE_BODY.on('click', '.order-individual-button', function(e) {
    return false;
});

// $.ajax({
//     url: "https://api.ipify.org/orders",
//     dataType: "json",
//     success: function(data, textStatus, jqXHR) {
//         console.log(data);
//     }
// });
