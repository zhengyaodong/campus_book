# 书籍路由模块
from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Book

book_bp = Blueprint('book', __name__)


@book_bp.route('', methods=['GET'])
def get_books():
    """获取书籍列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    category = request.args.get('category')

    query = Book.query.filter_by(status=1)
    if category:
        query = query.filter_by(category=category)

    books = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'code': 200,
        'data': {
            'items': [book.to_dict() for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': page
        }
    })


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取书籍详情"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404

    return jsonify({'code': 200, 'data': book.to_dict()})


@book_bp.route('', methods=['POST'])
def create_book():
    """发布书籍"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title', '').strip()

    if not user_id:
        return jsonify({'code': 400, 'msg': '缺少用户ID'}), 400
    if not title:
        return jsonify({'code': 400, 'msg': '书名不能为空'}), 400

    required_fields = ['category', 'condition', 'price', 'delivery_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'msg': f'{field}不能为空'}), 400

    book = Book(
        title=title,
        author=data.get('author', ''),
        isbn=data.get('isbn', ''),
        category=data['category'],
        condition=data['condition'],
        price=float(data['price']),
        description=data.get('description', ''),
        stock=data.get('stock', 1),
        delivery_type=data['delivery_type'],
        images=data.get('images', '[]'),
        user_id=user_id,
        status=1
    )
    db.session.add(book)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '发布成功', 'data': book.to_dict()})


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """更新书籍"""
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404

    updatable_fields = ['title', 'author', 'isbn', 'category', 'condition', 'price', 'description', 'stock', 'delivery_type', 'images', 'status']
    for field in updatable_fields:
        if field in data:
            setattr(book, field, data[field])

    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': book.to_dict()})


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """删除书籍"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'code': 404, 'msg': '书籍不存在'}), 404

    book.status = 0
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})


@book_bp.route('/search', methods=['GET'])
def search_books():
    """搜索书籍"""
    keyword = request.args.get('keyword', '').strip()
    category = request.args.get('category')
    condition = request.args.get('condition')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = 20

    query = Book.query.filter_by(status=1)

    if keyword:
        query = query.filter(Book.title.like(f'%{keyword}%'))

    if category:
        query = query.filter_by(category=category)

    if condition:
        query = query.filter_by(condition=condition)

    if min_price is not None:
        query = query.filter(Book.price >= min_price)

    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    books = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'code': 200,
        'data': {
            'items': [book.to_dict() for book in books.items],
            'total': books.total,
            'pages': books.pages,
            'current_page': page
        }
    })
