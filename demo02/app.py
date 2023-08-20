from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user')  # 自定义路径
def user():
    return 'user center'


@app.route('/user/list')  # 多级路径
def users():
    return 'user list'


@app.route('/user/<user_id>')  # 将参数固定到path中
def user_detail(user_id):
    return 'user id = %s' % user_id


@app.route('/user/test_int/<int:user_int_id>')  # 限制参数类型
def user_detail_int(user_int_id):
    return 'user int id = %s' % user_int_id


@app.route('/book/list')
# /book/list        默认给第一页的数据
# /book/list?page=2 给第二页的数据
# 需要先在最前面引入request => from flask import Flask, request
def book_list():
    page = request.args.get("page", default=1, type=int)
    return f"您获得的是第{page}页的图书列表!"


if __name__ == '__main__':
    app.run()
