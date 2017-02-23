var AUTOMATIONJ_SERVER_URL = 'http://45.79.183.134:8092';

var monthNames = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
];

var weekDayNames = [
    "Sun",
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat"
];

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
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/trackings">Trackings</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/feedbacks">Feedbacks</a></li> \
                <li><a href="' + AUTOMATIONJ_SERVER_URL + '/returns">Returns</a></li> \
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
            <th>Sales / Avg. sold price</th>\
            <th>eBay fees (est.)</th>\
            <th>PayPal fees(est.)</th>\
            <th>Amazon costs</th>\
            <th>Profits / Avg. profits / Percentages (est.)</th>\
            <th>Refunds</th>\
        </tr>\
    </thead>\
    <tbody>\
    </tbody>\
</table>';

var TABLE_ROW_TEMPLATE = '\
<tr> \
    <td class="table-cell-individual"><%= report[13] %></td> \
    <td class="table-cell-individual"><%= report[0] %></td> \
    <td class="table-cell-individual"><b>$<%= formatMoney(report[1]) %></b> / <small>$<%= formatMoney(report[7]) %></small></td> \
    <td class="table-cell-individual">$<%= formatMoney(report[2]) %></td> \
    <td class="table-cell-individual">$<%= formatMoney(report[3]) %></td> \
    <td class="table-cell-individual">$<%= formatMoney(report[4]) %></td> \
    <td class="table-cell-individual"><%= report[12] %></td> \
    <td class="table-cell-individual"><strong class="text-danger">-$<%= formatMoney(report[11]) %></strong> <small class="text-danger">(<%= report[10] %>)</small></td> \
</tr>';

var _currentDurationType = 'daily';

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
            // profit_display
            var _profit = reports[i][5];
            var _profitPercentage = reports[i][6];
            var _avg_profit = reports[i][8];
            var _alertTag = _profit > 0 ? 'text-info' : 'text-danger';
            reports[i][12] = '<span class="' + _alertTag + '"><b>$' + formatMoney(_profit) + '</b> / <small>$' + formatMoney(_avg_profit) + '</small><br><small>' + _profitPercentage.toFixed(1) + '%</small></span>';

            // date format
            var _d = new Date(reports[i][9]);
            if (_currentDurationType == 'weekly') {
                reports[i][13] = "Week of " + _d.getUTCDate() + " " + monthNames[_d.getUTCMonth()] + " " + _d.getUTCFullYear();
            } else if (_currentDurationType == 'monthly') {
                reports[i][13] = monthNames[_d.getUTCMonth()] + " " + _d.getUTCFullYear();
            } else {
                reports[i][13] = weekDayNames[_d.getUTCDay()] + ", " + _d.getUTCDate() + " " + monthNames[_d.getUTCMonth()] + " " + _d.getUTCFullYear();
            }
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
    _currentDurationType = durationtype;
    chrome.runtime.sendMessage({
        app: "automationJ",
        task: "fetchReports",
        durationtype: durationtype
    }, _refreshTable);
}

function formatMoney(n) {
    return n.toFixed(2).replace(/./g, function(c, i, a) {
        return i && c !== "." && ((a.length - i) % 3 === 0) ? ',' + c : c;
    });
}

// refresh/initialize order table
initDom();
refreshTable();

var $table_body = getTableBody();
$('body').on('click', '.refresh-table-button', function(e) {
    var $this = $(this);
    refreshTable($this.attr('data-durationtype'));
});
