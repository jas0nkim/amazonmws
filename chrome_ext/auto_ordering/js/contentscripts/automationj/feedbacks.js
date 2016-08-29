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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
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
            <th>Tracking information</th>\
            <th>Action / Feedback</th>\
            <th>eBay order received at</th>\
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
    <td class="order-individual"><%= order.tracking_info %></td> \
    <td class="order-individual"><%= order.feedback_button %></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
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
            if (orders[i].amazon_order == null) {
                orders[i]['amazon_order_id'] = '-';
                orders[i]['tracking_info'] = '-';
                orders[i]['feedback_button'] = '-';
            } else {
                // amazon_order_id
                amazon_order_id = orders[i].amazon_order.order_id;
                orders[i]['amazon_order_id'] = '<span class="order-individual-amazon-order-id" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">' + amazon_order_id + '</span>';
                // tracking_info
                if (orders[i].tracking == null) {
                    orders[i]['tracking_info'] = '<a href="javascript:void(0)" class="btn btn-default track-individual-button" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Track Now</a>';
                } else {
                    orders[i]['tracking_info'] = '<b>' + orders[i].tracking.tracking_number + '</b><br><small>' + orders[i].tracking.carrier + '</small>';
                }
                // feedback_button
                if (orders[i].feedback_left == 0 || orders[i].feedback_left == false) {
                    orders[i]['feedback_button'] = '<a href="javascript:void(0)" class="btn btn-info feedback-individual-button" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Leave Feedback Now</a></td>';
                } else {
                    orders[i]['feedback_button'] = '<b>Positive feecback left</b>';
                }
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

function updateFeedbackLeaving(ebayOrderId, amazonOrderId) {
    $('.feedback-individual-button[data-amazonorderid="' + amazonOrderId + '"]').replaceWith('<b>Positive feecback left</b>');
}

var trackAmazonOrder = function(e) {
    var $this = $(this);
    $this.addClass('disabled').text('Proceeding...');
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

var leaveFeedback = function(e) {
    var $this = $(this);
    $this.addClass('disabled').text('Proceeding...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "leaveFeedback",
        ebayOrderId: $this.attr('data-ebayorderid'),
        amazonOrderId: $this.attr('data-amazonorderid')
    }, function(response) {
        console.log('leaveFeedback response', response);
    });
    return false;
};


// refresh/initialize order table
initDom();
refreshOrderTable();

var $order_table_body = getOrderTableBody();
$order_table_body.on('click', '.track-individual-button', trackAmazonOrder);
$order_table_body.on('click', '.feedback-individual-button', leaveFeedback);
$('body').on('click', '#refresh-table-button', function() {
    refreshOrderTable();
});


// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'succeededOrderTracking':
            updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber);
            break;
        case 'succeededFeedbackLeaving':
            updateFeedbackLeaving(message.ebayOrderId, message.amazonOrderId);
            break;
        case 'failedFeedbackLeaving':
            // updateOrderNowButton(message);
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
