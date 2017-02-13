$(function () {
    getScore();
});

function getScore() {
    $.getJSON('/get_score', function (data) {
        $('.backlog-waiting-time').text(data.backlogWaitingTime.toString());
        $('.backlog-waiting').css('color', data.backlogWaitingColor)
        $('.backlog-count').text(data.backlogCount.toString());
        $('.orders-processed').text(data.ordersProcessed.toString());
    })
}
setInterval('getScore()', 10000);
