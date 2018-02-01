function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
    });
})

$(document).ready(function(){
    $('.form-login').submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
    

    var req_data={
        mobile:mobile,
        passwd:passwd,
    }

    $.ajax({
        url:'/api/login',
        type:'post',
        data:JSON.stringify(req_data),
        contentType:'application/json',
        dataType:'json',
        headers:{
            "X-XSRFTOKEN":getCookie("_xsrf"),
        },
        success:function (data){
            if (data.errmg=='手机号错误'){
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            };
            if (data.errmg=='账号或密码错误'){
               $("#password-err span").html("账号或密码错误!");
                $("#password-err").show(); 
            };
            if (data.errmg == '用户不存在'){
                $("#password-err span").html("用户不存在!");
                $("#password-err").show(); 
            };
            if (data.errmg == '数据库错误'){
                // $("#password-err span").html("用户不存在!");
                // $("#password-err").show(); 
                alert('qqqqeeeeeeee')
            };
            if (data.errmg =='OK'){
                window.location.href = 'index.html'
                }
            }
        })
    
    })
})