jQuery(function ($) {
    /** 表单提交* */
    $("#edit_submit").on('click', (function () {
        $('#edit_form').data('bootstrapValidator').resetForm();//清理历史错误
        $('#edit_form').bootstrapValidator('validate');
        if ($('#edit_form').data('bootstrapValidator').isValid()) {
            $("#edit_submit").attr({"disabled": "disabled"});
            $('#edit_form').ajaxSubmit({
                url: '/user/save',
                success: function (data) {
                    if (data.code == 1) {
                        $('#modal-default').modal("hide");
                        toastr.success("操作成功");
                        $('#dynamic-table').DataTable().ajax.reload(); //重新载入
                    } else {
                        toastr.error(data.msg);
                    }
                    $("#edit_submit").removeAttr("disabled");
                }
            });
            $("#edit_submit").removeAttr("disabled");
        }
        return false;
    }));

    $('#edit_form').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            userName: {
                selector: '#inputUserName',
                validators: {
                    notEmpty: {message: '不能为空！'}
                }
            }, email: {
                selector: '#inputEmail',
                validators: {
                    notEmpty: {message: '不能为空！'}
                }
            }, phone: {
                selector: '#inputPhone',
                validators: {
                    notEmpty: {message: '不能为空！'}
                }
            }
        }
    });
});