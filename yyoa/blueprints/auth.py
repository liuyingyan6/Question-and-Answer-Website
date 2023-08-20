# 存放所有用户、授权相关的模块
from flask import Blueprint, render_template, request, jsonify
from exts import mail, db
from flask_mail import Message
import string, random
from models import EmailCaptchaModel

bp = Blueprint("auth", __name__, url_prefix="/auth")  # 这个url_prefix相当于给所有路径加上前缀 => 类似@RequestMapping


@bp.route("/login")  # 实际在地址栏上要输入/auth/login才能使用
def login():
    return render_template("login.html")


# @bp.route如果没有指定methods参数，默认就是get请求
@bp.route("/captcha/email", methods=['POST'])
def get_email_captcha():
    email = request.args.get("email")  # /auth/captcha/email?email=123@qq.com

    source = string.digits * 4  # 随机产生4位数，string.digits * 4相当于是0123456789012345678901234567890123456789
    captcha = random.sample(source, 4)
    # print(captcha)  # ['1', '2', '8', '9']列表类型
    captcha = "".join(captcha)
    print(captcha)  # 1289

    # msg = Message("【yyoa】验证码", ["892901548@qq.com"], f"您的验证码是：{captcha}")
    # mail.send(msg)

    # 验证码的数据通常存在缓存中的，如memcached和redis，但是这里先用数据库储存
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": "l"})


@bp.route("/register")
def register():
    return render_template("register.html")


@bp.route("/mail/test")
def test_mail():
    msg = Message("test subject", ["892901548@qq.com"], "test body")
    mail.send(msg)
    return "ok"
