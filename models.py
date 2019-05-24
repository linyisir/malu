from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, id, email, name, password): # 类似与java中的构造器
        self.id = id
        self.email = email
        self.name = name
        self.password = self.set_password(password)

    def set_password(self, password): # 对明文密码进行加密，返回的是加密后的密码
        return generate_password_hash(password)

    def check_password(self, password): # 检查密码，传入的是明文密码，会将明文密码进行加密后再进行比对
        return check_password_hash(self.password, password)

    def change_password(self, password): # 修改密码
        self.password = self.set_password(password)




# class User:
#     def __init__(self, id, email, name, password):
#         self.id = id
#         self.email = email
#         self.name = name
#         self.password = password
#
#     def check_password(self, password):
#         return self.password == password
#
# users = [
#     User('1', 'fury@163.com', 'fury', '111111'),
#     User('2', 'zeus@163.com', 'zeus', '222222'),
#     User('3', 'warrior@163.com', 'warrior', '333333')
# ]
#
# def findById(userId):
#     for user in users:
#         if user.id == userId:
#             return user
#     else:
#         return None
#
# def findByEmail(email):
#     for user in users:
#         if user.email == email:
#             return user
#     else:
#         return None