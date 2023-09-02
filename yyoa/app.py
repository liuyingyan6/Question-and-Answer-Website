from flask import Flask, session, g
import config  # 引入我们自己写的config.py
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定自己写的配置文件config.py
app.config.from_object(config)

db.init_app(app)  # 将已经创建好的db对象与app进行绑定
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# 在Flask中，有以下5个常用的钩子函数：
# before_first_request：在处理第一个请求之前执行。通常用于初始化操作。
# before_request：在每个请求之前执行。可以用于在处理请求之前进行一些共通的操作，如验证用户身份、检查访问权限等。
# after_request：在每个请求之后执行，无论是否发生了异常。可以用于修改响应、添加响应头等操作。
# teardown_request：在每个请求之后执行，仅在请求发生异常时不执行。可以用于释放资源、关闭数据库连接等操作。

@app.before_request  # 拦截请求
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)  # g是用来储存全局变量的

    else:
        setattr(g, "user", None)


@app.context_processor  # 上下文处理器
def my_context_processor():  # 在这个方法里面返回什么变量，那么模板里就会有这个变量
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
