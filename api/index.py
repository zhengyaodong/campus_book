# -*- coding: utf-8 -*-
"""Vercel API路由入口"""
import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'campus_book.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============ 数据模型 ============
class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    nickname = db.Column(db.String(50))
    avatar = db.Column(db.String(255), default='')
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(100))
    created_at = db.Column(db.String(20))

class Book(db.Model):
    """书籍模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=1)
    delivery_type = db.Column(db.String(50))
    images = db.Column(db.Text, default='[]')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=1)
    created_at = db.Column(db.String(20))
    seller_nickname = db.Column(db.String(50))

class Order(db.Model):
    """订单模型"""
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    total_price = db.Column(db.Float)
    status = db.Column(db.Integer, default=1)
    created_at = db.Column(db.String(20))
    updated_at = db.Column(db.String(20))

class Address(db.Model):
    """地址模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_default = db.Column(db.Integer, default=0)

# ============ 工具函数 ============
def sha256(password):
    """SHA256加密"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_order_no():
    """生成订单号"""
    import time
    return f"ORD{int(time.time()*1000)}"

# ============ 用户接口 ============
@app.route('/api/user/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    nickname = data.get('nickname', username.split('@')[0] if '@' in username else username)
    
    if not username or not password:
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400
    
    if len(password) < 6 or len(password) > 20:
        return jsonify({'code': 400, 'msg': '密码长度需6-20位'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'}), 400
    
    import datetime
    user = User(
        username=username,
        password=sha256(password),
        email=email,
        nickname=nickname,
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '注册成功', 'data': {'id': user.id, 'username': user.username}})

@app.route('/api/user/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'code': 400, 'msg': '请输入用户名和密码'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or user.password != sha256(password):
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401
    
    return jsonify({
        'code': 200,
        'msg': '登录成功',
        'data': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'token': str(user.id)
        }
    })

@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 401, 'msg': '未登录'}), 401
    
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404
    
    return jsonify({'code': 200, 'data': {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.phone,
        'email': user.email,
        'created_at': user.created_at
    }})

@app.route('/api/user/profile', methods=['PUT'])
def update_profile():
    """更新用户信息"""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'code': 401, 'msg': '未登录'}), 401
    
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404
    
    if data.get('nickname'):
        user.nickname = data['nickname']
    if data.get('avatar'):
        user.avatar = data['avatar']
    if data.get('phone'):
        user.phone = data['phone']
    if data.get('email'):
        user.email = data['email']
    
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.phone,
        'email': user.email,
        'created_at': user.created_at
    }})

# ============ 书籍接口 ============
@app.route('/api/books', methods=['GET'])
def get_books():
    """获取书籍列表"""
    page = int(request.args.get('page', 1))
    category = request.args.get('category')
    
    query = Book.query.filter_by(status=1)
    if category:
        query = query.filter_by(category=category)
    
    books = query.order_by(Book.created_at.desc()).limit(20).all()
    total = query.count()
    
    return jsonify({'code': 200, 'data': {
        'items': [b.to_dict() for b in books],
        'total': total,
        'pages': 1,
        'current_page': page
    }})

@app.route('/api/books', methods=['POST'])
def create_book():
    """发布书籍"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    if not data.get('title') or not data.get('category') or not data.get('condition') or not data.get('price'):
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400
    
    user = User.query.get(int(user_id))
    import datetime
    book = Book(
        title=data['title'],
        author=data.get('author', ''),
        isbn=data.get('isbn', ''),
        category=data['category'],
        condition=data['condition'],
        price=float(data['price']),
        description=data.get('description', ''),
        stock=int(data.get('stock', 1)),
        delivery_type=data.get('delivery_type', ''),
        images=json.dumps(data.get('images', [])),
        user_id=int(user_id),
        status=1,
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        seller_nickname=user.nickname if user else ''
    )
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '发布成功', 'data': book.to_dict()})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取书籍详情"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404
    
    return jsonify({'code': 200, 'data': book.to_dict()})

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """更新书籍"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404
    
    if book.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    if data.get('title'): book.title = data['title']
    if data.get('author'): book.author = data['author']
    if data.get('category'): book.category = data['category']
    if data.get('condition'): book.condition = data['condition']
    if data.get('price'): book.price = float(data['price'])
    if data.get('description'): book.description = data['description']
    if data.get('stock'): book.stock = int(data['stock'])
    
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': book.to_dict()})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """删除书籍"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404
    
    if book.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """搜索书籍"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    condition = request.args.get('condition')
    page = int(request.args.get('page', 1))
    
    query = Book.query.filter_by(status=1)
    
    if keyword:
        query = query.filter(Book.title.like(f'%{keyword}%'))
    if category:
        query = query.filter_by(category=category)
    if min_price:
        query = query.filter(Book.price >= float(min_price))
    if max_price:
        query = query.filter(Book.price <= float(max_price))
    if condition:
        query = query.filter_by(condition=condition)
    
    books = query.order_by(Book.created_at.desc()).limit(20).all()
    total = query.count()
    
    return jsonify({'code': 200, 'data': {
        'items': [b.to_dict() for b in books],
        'total': total,
        'pages': 1,
        'current_page': page
    }})

# ============ 订单接口 ============
@app.route('/api/orders', methods=['POST'])
def create_order():
    """创建订单"""
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    address_id = data.get('address_id')
    
    if not all([user_id, book_id, address_id]):
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400
    
    book = Book.query.get(book_id)
    if not book or book.status != 1:
        return jsonify({'code': 404, 'msg': '书籍不存在或已下架'}), 404
    
    if book.stock < 1:
        return jsonify({'code': 400, 'msg': '书籍库存不足'}), 400
    
    import datetime
    order = Order(
        order_no=generate_order_no(),
        user_id=int(user_id),
        book_id=book_id,
        address_id=address_id,
        total_price=book.price,
        status=1,
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    book.stock -= 1
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '订单创建成功', 'data': order.to_dict()})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取订单列表"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    orders = Order.query.filter_by(user_id=int(user_id)).order_by(Order.created_at.desc()).all()
    
    return jsonify({'code': 200, 'data': {
        'items': [o.to_dict() for o in orders],
        'total': len(orders)
    }})

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取订单详情"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404
    
    return jsonify({'code': 200, 'data': order.to_dict()})

@app.route('/api/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """取消订单"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404
    
    if order.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    if order.status != 1:
        return jsonify({'code': 400, 'msg': '订单状态不可取消'}), 400
    
    book = Book.query.get(order.book_id)
    if book:
        book.stock += 1
    
    order.status = 4
    import datetime
    order.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '订单已取消'})

