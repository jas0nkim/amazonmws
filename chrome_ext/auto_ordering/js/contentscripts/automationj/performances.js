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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Performances</a></li> \
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
    <td class="table-cell-individual"><%= performance[1] %><br><br><a href="https://www.ebay.com/itm/<%= performance[1] %>" target="_blank">view item</a></td> \
    <td class="table-cell-individual"><%= performance[8] %></td> \
    <td class="table-cell-individual"><%= performance[9] %></td> \
    <td class="table-cell-individual"><%= performance[10] %></td> \
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
    var performances = response.performances;
    if (performances.length > 0) {
        var $table_body = getTableBody();
        $table_body.empty();
        for (var i = 0; i < performances.length; i++) {
            $table_body.append(_.template(TABLE_ROW_TEMPLATE)({
                performance: performances[i],
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
        task: "fetchItemPerformanceResults",
        days: days
    }, _refreshTable);
}


// refresh/initialize order table
initDom();
refreshTable();

var $table_body = getTableBody();
$('body').on('click', '.refresh-table-button', function(e) {
    var $this = $(this);
    refreshTable($this.attr('data-durationdays'));
});
