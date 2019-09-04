$(document).ready(function () {
    selectMenu("oneMenu-id|teacherMenu-id");

    function getOperate(userCode) {
        var opHtml = '<li><a href="javascript:void(0);"  onclick="edit(\'' + userCode + '\')">编辑</a></li>'
            + '<li class="divider"></li>'
            + '<li><a href="javascript:void(0);"  onclick="del(\'' + userCode + '\');">删除</a></li>';
        return $.getOperateHtml(opHtml);
    }

    var table = $('#dynamic-table').DataTable({
        "serverSide": true,// 服务器端分页处理
        "bAutoWidth": false,
        "bProcessing": true, //DataTables载入数据时，是否显示‘进度’提示
        "aLengthMenu": [5, 10, 20, 50], //更改显示记录数选项
        "iDisplayLength": 10, //默认显示的记录数
        "searching": false,
        "bInfo": true, //是否显示页脚信息，DataTables插件左下角显示记录数
        "sPaginationType": "full_numbers", //详细分页组，可以支持直接跳转到某页
        "bSort": false, //是否启动各个字段的排序功能
        "language": {
            url: '/static/i18n/chinese.json'
        },
        fnDrawCallback: function (table) {
            var pageNo = (table.oAjaxData.start / table.oAjaxData.length) + 1;
            var oTable = $("#dynamic-table").dataTable();
            $.skipPage(pageNo, oTable);
        },
        columns: [
            {"data": "userCode", "defaultContent": ""},
            {"data": "userName", "defaultContent": ""},
            {
                "data": "gender", "defaultContent": "", "render": function (data, type, row) {
                    var val = "";
                    if (row.gender === 1) {
                        val = '男'
                    } else if (row.gender === 0) {
                        val = '女'
                    }
                    return '<span>' + val + '</span>';
                }
            },
            {"data": "email", "defaultContent": ""},
            {"data": "phone", "defaultContent": ""},
            {"data": "familyPhone", "defaultContent": ""},
            {"data": "remark", "defaultContent": ""},
            {
                "data": null,
                "render": function (data, type, row) {
                    return getOperate(row.userCode);
                }
            }
        ],
        ajax: function (data, callback, settings) {
            var param = {};
            param.pageSize = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候
            param.start = data.start;//开始的记录序号
            param.page = (data.start / data.length) + 1;//当前页码
            param.draw = data.draw;
            var x = $("#queryForm").serializeArray();
            $.each(x, function (i, field) {
                param[field.name] = field.value;
            });
            param['role']=1;
            $.ajax({
                type: "post",
                url: "/user/list",
                cache: false,	//禁用缓存
                data: param,	//传入已封装的参数
                dataType: "json",
                success: function (result) {
                    /*if (result.code!=1) {
                        $.dialog.alert("查询失败。错误码：" + result.errorCode);
                        return;
                    }*/
                    var returnData = {};
                    returnData.draw = data.draw;//这里直接自行返回了draw计数器,应该由后台返回
                    returnData.recordsTotal = result.total;
                    returnData.recordsFiltered = result.total;//后台不实现过滤功能，每次查询均视作全部结果
                    returnData.data = result.rows;
                    callback(returnData);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    toastr.error("查询失败");
                }
            });
        }
    });

    //查询按钮
    $("#submitQuery").on('click', function () {
        table.ajax.reload();
    });

    //重置按钮
    $("#resetQuery").on('click', function () {
        $('#queryForm')[0].reset();
        table.ajax.reload();
    });

    //新增按钮 显示$('#modal-default').show(); 隐藏$('#modal-default').modal("hide");
    $("#addDataBtn").on('click', function () {
        $('#inputUserCode').val('');
        $('#modal-default').modal('show');
        $('#edit_form').resetForm();
    });
});

function edit(userCode) {
    $.ajax({
        type: "POST",
        async: false,
        dataType: "json",
        url: "/user/edit?userCode=" + userCode,
        success: function (res) {
            if (res.code == 1) {
                var data = res.data;
                $("#inputUserCode").val(data.userCode);
                $("#inputUserName").val(data.userName);
                $("#inputSex").val(data.gender);
                $("#inputEmail").val(data.email);
                $("#inputPhone").val(data.phone);
                $("#inputFamilyPhone").val(data.familyPhone);
                $("#inputRemark").val(data.remark);
                $('#modal-default').modal('show');
            } else {

            }
        }

    });
}

//删除
function del(userCode) {
    bootbox.confirm("您确定要删除吗", function (result) {
        if (result) {
            $.post("/user/delete", {userCode: userCode}, function (result) {
                debugger;
                if (result.code === 1) {
                    toastr.success("操作成功");
                    $('#dynamic-table').DataTable().ajax.reload(); //重新载入
                } else {
                    toastr.error(result.msg);
                }
            }, "json");
        }
    });
}