# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

app = create_app()

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    """API路由代理"""
    from flask import request
    return app.full_dispatch(request)

@app.route('/')
def index():
    """前端页面路由"""
    from flask import send_from_directory
    return send_from_directory('../frontend/dist', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    """静态文件代理"""
    from flask import send_from_directory
    return send_from_directory('../frontend/dist', path)
