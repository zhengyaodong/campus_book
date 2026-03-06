# Flask应用初始化模块
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from app.routes import user_bp, book_bp, order_bp, address_bp
        app.register_blueprint(user_bp, url_prefix='/api/user')
        app.register_blueprint(book_bp, url_prefix='/api/books')
        app.register_blueprint(order_bp, url_prefix='/api/orders')
        app.register_blueprint(address_bp, url_prefix='/api/addresses')

        db.create_all()

    return app
