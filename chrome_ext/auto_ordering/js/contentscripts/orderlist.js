var $ORDER_TABLE_BODY = $('#order-table tbody');

$ORDER_TABLE_BODY.on('click', '.order-individual-button', function(e) {

    var $this = $(this);
    var orderData = JSON.parse($this.attr('data-orderdata'));
    
    alert('Order ID', $this.attr('data-orderid'));
    alert('Order Object', orderData);
    return false;
});
