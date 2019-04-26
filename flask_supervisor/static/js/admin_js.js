$(function() {

    $("#edit_userinfo").click(function(){
        $("#edit_user").show();
    })

    //首页、公共 Start
    $(".module_tips>.tip_close").click(function(){
        $(this).parent().hide(500);
    })

    //退出登录
    $(document).ready(function(){
        $("#logout").click(function(){
            layer.confirm('你确定要退出吗？', {icon: 3}, function(index){
                $.getJSON("/index.php/Admin/Entrance/logout",function(res){
                    if(res.code == 1){
                        lunhui.success(res.msg,res.url);
                    }else{
                        lunhui.error(res.msg);
                    }
                });
                layer.close(index);
            });
        });

        //安全退出
        $("#safelogout").click(function(){
            layer.confirm('你确定要退出吗？', {icon: 3}, function(index){
                $.getJSON("/index.php/Admin/Entrance/logout",function(res){
                    if(res.code == 1){
                        lunhui.success(res.msg,res.url);
                    }else{
                        lunhui.error(res.msg);
                    }
                });
                layer.close(index);
            });
        });
    });

    //清除缓存
    $(function(){
        $("#cache").click(function(){
            layer.confirm('你确定要清除缓存吗？', {icon: 3, title:'提示'}, function(index){
                $.getJSON("",function(res){
                    if(res.code == 1){
                        layer.msg(res.msg,{icon:1,time:2000,shade: 0.1});
                    }else{
                        layer.msg(res.msg,{icon:0,time:2000,shade: 0.1});
                    }
                });
                layer.close(index);
            })
        });
    });

     // 顶部菜单栏收缩及主题按钮
    $(function(){
        $("body").hasClass('mini-navbar') ? ($(".navbar-minimalize").find("i").removeClass().addClass('fa fa-indent')): ($(".navbar-minimalize").find("i").removeClass().addClass('fa fa-outdent'));
        $(".navbar-minimalize").click(function(){
            $("body").hasClass('mini-navbar') ? ($(".navbar-minimalize").find("i").removeClass().addClass('fa fa-indent')): ($(".navbar-minimalize").find("i").removeClass().addClass('fa fa-outdent'));
        })
    });



    // 顶部各个模块切换
    $(".top_menu").find('a').click(function(){
        $('.top_menu').find('li').removeClass('active');
        _modules = $(this).parent().addClass('active').attr('data-param');
        $("#side-menu>.menu").hide();
        $(".block_"+_modules).show();

    });

    // 菜单列表 Start
    $(function(){
        $('#add_rule').ajaxForm({
            beforeSubmit: checkForm,
            success: complete,
            dataType: 'json'
        });

        function checkForm(){
            //if($("#pid").val() == 0){
            //    layer.msg('请选择所属菜单导航',{icon:2,time:1500,shade: 0.1}, function(index){
            //        layer.close(index);
            //    });
            //    return false;
            //}

            if( '' == $.trim($('#title').val())){
                layer.msg('请输入菜单名称',{icon:2,time:1500,shade: 0.1}, function(index){
                    layer.close(index);
                });
                return false;
            }

            if( '' == $.trim($('#name').val())){
                layer.msg('控制器/方法不能为空',{icon:0,time:1500,shade: 0.1}, function(index){
                    layer.close(index);
                });
                return false;
            }
        }


        function complete(data){
            if(data.code==1){
                layer.msg(data.msg, {icon: 6,time:1500,shade: 0.1}, function(index){
                    window.location.href="./index";
                });
            }else{
                layer.msg(data.msg, {icon: 0,time:1500,shade: 0.1});
                return false;
            }
        }

    });




});


