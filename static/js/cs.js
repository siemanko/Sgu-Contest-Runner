/* Copyright 2012 Bogdan-Cristian Tataroiu */

$(document).ready(function() {
    $('#navTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});
