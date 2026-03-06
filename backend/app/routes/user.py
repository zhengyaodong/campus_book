# 用户路由模块
from flask import Blueprint, request, jsonify
from app import db
from app.models.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    nickname = data.get('nickname', '新用户')
    phone = data.get('phone', '')
    email = data.get('email', '')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400

    if len(password) < 6 or len(password) > 20:
        return jsonify({'code': 400, 'msg': '密码长度需6-20位'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'}), 400

    user = User(
        username=username,
        password=User.hash_password(password),
        nickname=nickname,
        phone=phone,
        email=email
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '注册成功', 'data': user.to_dict()})


@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401

    return jsonify({'code': 200, 'msg': '登录成功', 'data': user.to_dict()})


@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'code': 400, 'msg': '缺少用户ID'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404

    return jsonify({'code': 200, 'data': user.to_dict()})


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """更新用户信息"""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'msg': '缺少用户ID'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404

    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'avatar' in data:
        user.avatar = data['avatar']

    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': user.to_dict()})
