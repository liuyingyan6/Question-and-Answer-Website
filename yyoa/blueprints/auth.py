# 存放所有用户、授权相关的模块
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string, random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")  # 这个url_prefix相当于给所有路径加上前缀 => 类似@RequestMapping


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


@bp.route("/register", methods=['GET', 'POST'])  # 这个函数只能用get或者post请求
def register():
    if request.method == 'GET':  # 如果get请求进入
        return render_template("register.html")  # 则返回渲染视图
    else:  # 因为规定了只能用get、post，所以剩下只有post请求
        form = RegisterForm(request.form)  # 调用forms.py里的验证器
        if form.validate():  # 如果通过了验证
            email = form.email.data  # 获得邮箱地址的值
            username = form.username.data  # 获得用户名
            password = form.password.data  # 获得密码
            user = UserModel(email=email, username=username, password=generate_password_hash(
                password))  # 到mysql数据库中新建一行存起来，密码用了generate_password_hash进行加密处理
            db.session.add(user)  # 添加到表格
            db.session.commit()  # 提交变更
            return redirect(url_for("auth.login"))  # 重定向至登录页面
        # url_for的作用是通过视图函数/蓝图的名称生成对应的 URL
        else:  # 如果没通过验证
            print(form.errors)  # 把错误信息打印出来
            return redirect(url_for("auth.register"))  # 重定向至注册页面重新填写


@bp.route("/login", methods=['GET', 'POST'])  # 实际在地址栏上要输入/auth/login才能使用
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)  # 使用forms.py里的LoginForm验证方法
        if form.validate():  # 如果通过验证
            email = form.email.data  # 获取email、password的值
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()  # 从数据库user表中找到email对应的用户
            if not user:  # 找不到则代表邮箱错误
                print("邮箱或密码错误")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,
                                   password):  # 使用check_password_hash把该用户加密后的密码给前端传过来的明文密码进行对比 => 注意要在config.py中配置SECRET_KEY作为盐
                session['user_id'] = user.id  # session存储用户id
                return redirect("/")  # 重定向至首页
            else:
                print("邮箱或密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/mail/test")
def test_mail():
    msg = Message("test subject", ["892901548@qq.com"], "test body")
    mail.send(msg)
    return "ok"


@bp.route("/register_mine")
def register_mine():
    return render_template("/mine/register_mine.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/login_mine")
def login_mine():
    return render_template("/mine/login_mine.html")
