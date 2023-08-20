from flask import Flask
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


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
