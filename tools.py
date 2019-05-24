from functools import wraps
from flask import g, request
from flask import redirect,url_for

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if g.user:
            return func(*args, **kw)
        else:
            endpoint = request.endpoint # 获取请求路径的端点
            print(endpoint)
            return redirect(url_for('login', next=endpoint)) # 将端点作为重定向路径的参数
    return wrapper
