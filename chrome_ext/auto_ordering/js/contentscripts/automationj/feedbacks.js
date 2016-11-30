var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';

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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders">Orders</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales report</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
            </ul> \
            <div class="navbar-form navbar-left"> \
                <div class="form-group"> \
                    <input type="text" class="form-control" id="selected-amazon-account" placeholder="Amazon Account..."> \
                </div> \
                <button type="button" class="btn btn-info" id="feedback-all-button">Feedback All Orders</button> \
            </div> \
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
            <th>Amazon order ID / Account</th>\
            <th>Tracking information</th>\
            <th>Action / Feedback</th>\
            <th>eBay order received at</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
    <tfoot>\
        <tr>\
            <td colspan="6">\
                <button id="load-more-orders-button" class="btn btn-success" style="width: 100%">Load More Orders</button>\
            </td>\
        </tr>\
    </tfoot>\
</table>';

var ORDER_TABLE_ROW_TEMPLATE = '\
<tr class="<% order.order_status_simplified == \'cancelled\' ? print(\'warning\') : order.order_status_simplified == \'case_opened\' ? print(\'danger\') : order.order_status_simplified == \'pending\' ? print(\'info\') : print(\'\') %>"> \
    <td class="order-individual"><b><%= order.record_number %></b><br><small><%= order.order_id %></small></td> \
    <td class="order-individual"><a href="javascript:void(0);" title="<%= order.buyer_email %>"><%= order.buyer_user_id %></a></td> \
    <td class="order-individual"><%= order.amazon_order_id %><br><small class="related-amazon-account"><%= order.related_amazon_account %></small></td> \
    <td class="order-individual"><%= order.tracking_info %></td> \
    <td class="order-individual"><%= order.feedback_button %></td> \
    <td class="order-individual"><%= order.creation_time %></td> \
</tr>';

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
        for (var i = 0; i < orders.length; i++) {
            // order_status
            if (orders[i].payment_status == 'Pending' || orders[i].payment_status == 'Failed') {
                orders[i]['order_status_simplified'] = 'pending';
            } else if (orders[i].order_status == 'Cancelled' || orders[i].order_status == 'CancelPending') {
                orders[i]['order_status_simplified'] = 'cancelled';
            } else if (orders[i].order_status == 'Active') {
                orders[i]['order_status_simplified'] = 'case_opened';
            } else {
                orders[i]['order_status_simplified'] = 'completed';
            }
            // amazon_order
            if (orders[i].amazon_order == null) {
                orders[i]['amazon_order_id'] = '-';
                orders[i]['related_amazon_account'] = '-';
                orders[i]['tracking_info'] = '-';
                orders[i]['feedback_button'] = '-';
            } else {
                // amazon_order_id
                amazon_order_id = orders[i].amazon_order.order_id;
                orders[i]['amazon_order_id'] = '<span class="order-individual-amazon-order-id" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">' + amazon_order_id + '</span>';
                // related amazon account
                orders[i]['related_amazon_account'] = orders[i].amazon_order.amazon_account_email;
                // tracking_info
                if (orders[i].tracking == null) {
                    if (orders[i].order_status_simplified == 'cancelled') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default track-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Order Cancelled</a>';
                    } else if (orders[i].order_status_simplified == 'case_opened') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default track-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Case Opened</a>';
                    } else if (orders[i].order_status_simplified == 'pending') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default track-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Payment Pending</a>';
                    } else {
                        orders[i]['tracking_info'] = '<a href="javascript:void(0)" class="btn btn-default track-individual-button" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Track Now</a>';
                    }
                } else {
                    orders[i]['tracking_info'] = '<b>' + orders[i].tracking.tracking_number + '</b><br><small>' + orders[i].tracking.carrier + '</small>';
                }
                // feedback_button
                if (orders[i].feedback_left == 0 || orders[i].feedback_left == false) {
                    if (orders[i].order_status_simplified == 'cancelled') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default feedback-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Order Cancelled</a>';
                    } else if (orders[i].order_status_simplified == 'case_opened') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default feedback-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Case Opened</a>';
                    } else if (orders[i].order_status_simplified == 'pending') {
                        orders[i]['order_button'] = '<a href="javascript:void(0)" class="btn btn-default feedback-individual-button disabled" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Payment Pending</a>';
                    } else {
                        orders[i]['feedback_button'] = '<a href="javascript:void(0)" class="btn btn-info feedback-individual-button" data-ebayorderid="' + orders[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Leave Feedback Now</a></td>';
                    }
                } else {
                    orders[i]['feedback_button'] = '<b>Positive feedback left</b>';
                }
            }

            $order_table_body.append(_.template(ORDER_TABLE_ROW_TEMPLATE)({ order: orders[i] }));
            _lastOrderRecordNumber = orders[i].record_number;
        }
    }
    $('#refresh-table-button').removeClass('disabled').text('Refresh');
    $('#load-more-orders-button').removeClass('disabled').text('Load More Orders');
};

