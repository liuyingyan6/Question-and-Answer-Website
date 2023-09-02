import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db


# Form: 验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式有误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式有误")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名长度不符合标准")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不符合标准")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 检查邮箱是否已经被注册
    def validate_email(self, field):  # 这里的field代表email这个字段
        # self 是一个特殊的参数，它代表类的实例对象（即通过类创建的对象）自身，在这里则代表了 RegisterForm 类的实例对象
        # 注意：validate_字段 这个方法名不能随便修改，它代表对表格中特定字段的自定义验证
        register_email = field.data  # 使用field.data获得email的值
        user = UserModel.query.filter_by(email=register_email).first()  # 从mysql数据库中的user表查找email字段与注册的email相同的用户
        if user:  # 如果存在该用户的话，说明email已被注册
            raise wtforms.ValidationError(message="该邮箱已被注册")  # 抛异常提示错误信息

    # 检查验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data  # 获得验证码的值
        email = self.email.data  # 获得邮箱地址的值
        captcha_model = EmailCaptchaModel.query.filter_by(email=email,
                                                          captcha=captcha).first()  # 从mysql数据库的email_captcha表查找email字段和captcha字段符合的用户
        if not captcha_model:  # 如果找不到，说明验证码对不上
            raise wtforms.ValidationError(message="验证码错误")  # 抛异常
        else:  # 如果找得到
            db.session.delete(captcha_model)  # 可以把验证码从数据库中删除
            db.session.commit()  # 提交改动


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式有误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不符合标准")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题长度不符合标准")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容长度不符合标准")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容长度不符合标准")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须传入问题id")])
