/* Copyright 2012 Bogdan-Cristian Tataroiu, Szymon Sidor */

$(document).ready(function() {
    $('#navTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $("#timeLeft").each(function () {
        var endTimestamp = parseFloat($(this).attr('class')),
            that = this;
        var updateTimeLeft = function () {
            $(that).html(formatTimeRemaining(endTimestamp));
        };
        updateTimeLeft();
        setInterval(updateTimeLeft, 1000);
    });
});

var formatTimeRemaining = function(endTimestamp) {
    var date = new Date();
    var now = Math.floor(date.getTime() / 1000);
    var rem = 0;
    if (endTimestamp < now) {
        rem = 0;
    } else {
        rem = endTimestamp - now;
    }
    var s = rem % 60;
    rem = Math.floor(rem / 60);
    var m = rem % 60;
    rem = Math.floor(rem / 60);
    var h = rem;
    return (("00" + h).slice(-2) + ':' +
            ("00" + m).slice(-2) + ':' +
            ("00" + s).slice(-2));
};
