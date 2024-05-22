// 登录
function bindLoginClick(){
    document.getElementById("login-btn").addEventListener("click", function(event){
        // 阻止默认的事件
        event.preventDefault();

        // 获取表单数据
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        var formData = new FormData();
        formData.append("email", email);
        formData.append("password", password);
        $.ajax({
            url: "/auth/login",
            method: "POST",
            data: formData,
            processData: false, // 不要处理数据
            contentType: false, // 不要设置 Content-Type
            success: function(result){
                var code = result["code"];
                if (code == 200){
                    location.href="/device/devicelist";
                } else {
                    for (var key in result['data']){
                        $("#warning-message").text(result['data'][key]).show();
                        $("#warning-message").fadeOut(3000); // 300 毫秒的滑动效果
                    }
                }
            },
            error: function (error) {
              console.log(error);
            }
        });
    });
}

$(function () {
    bindLoginClick();
});
