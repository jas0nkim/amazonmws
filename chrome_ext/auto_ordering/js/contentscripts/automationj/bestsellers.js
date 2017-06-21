var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';
var AMAZON_ITEM_URL_PRIFIX = 'https://www.amazon.com/dp/';
var EBAY_ITEM_URL_PRIFIX = 'https://www.ebay.com/itm/';

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
                <li class="dropdown"> \
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Orders <span class="caret"></span></a> \
                    <ul class="dropdown-menu"> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/all">All orders</a></li> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/orders/unsourced">Unsourced orders</a></li> \
                    </ul> \
                </li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Trackings & Feedbacks</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/returns">Returns</a></li> \
                <li class="active dropdown"> \
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Reports <span class="caret"></span></a> \
                    <ul class="dropdown-menu"> \
                        <li><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales</a></li> \
                        <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/bestsellers">Best sellers</a></li> \
                    </ul> \
                </li> \
                <!-- \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
                --> \
            </ul> \
        </div><!-- /.navbar-collapse --> \
    </div> \
</nav>';

var MAIN_CONTAINER = '<div id="main-container" class="container-fluid"></div>';

var REFRESH_TABLE_BUTTONS = '<div class="pull-right" style="padding:20px 0px;"> \
    <button id="last-thirty-days-button" class="refresh-table-button btn btn-success" data-durationdays="30" data-buttontext="Last 30 days">Last 30 days</button> \
    <button id="last-ninty-days-button" class="refresh-table-button btn btn-success" data-durationdays="90" data-buttontext="Last 90 days">Last 90 days</button> \
    <button id="last-one-year-button" class="refresh-table-button btn btn-success" data-durationdays="365" data-buttontext="Last 1 year">Last 1 year</button> \
</div>';

var TABLE_BODY_TEMPLATE = '\
<table id="table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th>Rank</th>\
            <th>Item / Brand</th>\
            <th>Category</th>\
            <th>Solds / Cancels / Returns / Return rates</th>\
            <th>Listed since</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="table-cell-individual"><%= rank %></td> \
    <td class="table-cell-individual" style="width: 25%"><strong><%= bestseller[2] %></strong><br><span class="text-info"><%= bestseller[3] %></span><br><br><a href="<%= ebay_item_url_prefix + bestseller[0] %>" target="_blank">view ebay item</a><br><a href="<%= amz_item_url_prefix + bestseller[1] %>" target="_blank">view amazon item</a></td> \
    <td class="table-cell-individual" style="width: 25%"><%= bestseller[4] %></td> \
    <td class="table-cell-individual"><span class="text-info"><strong><%= bestseller[6] %></strong></span><span class="text-warning"> / <%= bestseller[7] %> / <%= bestseller[8] %></span><br><span class="text-danger"><%= (bestseller[8] / (bestseller[6] - bestseller[7]) * 100).toFixed(1) %>%</span></td> \
    <td class="table-cell-individual"><%= bestseller[5] %></td> \
</tr>';

$('body').css({ "padding-top": "70px" });

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
    var bestsellers = response.bestsellers;
    if (bestsellers.length > 0) {
        var $table_body = getTableBody();
        $table_body.empty();
        var rank = 1;
        for (var i = 0; i < bestsellers.length; i++) {
            $table_body.append(_.template(TABLE_ROW_TEMPLATE)({
                bestseller: bestsellers[i],
                rank: rank,
                amz_item_url_prefix: AMAZON_ITEM_URL_PRIFIX,
                ebay_item_url_prefix: EBAY_ITEM_URL_PRIFIX
            }));
            rank++;
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
        // default days value is 30
        days = 30;
    }
    $('.refresh-table-button').addClass('disabled').text('Loading...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchBestSellers",
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
