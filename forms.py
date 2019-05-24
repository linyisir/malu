from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField(
        label = '邮箱',
        validators = [
            InputRequired('邮箱不能为空'),
            Email('邮箱格式错误')
        ]
    )
    password = StringField(
        label='密码',
        validators=[
            InputRequired('密码不能为空'),
            Length(6, 9, '密码长度是6到9')
        ]
    )
    remenber = BooleanField(
        label='记住我'
    )

class RegistForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            InputRequired('昵称不能为空')
        ]
    )
    email = StringField(
        label='邮箱',
        validators=[
            InputRequired('邮箱不能为空'),
            Email('邮箱格式错误')
        ]
    )
    password = PasswordField(
        label='密码',
        validators=[
            InputRequired('密码不能为空'),
            Length(6, 9, '密码长度是6到9')
        ]
    )
    confirm = PasswordField(
        label='确认',
        validators=[
            InputRequired('密码不能为空'),
            EqualTo('password', '两次密码不一致')
        ]
    )