function refreshOrderTable() {
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
        lastOrderRecordNumber: lastOrderRecordNumber,
    }, _loadMoreOrders);
}

function updateOrderTracking(ebayOrderId, amazonOrderId, carrier, trackingNumber, success) {
    if (success) {
        $('.track-individual-button[data-amazonorderid="' + amazonOrderId + '"]').replaceWith('<b>' + trackingNumber + '</b><br><small>' + carrier + '</small>');
    } else {
        $('.track-individual-button[data-amazonorderid="' + amazonOrderId + '"]').text('Track Later');
    }
}

function updateFeedbackLeaving(ebayOrderId, amazonOrderId, success) {
    if (success) {
        $('.feedback-individual-button[data-amazonorderid="' + amazonOrderId + '"]').replaceWith('<b>Positive feedback left</b>');
    } else {
        $('.feedback-individual-button[data-amazonorderid="' + amazonOrderId + '"]').text('Feedback Later');
    }
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

var FEEDBACK_QUEUE = [];

function feedbackNextAmazonOrder() {
    var data = FEEDBACK_QUEUE.pop(); // pop from the last: LIFO
    if (typeof data == 'undefined') {
        return false;
    }
    $('.feedback-individual-button[data-amazonorderid="' + data.amazonOrderId + '"]').addClass('disabled').text('Proceeding...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "leaveFeedback",
        ebayOrderId: data.ebayOrderId,
        amazonOrderId: data.amazonOrderId
    }, function(response) {
        console.log('leaveFeedback response', response);
    });
    return false;
}

// refresh/initialize order table
initDom();
refreshOrderTable();

var $order_table = getOrderTable();
var $order_table_body = getOrderTableBody();
$('body').on('click', '#refresh-table-button', function() {
    refreshOrderTable();
});
$('body').on('click', '#feedback-all-button', function(e) {
    var amazon_account = $('#selected-amazon-account').val();
    if (amazon_account == '' || amazon_account == null) {
        alert('please enter Amazon Account');
    } else {
        FEEDBACK_QUEUE = [] // clear existing queue
        $order_table_body.find('tr').each(function(e) {
            if ($.trim($(this).find('.related-amazon-account').text()) == $.trim(amazon_account)) {
                var $feedbackNowButton = $(this).find('.feedback-individual-button');
                if ($feedbackNowButton.length && !$feedbackNowButton.hasClass('disabled')) {
                    FEEDBACK_QUEUE.push({
                        ebayOrderId: $feedbackNowButton.attr('data-ebayorderid'),
                        amazonOrderId: $feedbackNowButton.attr('data-amazonorderid')
                    });
                }
            }
        });
        feedbackNextAmazonOrder();
    }
});
$order_table_body.on('click', '.track-individual-button', trackAmazonOrder);
$order_table_body.on('click', '.feedback-individual-button', function(e) {
    var $this = $(this);
    FEEDBACK_QUEUE.push({
        ebayOrderId: $this.attr('data-ebayorderid'),
        amazonOrderId: $this.attr('data-amazonorderid')
    });
    feedbackNextAmazonOrder();
});

$order_table.on('click', '#load-more-orders-button', function(e){
    loadMoreOrders(_lastOrderRecordNumber);
});


// chrome extention message listeners
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.app == 'automationJ') { switch(message.task) {
        case 'succeededOrderTracking':
            updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber, true);
            break;
        case 'failedOrderTracking':
            updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber, false);
            break;
        case 'succeededFeedbackLeaving':
            updateFeedbackLeaving(message.ebayOrderId, message.amazonOrderId, true);
            feedbackNextAmazonOrder();
            break;
        case 'failedFeedbackLeaving':
            updateFeedbackLeaving(message.ebayOrderId, message.amazonOrderId, false);
            feedbackNextAmazonOrder();
            break;
        default:
            break;
    }}
    sendResponse({ success: true });
});
