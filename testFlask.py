from flask import Flask
from flask import render_template
from flask import request, g

from flask_wtf import CSRFProtect
from forms import LoginForm, RegistForm

# from models import User, findById, findByEmail

from flask import redirect, url_for

from tools import login_required

from bluePoint import bp

from flask import abort
from uuid import uuid4
from flask import session

from models import db, User

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(bp) # 注册蓝图
db.init_app(app) # 注册sqlalchemy
CSRFProtect(app) # 注册csrfprotect

def gen_token():
    token = str(uuid4()) # 生成一个token
    session['csrf_token'] = token # 将token放到session中去
    return token

app.jinja_env.globals.update({'gen_token':gen_token}) # 将gen_token方法放到模板的全局变量中去

@app.before_first_request # 这个钩子通常用来初始化数据库
def init_db():
    print("第一次")
    db.create_all() # 初始化数据库

@app.before_request
def csrf_protect():
    if request.method == 'POST':
        form_token = request.form.get('csrf_token', None)
        session_token = session.get('csrf_token', None)
        if form_token != session_token:
            abort(403, 'You are hacker!')


@app.before_request
def login_before_request():
    # userId = request.cookies.get('userId', None)
    userId = session.get('userId', None)
    # user = findById(userId) # 模拟数据库时用
    user = User.query.filter_by(id=userId).first()  # 使用数据库中的数据时使用
    g.user = user

@app.route('/')
@login_required
def index():
    # userId = request.cookies.get('userId', None)  # 进入主页面时获取cookie数据
    # user = findById(userId) # 根据获取到的cookie数据

    username = None
    if g.user:
        username = g.user.name
    return render_template('index.html', username=username)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        next = request.args.get('next', None)
        print('请求路径为', next)
        return render_template('login.html', form = form, next = next)
    else:
        form = LoginForm(request.form)
        if form.validate():
            print('格式验证成功')
            email = form.email.data
            print(email)
            password = form.password.data
            # user = findByEmail(email) # 模拟数据库时用
            user = User.query.filter_by(email=email).first()  # 使用数据库中的数据时使用 # 注意：.first()的作用是将查询到的数据转化成一个对象
            if user:
                print('邮箱正确')
                if user.check_password(password):
                    print('密码正确')
                    # resp = redirect(url_for('index')) # 邮箱和密码都正确时就重定向到主页面
                    endpoint = request.form.get('next', None)
                    resp = redirect(url_for(endpoint))
                    age = form.remenber.data and 678400 or None # 如果勾选了记住我,cookie的事件就进行相应延长
                    # resp.set_cookie('userId', str(user.id), max_age=age) # 邮箱和密码都正确时就将用户的ID放到cookie中去
                    session['userId'] = str(user.id) # 利用sesssion存cookie数据
                    return resp;
                else:
                    print('密码错误')
                    info = {
                        'password': '密码错误'
                    }
                    return render_template('login.html', form=form, **info)
            else:
                print('邮箱错误')
                info = {
                    'email': '该邮箱未注册'
                }
                form = LoginForm()
                return render_template('login.html', form = form, **info)
        else:
            info = form.errors  # 获取错误信息(结果是一个字典)
            form = LoginForm()
            return render_template('login.html', form = form, **info) # 格式验证失败就重定向到登录页面

# 模拟CSRF攻击时用
@app.route('/dosth/', methods=['post', 'get'])
@login_required
def dosth():
    print('做了一些事')
    return '做了一些事'

# 注销登录状态（就是将session数据清空）
@app.route('/logout/')
def layout():
    print('注销前：', session.get('userId', None))
    session.pop('userId')
    print('注销后：', session.get('userId', None))
    if session.get('userId', None):
        print('注销失败')
    else:
        print('注销成功')
    return redirect(url_for('index')) # 注销成功与否都会重定向到主页面
# 如果注销成功，就没有登录状态啦；当请求主页面是会自动渲染登录页面


@app.route('/regist/', methods=['post', 'get'])
def regist():
    if request.method == 'GET':
        form = RegistForm()
        return render_template('regist.html', form = form)
    else:
        form = RegistForm(request.form)
        if form.validate():
            print('格式正确')
            if User.query.filter_by(email=form.email.data)[:]:
                return '该邮箱已经注册'
            user = User(str(uuid4()), form.email.data, form.name.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            print('hello boy')
            return '注册成功'
        else:
            return str(form.errors)

print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)
