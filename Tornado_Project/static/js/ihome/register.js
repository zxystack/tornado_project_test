function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    var preImageCodeId = imageCodeId;
    imageCodeId = generateUUID();
    $(".image-code img").attr("src", "/api/imagecode?pcodeid="+preImageCodeId+"&codeid="+imageCodeId);
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    // 错误，传送的数据不是json格式
    // $.post("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId}, 
    //     function(data){
    //         if (0 != data.errno) {
    //             $("#image-code-err span").html(data.errmsg); 
    //             $("#image-code-err").show();
    //             if (2 == data.errno || 3 == data.errno) {
    //                 generateImageCode();
    //             }
    //             $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //         }   
    //         else {
    //             var $time = $(".phonecode-a");
    //             var duration = 60;
    //             var intervalid = setInterval(function(){
    //                 $time.html(duration + "秒"); 
    //                 if(duration === 1){
    //                     clearInterval(intervalid);
    //                     $time.html('获取验证码'); 
    //                     $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //                 }
    //                 duration = duration - 1;
    //             }, 1000, 60); 
    //         }
    // }, 'json'); 
    var req_data = {
        mobile:mobile, 
        image_code_text:imageCode, 
        image_code_id:imageCodeId,
    };
    $.ajax({
        url:"/api/smscode",
        type:"post",
        data: JSON.stringify(req_data),
        contentType:"application/json",
        dataType:"json",
        headers:{
            "X-XSRFTOKEN":getCookie("_xsrf"),
        },
        success:function (data) {
            if ("0" != data.errno) {
                $("#image-code-err span").html(data.errmsg); 
                $("#image-code-err").show();
                if ("4001" == data.errno || "4002" == data.errno || "4004" == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
            }
        }
    });
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;

        }

        var req_data2 = {
            mobile:mobile,
            phoneCode:phoneCode,
            passwd:passwd,
        };


        $.ajax({
            url:'/api/register',
            type:"post",
            data:JSON.stringify(req_data2),
            contentType:'application/json',
            dataType:'json',
            headers:{
                 "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success:function (data) {
                if (data.errmsg=='用户已经存在'){
                    $("#mobile-err span").html("用户已经存在");
                    $("#mobile-err").show();
                    return;
                }

                if (data.errmsg=='密码格式不正确'){
                    $("#password2-err span").html("首字母开头");
                    $("#password2-err").show();
                    alert(data.errmsg)
                    return;
                }
                if (data.errmsg=='密码位数不正确'){
                    $("#password2-err span").html("输入6-16位密码");
                    $("#password2-err").show();
                    return;
                }
                if (data.errmsg=='OK'){
                    alert('注册成功')
                    window.location.href = 'login.html'
                }
                
                }
            

        })

    });

     

})  




       