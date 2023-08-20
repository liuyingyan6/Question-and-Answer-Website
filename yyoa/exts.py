# 存放引入的extensions插件
# 这个文件存在的意义就是为了解决循环引用问题 => models的db需要引入app，然后app又从models中引入UserModel
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 这里不把app传进来，否则会造成死循环 => app从引入models中引入UserModel，models中从exts引入db，exts的db又要引用app
# 另外，我们在app中给db绑定app，且指明是在初始化创建完db之后再与app进行绑定

from flask_mail import Mail

mail = Mail()
