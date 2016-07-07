var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><a href="javascript:void(0)" class="order-individual-button">Order Now</a></td> \
    <td class="order-individual"><%= data.recordNumber %></td> \
    <td class="order-individual"><%= data.buyerEmail %></td> \
    <td class="order-individual"><%= data.buyerUsername %></td> \
    <td class="order-individual"><%= data.ebid %></td> \
    <td class="order-individual"><%= data.itemTitle %></td> \
    <td class="order-individual"><%= data.customTitle %></td> \
    <td class="order-individual"><%= data.salePrice %></td> \
    <td class="order-individual"><%= data.totalPrice %></td> \
    <td class="order-individual"><%= data.paidDate %></td> \
</tr>';

function buildOrderTable(data) {
    if (data.length > 0) {
        var $tableBody = $('#order-table tbody');

        for (var i = 0; i < data.length; i++) {
            $tableBody.append(_.template(ORDER_TABLE_ROW_TEMPLATE)(data[0]);
        }
    }
}

$.ajax({
    url: "https://api.ipify.org/orders",
    dataType: "json",
    success: function(data, textStatus, jqXHR) {
        console.log(data);
    }
});
