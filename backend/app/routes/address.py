# 地址路由模块
from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Address

address_bp = Blueprint('address', __name__)


@address_bp.route('', methods=['GET'])
def get_addresses():
    """获取地址列表"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'code': 400, 'msg': '缺少用户ID'}), 400

    addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc()).all()

    return jsonify({
        'code': 200,
        'data': [addr.to_dict() for addr in addresses]
    })


@address_bp.route('', methods=['POST'])
def create_address():
    """新增收货地址"""
    data = request.get_json()
    user_id = data.get('user_id')
    receiver = data.get('receiver', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    is_default = data.get('is_default', 0)

    if not all([user_id, receiver, phone, address]):
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400

    if is_default == 1:
        Address.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})

    addr = Address(
        user_id=user_id,
        receiver=receiver,
        phone=phone,
        address=address,
        is_default=is_default
    )
    db.session.add(addr)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '地址添加成功', 'data': addr.to_dict()})


@address_bp.route('/<int:addr_id>', methods=['PUT'])
def update_address(addr_id):
    """更新收货地址"""
    data = request.get_json()
    addr = Address.query.get(addr_id)
    if not addr:
        return jsonify({'code': 404, 'msg': '地址不存在'}), 404

    if 'receiver' in data:
        addr.receiver = data['receiver']
    if 'phone' in data:
        addr.phone = data['phone']
    if 'address' in data:
        addr.address = data['address']

    if data.get('is_default') == 1:
        Address.query.filter(Address.user_id == addr.user_id, Address.id != addr_id).update({'is_default': 0})
        addr.is_default = 1

    db.session.commit()
    return jsonify({'code': 200, 'msg': '地址更新成功', 'data': addr.to_dict()})


@address_bp.route('/<int:addr_id>', methods=['DELETE'])
def delete_address(addr_id):
    """删除收货地址"""
    addr = Address.query.get(addr_id)
    if not addr:
        return jsonify({'code': 404, 'msg': '地址不存在'}), 404

    db.session.delete(addr)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '地址删除成功'})
