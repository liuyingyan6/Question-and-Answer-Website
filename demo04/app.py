from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate  # 作用是迁移ORM模型

app = Flask(__name__)

HOSTNAME = "127.0.0.1"  # ip地址
PORT = 3306  # 端口号
USERNAME = "root"  # 用户名
PASSWORD = "root"  # 密码
DATABASE = "flask_01"  # 数据库名字
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

db = SQLAlchemy(app)

# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中的连接信息

# 测试是否连接成功，打印出(1,)说明连接成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         result = conn.execute(text("select 1"))
#         print(result.fetchone())


migrate = Migrate(app, db)


# ORM模型映射成表的三步：
# 1、flask db init => 将flask初始化为类似git的migrations仓库 => 只需要执行一次 => 在项目里生成一个migrations文件夹
# 2、flask db migrate => 识别ORM模型的改变，生成迁移脚本 => migrations文件夹下的versions文件夹生成一个py文件
# 3、flask db upgrade => 运行迁移脚本，同步到数据库中 => 数据库中产生变化（还会有一个alembic_version表，记录当前迁移脚本的版本号
# 之后有任何修改的话只需要运行第2、3步即可


# 引入ORM对象关系映射
class User(db.Model):  # 这个是User类继承db.Model的意思
    __tablename__ = "user"  # 创建名为user的表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 创建列名id，类型为int，设置为主键，设置为自增
    username = db.Column(db.String(100), nullable=False)  # 创建列名username，类型为varchar（限制字数100），设置字段不可为空
    password = db.Column(db.String(100), nullable=False)  # 创建列名password，类型为varchar（限制字数100），设置字段不可为空
    email = db.Column(db.String(100), nullable=False)
    signature = db.Column(db.String(100), nullable=False)

    # # 如果Post使用了back_populates的话，在这里也需要做一个对应，否则会报错
    # posts = db.relationship("Post", back_populates="User")


class Post(db.Model):  # 用户发表的帖子
    __tablename__ = "post"  # 创建名为user的表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加外键，关联user表的id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 在Post里定义user属性，就可以使用post.user直接获取对应的作者信息，程序会找到与User表产生外键关系的字段（即user_id），根据这个字段到User表中查找内容
    # 相当于：post.user = User.query.get(post.user_id)
    # user = db.relationship("User",
    #                        back_populates="post")  # 添加了back_populates后，还可以使用user.posts获得用户的所有帖子，但是必须在User类中也定义一个post

    user = db.relationship("User", backref="posts")  # 用backref的话就不需要修改User类


# with app.app_context():
#     db.create_all()
#     # 注意使用creat_all的话有一个问题，就是如果数据库中已经存在了这些表，而我又在上面的类中进行了修改，比如增减了字段，使用creat_all的话都是不会识别到的


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/add')  # 添加
def add_user():
    user = User(username="kelly", password="kkk")  # 创建ORM对象
    db.session.add(user)  # 将ORM对象添加到db.session中
    db.session.commit()  # 将db.session中的操作同步到数据库中
    return '用户添加了~'


@app.route('/user/query')  # 查询
def query_user():
    # 1、查找一条数据：根据主键id查找
    user = User.query.get(1)
    # 这里可以直接在User类后面点出query函数，是因为User继承了db.Model
    print(f"{user.id}:{user.username}--{user.password}")

    print("-------------------")

    # 2、查找多条数据：使用filter_by，查找结果是一个Query类型的，可以理解为类对象的数组
    users = User.query.filter_by(username="kelly")
    print(type(users))  # <class 'flask_sqlalchemy.query.Query'>
    for usr in users:
        print(usr.username)
        print(usr.password)

    # 还有其他：like、in、or等等等等

    return '数据查找~'


@app.route('/user/update')  # 修改
def update_user():
    # 可以用.first或者[0]获得第一条数据，注意如果Query为空的话，[0]会报错
    user = User.query.filter_by(username="kelly")[0]
    user.password = "changed"  # 修改用户的信息，并自动存到session中
    db.session.commit()  # 将db.session中的操作同步到数据库中
    return '修改了用户信息~'


@app.route('/user/delete')  # 删除
def delete_user():
    user = User.query.get(1)  # 获取用户
    db.session.delete(user)  # 删除用户并存到session中
    db.session.commit()  # 提交session中的操作到数据库中
    return '删除了用户~'


@app.route('/post/add')  # 添加帖子
def add_post():
    post1 = Post(title="Django学习大全", content="Django学习大全xxxxxx")
    post1.user = User.query.get(2)

    post2 = Post(title="Flask学习大全", content="Flask学习大全xxxxxx")
    post2.user = User.query.get(3)

    db.session.add_all([post1, post2])
    db.session.commit()
    return '帖子添加了~'


@app.route('/post/query')  # 查询帖子
def query_post():
    post = Post.query.get(1)
    print(post.user)  # <User 2>
    print(post.user.username)  # kk

    user = User.query.get(2)
    for post in user.posts:
        print(post.title)

    return '查找到帖子~'


if __name__ == '__main__':
    app.run()
