function bindEmailCaptchaClick() {
    $("#captcha-btn").click(function (event) {
        // $this：代表的是当前按钮的jquery对象
        let $this = $(this);
        // 阻止默认的事件 => post表单的话就是提交表单
        event.preventDefault();

        let email = $("input[name='email']").val(); // .val获得input框中用户输入的值
        $.ajax({
            // http://127.0.0.1:500
            // /auth/captcha/email?email=xx@qq.com
            url: "/auth/captcha/email?email=" + email,
            method: "POST",
            success: function (result) {
                let code = result['code'];
                if (code == 200) {
                    let countdown = 60;
                    // 开始倒计时之前，就取消按钮的点击事件，倒计时结束后重新绑定点击事件
                    $this.off("click");
                    let timer = setInterval(function () {
                        $this.text(countdown + "秒后可重发"); // 让当前按钮的jquery对象的文本显示为倒计时
                        countdown -= 1;
                        // 倒计时结束的时候执行
                        if (countdown <= 0) {
                            // 清掉定时器
                            clearInterval(timer);
                            // 将按钮的文字重新修改回来
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000); // 每隔1s执行一次setInterval
                    // alert("邮箱验证码发送成功！");
                } else {
                    alert(result['message']);
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    });
}


// 整个网页都加载完毕后再执行的
$(function () {
    bindEmailCaptchaClick();
});