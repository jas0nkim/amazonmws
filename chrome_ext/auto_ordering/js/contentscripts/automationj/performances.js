var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';

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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Performances</a></li> \
            </ul> \
        </div><!-- /.navbar-collapse --> \
    </div> \
</nav>';

var MAIN_CONTAINER = '<div id="main-container" class="container-fluid"></div>';

var REFRESH_TABLE_BUTTONS = '<div class="pull-right" style="padding:20px 0px;"> \
    <button id="last-three-days-button" class="refresh-table-button btn btn-success" data-durationdays="3" data-buttontext="Last 3 days">Last 3 days</button> \
    <button id="last-seven-days-button" class="refresh-table-button btn btn-success" data-durationdays="7" data-buttontext="Last 7 days">Last 7 days</button> \
    <button id="last-fifteen-days-button" class="refresh-table-button btn btn-success" data-durationdays="15" data-buttontext="Last 15 days">Last 15 days</button> \
    <button id="last-thrity-days-button" class="refresh-table-button btn btn-success" data-durationdays="30" data-buttontext="Last 30 days">Last 30 days</button> \
    <button id="last-sixty-days-button" class="refresh-table-button btn btn-success" data-durationdays="60" data-buttontext="Last 60 days">Last 60 days</button> \
</div>';

var TABLE_BODY_TEMPLATE = '\
<table id="table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Item</th>\
            <th>Clicks</th>\
            <th>Watches</th>\
            <th>Solds</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="table-cell-individual"><a href="https://www.ebay.com/itm/<%= item.ebid %>" target="_blank"><%= item.ebid %></a><br><span><%= item.title %></span><br><a href="<%= amz_item_url_prefix + item.sku %>" target="_blank"><%= item.sku %></a></td> \
    <td class="table-cell-individual"><%= item.clicks %></td> \
    <td class="table-cell-individual"><%= item.watches %></td> \
    <td class="table-cell-individual"><%= item.solds %></td> \
</tr>';

function initDom() {
    $('body').append(NAVBAR);
    $('body').append(MAIN_CONTAINER);
    $('body #main-container').append(REFRESH_TABLE_BUTTONS);
    $('body #main-container').append(TABLE_BODY_TEMPLATE);
}

function getTableBody() {
    return $('body').find('#table tbody');
}

var _refreshTable = function(response) {
    if (response.success != true) {
        return false;
    }
    var items = response.items;
    if (items.length > 0) {
        var $table_body = getTableBody();
        $table_body.empty();
        for (var i = 0; i < items.length; i++) {
            // if (items[i].amazon_order == null) {
            //     items[i]['amazon_order_id'] = '-';
            //     items[i]['track_button'] = '-';
            // } else {
            //     // amazon_order_id
            //     amazon_order_id = items[i].amazon_order.order_id;
            //     items[i]['amazon_order_id'] = '<span class="table-cell-individual-amazon-order-id" data-ebayorderid="' + items[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">' + amazon_order_id + '</span>';
            //     // track_button
            //     if (items[i].tracking == null) {
            //         items[i]['track_button'] = '<a href="javascript:void(0)" class="btn btn-info track-individual-button" data-ebayorderid="' + items[i].order_id + '" data-amazonorderid="' + amazon_order_id + '">Track Now</a>';
            //     } else {
            //         items[i]['track_button'] = '<b>' + items[i].tracking.tracking_number + '</b><br><small>' + items[i].tracking.carrier + '</small>';
            //     }
            // }

            $table_body.append(_.template(TABLE_ROW_TEMPLATE)({
                item: items[i],
                amz_item_url_prefix: AMAZON_ITEM_URL_PRIFIX
            }));
        }
    }
    $('.refresh-table-button').each(function(e) {
        var $this = $(this);
        var buttonText = $this.attr('data-buttontext');
        $this.removeClass('disabled').text(buttonText);
    });
};

function refreshTable(days) {
    if (typeof days == 'undefined') {
        // default days value is 3
        days = 3;
    }
    $('.refresh-table-button').addClass('disabled').text('Loading...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchItemStatResults",
        days: days
    }, _refreshTable);
}

// function updateOrderTracking(ebayOrderId, amazonOrderId, carrier, trackingNumber, success) {
//     if (success) {
//         $('.track-individual-button[data-amazonorderid="' + amazonOrderId + '"]').replaceWith('<b>' + trackingNumber + '</b><br><small>' + carrier + '</small>');
//     } else {
//         $('.track-individual-button[data-amazonorderid="' + amazonOrderId + '"]').text('Track Later');
//     }
// }

// var trackAmazonOrder = function(e) {
//     var $this = $(this);
//     $this.addClass('disabled').text('Proceeding...');
//     chrome.runtime.sendMessage({
//         app: "automationJ",
//         task: "trackAmazonOrder",
//         ebayOrderId: $this.attr('data-ebayorderid'),
//         amazonOrderId: $this.attr('data-amazonorderid')
//     }, function(response) {
//         console.log('trackAmazonOrder response', response);
//     });
//     return false;
// };


// refresh/initialize order table
initDom();
refreshTable();

var $table_body = getTableBody();
$table_body.on('click', '.track-individual-button', trackAmazonOrder);
$('body').on('click', '.refresh-table-button', function(e) {
    var $this = $(this);
    refreshTable($this.attr('data-durationdays'));
});


// // chrome extention message listeners
// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//     if (message.app == 'automationJ') { switch(message.task) {
//         case 'succeededOrderTracking':
//             updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber, true);
//             break;
//         case 'failedOrderTracking':
//             updateOrderTracking(message.ebayOrderId, message.amazonOrderId, message.carrier, message.trackingNumber, false);
//             break;
//         default:
//             break;
//     }}
//     sendResponse({ success: true });
// });
