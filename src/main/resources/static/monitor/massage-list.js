function getMassageList(param) {
    $.ajax({
        type: "POST",
        async: false,
        dataType: "json",
        url: basePath + "/monitor/massage-list?_time=" + new Date().getTime(),
        data: param,
        success: function (res) {
            //将数据填充
            $("#nowPage").val(res.page);
            $("#pageNum").val(res.pages);
            var content = showMassageList(res);
            $('#massageList').html(content);//显示详情页面
        }
    });
}

function showMassageList(data) {
    var html = '';
    var res = data.rows;
    for (var i = 0; i < res.length; i++) {
        html += '<li class="clearfix">' +
            '<div class="news-date">' +
            '<div class="news-date1">' + res[i].id + '</div>' +
            '</div>' +
            '<div class="news-bodys">' +
            '<a class="username">' + res[i].speaker + '</a>' +
            '<a class="verb">' + res[i].verb + '</a>' +
            '<p class="centence">' + res[i].content + '</p></div></li>'
    }
    return html;
}