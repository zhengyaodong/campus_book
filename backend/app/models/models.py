# 数据库模型模块
from app import db
from datetime import datetime
import hashlib

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, comment='用户名(邮箱/手机)')
    password = db.Column(db.String(256), nullable=False, comment='密码(加密)')
    nickname = db.Column(db.String(50), default='新用户', comment='昵称')
    avatar = db.Column(db.String(255), default='', comment='头像URL')
    phone = db.Column(db.String(20), default='', comment='手机号')
    email = db.Column(db.String(100), default='', comment='邮箱')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='注册时间')

    books = db.relationship('Book', backref='seller', lazy='dynamic')
    orders = db.relationship('Order', backref='buyer', lazy='dynamic')
    addresses = db.relationship('Address', backref='user', lazy='dynamic')

    @staticmethod
    def hash_password(password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """验证密码"""
        return self.password == self.hash_password(password)

    def to_dict(self):
        """用户信息转字典"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Book(db.Model):
    """书籍模型"""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='书名')
    author = db.Column(db.String(100), default='', comment='作者')
    isbn = db.Column(db.String(20), default='', comment='ISBN')
    category = db.Column(db.String(50), nullable=False, comment='分类')
    condition = db.Column(db.String(20), nullable=False, comment='成色')
    price = db.Column(db.Float, nullable=False, comment='价格')
    description = db.Column(db.Text, default='', comment='描述')
    stock = db.Column(db.Integer, default=1, comment='库存')
    delivery_type = db.Column(db.String(20), nullable=False, comment='交易方式')
    images = db.Column(db.Text, default='[]', comment='图片JSON')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='卖家ID')
    status = db.Column(db.Integer, default=1, comment='状态(1:上架 0:下架)')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='发布时间')

    orders = db.relationship('Order', backref='book', lazy='dynamic')

    def to_dict(self):
        """书籍信息转字典"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'condition': self.condition,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'delivery_type': self.delivery_type,
            'images': self.images,
            'user_id': self.user_id,
            'seller_nickname': self.seller.nickname if self.seller else '',
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False, comment='订单号')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='买家ID')
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, comment='书籍ID')
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False, comment='收货地址ID')
    total_price = db.Column(db.Float, nullable=False, comment='总价')
    status = db.Column(db.Integer, default=1, comment='订单状态(1:待付款 2:待发货 3:待收货 4:已完成 5:已取消)')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """订单信息转字典"""
        return {
            'id': self.id,
            'order_no': self.order_no,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else '',
            'book_price': self.book.price if self.book else 0,
            'address_id': self.address_id,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Address(db.Model):
    """收货地址模型"""
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    receiver = db.Column(db.String(50), nullable=False, comment='收货人')
    phone = db.Column(db.String(20), nullable=False, comment='电话')
    address = db.Column(db.String(255), nullable=False, comment='地址')
    is_default = db.Column(db.Integer, default=0, comment='是否默认(1:是 0:否)')

    orders = db.relationship('Order', backref='address', lazy='dynamic')

    def to_dict(self):
        """地址信息转字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'receiver': self.receiver,
            'phone': self.phone,
            'address': self.address,
            'is_default': self.is_default
        }
