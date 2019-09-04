/***
 * 扩展的方法
 */
jQuery.extend({
    showLoading: function () {
        document.getElementsByClassName("over-loading")[0].style.display = "block";
        document.getElementsByClassName("layout-loading")[0].style.display = "block";
    },
    hideLoading: function () {
        document.getElementsByClassName("over-loading")[0].style.display = "none";
        document.getElementsByClassName("layout-loading")[0].style.display = "none";
    },
    getOperateHtml: function (opHtml) {
        var html = '<div class="btn-group">'
            + '<button type="button" class="btn btn-sm dropdown-toggle"'
            + 'data-toggle="dropdown" aria-expanded="false">'
            + '操作&nbsp;<span class="caret"></span>'
            + '</button>'
            + '<ul class="dropdown-menu" role="menu">'
            + opHtml
            + '</ul>'
            + '</div>';
        return html;
    },
    skipPage: function (pageNo, oTable) {
        $("#dynamic-table_info").append("  到第 <input style='text-align: center;width: 50px; height: 20px' class='' id='changePage' type='text' value='" + pageNo + "'> 页 ");
        $('#changePage').keyup(function (e) {
            if (e.keyCode == 13) {
                if ($("#changePage").val() && $("#changePage").val() > 0) {
                    var redirectpage = $("#changePage").val() - 1;
                } else {
                    alert("请输入正确的页数");
                    $("#changePage").val("");
                    return;
                }
                oTable.fnPageChange(redirectpage);
            }
        });
    },
    go: function (url) {
        window.location.href = url;
    },
    alert: function (msg) {
        swal({title: msg});
    },
    confirm: function (msg, callback) {
        swal({
            title: msg,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            closeOnConfirm: false
        }, function () {
            callback.call(this);
        });
    },
    exportExcel: function (url) {
        this.exportFile("确定要导出为EXCEL吗？", url, 1);

    }, exportCsv: function (url) {
        alert(url);
        this.exportFile("确定要导出为CSV吗？", url, 2);

    }, exportFile: function (title, url, exportType) {
        swal({
            title: title,
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            closeOnConfirm: true
        }, function () {
            if (url.indexOf("?") != -1) {
                location.href = url + "&exportType=" + exportType;
            } else {
                location.href = url + "?exportType=" + exportType;
            }
        });

    }
});
