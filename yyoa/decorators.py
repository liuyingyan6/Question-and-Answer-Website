from functools import wraps
from flask import g, redirect, url_for


# 装饰器函数
def login_required(func):
    @wraps(func)  # 保留被装饰函数的元数据
    def inner(*args, **kwargs):  # 定义内部函数inner，它接受任意参数和关键字参数
        if g.user:  # 如果用户已登录
            return func(*args, **kwargs)  # 则调用被装饰的函数func并返回其结果
        else:  # 如果用户未登录
            return redirect(url_for("auth.login"))  # 重定向到登陆页面

    return inner  # return inner返回内部函数inner作为装饰器的结果
# 内部函数inner是装饰器函数的实际装饰逻辑。它接受被装饰函数的参数，并在内部进行一些额外的操作，类似java中的动态代理/AOP
