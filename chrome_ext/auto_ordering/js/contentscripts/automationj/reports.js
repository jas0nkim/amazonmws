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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li class="active"><a href="' + AUTOMATIONJ_SERVER_URL + '/reports">Sales report</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/performances">Listing performances</a></li> \
            </ul> \
        </div><!-- /.navbar-collapse --> \
    </div> \
</nav>';

var MAIN_CONTAINER = '<div id="main-container" class="container-fluid"></div>';

var REFRESH_TABLE_BUTTONS = '<div class="pull-right" style="padding:20px 0px;"> \
    <button id="daily-report-button" class="refresh-table-button btn btn-success" data-durationtype="daily" data-buttontext="Daily">Daily</button> \
    <button id="weekly-report-button" class="refresh-table-button btn btn-success" data-durationtype="weekly" data-buttontext="Weekly">Weekly</button> \
    <button id="monthly-report-button" class="refresh-table-button btn btn-success" data-durationtype="monthly" data-buttontext="Monthly">Monthly</button> \
</div>';

var TABLE_BODY_TEMPLATE = '\
<table id="table" class="table table-striped table-hover">\
    <thead>\
        <tr>\
            <th></th>\
            <th>Orders</th>\
            <th>Sales</th>\
            <th>eBay fees (est.)</th>\
            <th>PayPal fees(est.)</th>\
            <th>Amazon costs</th>\
            <th>Profits / Percentages (est.)</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="table-cell-individual"><%= report[7] %></td> \
    <td class="table-cell-individual"><%= report[0] %></td> \
    <td class="table-cell-individual">$<%= report[1] %></td> \
    <td class="table-cell-individual">$<%= report[2] %></td> \
    <td class="table-cell-individual">$<%= report[3] %></td> \
    <td class="table-cell-individual">$<%= report[4] %></td> \
    <td class="table-cell-individual"><b>$<%= report[5] %></b><br><small><%= report[6] %>%</small></td> \
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
    var reports = response.reports;
    if (reports.length > 0) {
        var $table_body = getTableBody();
        $table_body.empty();
        for (var i = 0; i < reports.length; i++) {
            $table_body.append(_.template(TABLE_ROW_TEMPLATE)({
                report: reports[i]
            }));
        }
    }
    $('.refresh-table-button').each(function(e) {
        var $this = $(this);
        var buttonText = $this.attr('data-buttontext');
        $this.removeClass('disabled').text(buttonText);
    });
};

function refreshTable(durationtype) {
    if (typeof durationtype == 'undefined') {
        // default days value is 3
        durationtype = 'daily';
    }
    $('.refresh-table-button').addClass('disabled').text('Loading...');
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchReports",
        durationtype: durationtype
    }, _refreshTable);
}


// refresh/initialize order table
initDom();
refreshTable();

var $table_body = getTableBody();
$('body').on('click', '.refresh-table-button', function(e) {
    var $this = $(this);
    refreshTable($this.attr('data-durationtype'));
});
