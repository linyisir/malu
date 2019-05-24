from flask import Blueprint
from flask import session

bp = Blueprint('session', __name__)

@bp.route('/get/')
def get():
    info = session.get('info', None)
    print(info)
    return '获取cookie数据成功'

@bp.route('/set/')
def set():
    session['info'] = str('warrior')
    return '设置cookie数据成功'