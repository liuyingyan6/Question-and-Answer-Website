from flask import Flask, render_template
from datetime import datetime

# render_template底层就是Jinja2模板引擎

app = Flask(__name__)


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


# 自定义过滤器
def datetime_format(value, format="%Y年 %m月 %d日 %H:%M:%S"):
    return value.strftime(format)


# 整个app引入自定义的过滤器
# dformat是给过滤器取的名字
app.add_template_filter(datetime_format, "dformat")


@app.route('/static')
def test_static():
    return render_template("static.html")


@app.route('/child1')
def child1():
    return render_template("child1.html")


@app.route('/child2')
def child2():
    return render_template("child2.html")


@app.route('/control/<int:age>')
def control(age):
    # 列表books中包含多个字典
    books = [
        {"name": "三国演义", "author": "罗贯中"},
        {"name": "水浒传", "author": "施耐庵"}
    ]
    return render_template("control.html", age=age, books=books)


@app.route('/filter')
def test_filter():
    jenny = User(username="jenny", email="jenny@outlook.com")  # 参数一定要写全
    my_time = datetime.now()
    return render_template("filter.html", user=jenny, time=my_time)


@app.route('/test_class')  # 传入参数为类
def test_class():
    aa = User(username="AA", email="aa@outlook.com")
    return render_template("test_class.html", user=aa)


@app.route('/test_dictionary')  # 传入参数为字典类型
def test_dictionary():
    kk = {
        "person_name": "kk",
        "email": "kk@aol.com"
    }
    return render_template("test_dictionary.html", person=kk)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/blog/<blog_id_path>')
def blog_detail(blog_id_path):
    return render_template("blog_detail.html", blog_id=blog_id_path, username="无名")


if __name__ == '__main__':
    app.run()
