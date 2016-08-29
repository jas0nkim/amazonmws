var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';

var NAVBAR = '<nav class="navbar navbar-default"> \
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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders">Orders</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
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
            <th>Buyer username (email)</th>\
            <th>Amazon order ID</th>\
            <th>Action / Tracking number</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="order-individual"><b><%= order.record_number %></b><br><small><%= order.order_id %></small></td> \
    <td class="order-individual"><a href="javascript:void(0);" title="<%= order.buyer_email %>"><%= order.buyer_user_id %></a></td> \
    <td class="order-individual"><%= order.amazon_order_id %></td> \
    <td class="order-individual"><%= order.track_button %></td> \
</tr>';

function initDom() {
    $('body').append(NAVBAR);
    $('body').append(MAIN_CONTAINER);
    $('body #main-container').append(REFRESH_TABLE_BUTTON);
    $('body #main-container').append(ORDER_TABLE_BODY_TEMPLATE);
}

function getOrderTableBody() {
    return $('body').find('#order-table tbody');
}

var _refreshOrderTable = function(response) {
    if (response.success != true) {
        return false;
    }
    var orders = response.orders;
    if (orders.length > 0) {
        var $order_table_body = getOrderTableBody();
        $order_table_body.empty();
        for (var i = 0; i < orders.length; i++) {
            // amazon_order_id
            var amazon_order_id = '-';
            if (orders[i].amazon_order != null) {
                amazon_order_id = orders[i].amazon_order.order_id;
            }
            orders[i]['amazon_order_id'] = '<span class="order-individual-amazon-order-id" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">' + amazon_order_id + '</span>';
            // track_button
            if (orders[i].tracking == null) {
                orders[i]['track_button'] = '<a href="javascript:void(0)" class="btn btn-info track-individual-button" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Track Now</a>';
            } else {
                orders[i]['track_button'] = '<b>' + orders[i].tracking.tracking_number + '</b><br><small>' + orders[i].tracking.carrier + '</small>';
            }

            $order_table_body.append(_.template(ORDER_TABLE_ROW_TEMPLATE)({ order: orders[i] }));
        }
    }
};

function refreshOrderTable() {
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchOrders"
    }, _refreshOrderTable);
}

function updateOrderTracking(ebayOrderId, amazonOrderId, carrier, trackingNumber) {
    $('.track-individual-button[data-amazonorderid="' + amazonOrderId + '"]').replaceWith('<b>' + trackingNumber + '</b><br><small>' + carrier + '</small>');
}

var trackAmazonOrder = function(e) {
    var $this = $(this);
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "trackAmazonOrder",
        ebayOrderId: $this.attr('data-ebayorderid'),
        amazonOrderId: $this.attr('data-amazonorderid')
    }, function(response) {
        console.log('trackAmazonOrder response', response);
    });
    return false;
};


// refresh/initialize order table
initDom();
refreshOrderTable();

var $order_table_body = getOrderTableBody();
$order_table_body.on('click', '.track-individual-button', trackAmazonOrder);
$('body').on('click', '#refresh-table-button', function() {
    refreshOrderTable();
});


// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'succeededOrderTracking':
            updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber);
            break;
        case 'failedOrderTracking':
            // updateOrderNowButton(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
