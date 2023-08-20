from flask import Flask  # 从flask这个包中导入Flask类

app = Flask(__name__)  # 使用Flask类创建一个app对象


# __name__代表当前app.py这个文件
# 作用是：1、有助于快速定位bug；2、寻找模板文件时有相对路径


@app.route('/')  # 创建一个路由器和视图函数的映射，/代表根路由
# 以后访问这个根路由的时候，程序会自动调用hello_world函数，返回一个Hello World!的文本信息
def hello_world():
    return 'Hello AA!'


if __name__ == '__main__':  # 如果当前文件是程序的主入口文件，那么就运行这个代码
    app.run()
