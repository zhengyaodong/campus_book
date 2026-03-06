# 广州软件学院 校园二手交易平台

校园二手书籍交易平台，为广州软件学院师生提供便捷的二手书籍买卖服务。

## 项目介绍

本项目是一个前后端分离的校园二手书交易平台，采用 Vue 3 + Flask 技术栈开发。

## 技术栈

### 前端
- Vue 3
- Element Plus
- Pinia (状态管理)
- Vue Router
- Vite

### 后端
- Python Flask
- Flask-SQLAlchemy
- SQLite 3

## 功能特性

- 用户注册/登录
- 书籍发布与浏览
- 分类筛选
- 关键词搜索
- 订单管理
- 收货地址管理
- 个人资料管理

## 项目结构

```
CampusBook/
├── backend/              # 后端项目
│   ├── app/
│   │   ├── __init__.py  # Flask应用初始化
│   │   ├── models/      # 数据模型
│   │   └── routes/      # API路由
│   ├── config.py        # 配置文件
│   └── run.py           # 启动文件
│
├── frontend/             # 前端项目
│   ├── src/
│   │   ├── api/         # API接口
│   │   ├── router/      # 路由配置
│   │   ├── stores/      # 状态管理
│   │   └── views/       # 页面组件
│   ├── public/          # 静态资源
│   └── package.json
│
└── README.md
```

## 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 安装运行

#### 1. 克隆项目

```bash
git clone <repository-url>
cd CampusBook
```

#### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python run.py
```

后端服务将在 http://127.0.0.1:5000 启动

#### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 http://localhost:3000 启动

#### 4. 访问系统

打开浏览器访问 http://localhost:3000

## 默认测试账号

- 邮箱: test@example.com
- 密码: 123456

## API 接口

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 用户 | /api/user/register | POST | 用户注册 |
| 用户 | /api/user/login | POST | 用户登录 |
| 用户 | /api/user/profile | GET | 获取用户信息 |
| 用户 | /api/user/profile | PUT | 更新用户信息 |
| 书籍 | /api/books | GET | 获取书籍列表 |
| 书籍 | /api/books | POST | 发布书籍 |
| 书籍 | /api/books/:id | GET | 书籍详情 |
| 书籍 | /api/books/:id | PUT | 更新书籍 |
| 书籍 | /api/books/:id | DELETE | 删除书籍 |
| 书籍 | /api/books/search | GET | 搜索书籍 |
| 订单 | /api/orders | POST | 创建订单 |
| 订单 | /api/orders | GET | 订单列表 |
| 订单 | /api/orders/:id | GET | 订单详情 |
| 订单 | /api/orders/:id/cancel | PUT | 取消订单 |
| 订单 | /api/orders/:id/confirm | PUT | 确认收货 |
| 地址 | /api/addresses | GET | 地址列表 |
| 地址 | /api/addresses | POST | 新增地址 |
| 地址 | /api/addresses/:id | PUT | 更新地址 |
| 地址 | /api/addresses/:id | DELETE | 删除地址 |

## 页面路由

| 路径 | 页面 |
|------|------|
| / | 首页 |
| /login | 登录 |
| /register | 注册 |
| /book/:id | 书籍详情 |
| /publish | 发布书籍 |
| /category | 分类浏览 |
| /category/:type | 分类浏览 |
| /search | 搜索结果 |
| /orders | 我的订单 |
| /order/:id | 订单详情 |
| /address | 收货地址 |
| /profile | 个人资料 |

## 开发规范

- 使用中文注释
- 密码使用 SHA256 加密存储
- 防止 SQL 注入

## 许可证

MIT License
