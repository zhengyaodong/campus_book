# 订单路由模块
from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Order, Book
from datetime import datetime
import random
import string

order_bp = Blueprint('order', __name__)


def generate_order_no():
    """生成订单号"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.digits, k=6))
    return f'CB{timestamp}{random_str}'


@order_bp.route('', methods=['POST'])
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

    order = Order(
        order_no=generate_order_no(),
        user_id=user_id,
        book_id=book_id,
        address_id=address_id,
        total_price=book.price,
        status=1
    )

    book.stock -= 1

    db.session.add(order)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '订单创建成功', 'data': order.to_dict()})


@order_bp.route('', methods=['GET'])
def get_orders():
    """获取订单列表"""
    user_id = request.args.get('user_id', type=int)
    status = request.args.get('status', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    if not user_id:
        return jsonify({'code': 400, 'msg': '缺少用户ID'}), 400

    query = Order.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'code': 200,
        'data': {
            'items': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        }
    })


@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取订单详情"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404

    order_dict = order.to_dict()
    order_dict['address'] = order.address.to_dict() if order.address else None

    return jsonify({'code': 200, 'data': order_dict})


@order_bp.route('/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404

    if order.status != 1:
        return jsonify({'code': 400, 'msg': '只有待付款订单可以取消'}), 400

    order.status = 5

    if order.book:
        order.book.stock += 1

    db.session.commit()
    return jsonify({'code': 200, 'msg': '订单取消成功'})


@order_bp.route('/<int:order_id>/confirm', methods=['PUT'])
def confirm_receipt(order_id):
    """确认收货"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'msg': '订单不存在'}), 404

    if order.status != 3:
        return jsonify({'code': 400, 'msg': '只有待收货状态可以确认收货'}), 400

    order.status = 4
    db.session.commit()
    return jsonify({'code': 200, 'msg': '确认收货成功'})