@app.route('/api/orders/<int:order_id>/confirm', methods=['PUT'])
def confirm_order(order_id):
    """确认收货"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404
    
    if order.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    if order.status != 3:
        return jsonify({'code': 400, 'msg': '订单状态不可确认'}), 400
    
    order.status = 5
    import datetime
    order.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '确认收货成功'})

# ============ 地址接口 ============
@app.route('/api/addresses', methods=['GET'])
def get_addresses():
    """获取地址列表"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 401, 'msg': '请先登录'}), 401
    
    addresses = Address.query.filter_by(user_id=int(user_id)).all()
    return jsonify({'code': 200, 'data': [a.to_dict() for a in addresses]})

@app.route('/api/addresses', methods=['POST'])
def create_address():
    """新增地址"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not all([user_id, data.get('receiver'), data.get('phone'), data.get('address')]):
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400
    
    if data.get('is_default'):
        Address.query.filter_by(user_id=int(user_id)).update({'is_default': 0})
    
    address = Address(
        user_id=int(user_id),
        receiver=data['receiver'],
        phone=data['phone'],
        address=data['address'],
        is_default=int(data.get('is_default', 0))
    )
    db.session.add(address)
    db.session.commit()
    
    return jsonify({'code': 200, 'msg': '地址添加成功', 'data': address.to_dict()})

@app.route('/api/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    """更新地址"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    address = Address.query.get(address_id)
    if not address:
        return jsonify({'code': 404, 'msg': '地址不存在'}), 404
    
    if address.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    if data.get('is_default'):
        Address.query.filter_by(user_id=int(user_id)).update({'is_default': 0})
    
    if data.get('receiver'): address.receiver = data['receiver']
    if data.get('phone'): address.phone = data['phone']
    if data.get('address'): address.address = data['address']
    if data.get('is_default') is not None: address.is_default = int(data['is_default'])
    
    db.session.commit()
    return jsonify({'code': 200, 'msg': '地址更新成功', 'data': address.to_dict()})

@app.route('/api/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """删除地址"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    address = Address.query.get(address_id)
    if not address:
        return jsonify({'code': 404, 'msg': '地址不存在'}), 404
    
    if address.user_id != int(user_id):
        return jsonify({'code': 403, 'msg': '无权限'}), 403
    
    db.session.delete(address)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '地址删除成功'})

# ============ 模型方法 ============
def to_dict(self):
    """转换为字典"""
    result = {}
    for col in self.__table__.columns:
        value = getattr(self, col.name)
        if isinstance(value, str):
            result[col.name] = value
        elif value is not None:
            result[col.name] = value
        else:
            result[col.name] = ''
    return result

User.to_dict = to_dict
Book.to_dict = to_dict
Order.to_dict = to_dict
Address.to_dict = to_dict

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
