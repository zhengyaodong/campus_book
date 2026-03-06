# -*- coding: utf-8 -*-
import requests
import json

base_url = "http://127.0.0.1:5000/api"

books = [
    # 教材类
    {"user_id": 1, "title": "高等数学(第七版)", "author": "同济大学数学系", "category": "教材类", "condition": "九成新", "price": 35.0, "description": "大学高等数学教材，内容完整，笔记较少", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "线性代数", "author": "同济大学", "category": "教材类", "condition": "八成新", "price": 20.0, "description": "线性代数教材，有少量笔记", "delivery_type": "自提", "stock": 1},
    {"user_id": 1, "title": "概率论与数理统计", "author": "浙江大学", "category": "教材类", "condition": "九成新", "price": 28.0, "description": "概率论教材，几乎全新", "delivery_type": "快递", "stock": 1},
    {"user_id": 1, "title": "大学英语精读(第三册)", "author": "李荫华", "category": "教材类", "condition": "七成新", "price": 15.0, "description": "大学英语教材，有一些笔记", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "数据结构与算法", "author": "严蔚敏", "category": "教材类", "condition": "八成新", "price": 30.0, "description": "数据结构经典教材", "delivery_type": "快递", "stock": 1},

    # 考研资料
    {"user_id": 1, "title": "考研政治核心考点", "author": "肖秀荣", "category": "考研资料", "condition": "九成新", "price": 45.0, "description": "2024考研政治复习资料", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "考研英语历年真题", "author": "张剑", "category": "考研资料", "condition": "八成新", "price": 38.0, "description": "英语真题汇编，含答案详解", "delivery_type": "快递", "stock": 1},
    {"user_id": 1, "title": "考研数学复习全书", "author": "李永乐", "category": "考研资料", "condition": "九成新", "price": 55.0, "description": "数学复习全书，全新未使用", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "408计算机专业基础", "author": "王道论坛", "category": "考研资料", "condition": "八成新", "price": 50.0, "description": "计算机统考408复习资料", "delivery_type": "自提", "stock": 1},
    {"user_id": 1, "title": "考研专业课真题集", "author": "目标院校", "category": "考研资料", "condition": "七成新", "price": 40.0, "description": "目标院校专业课真题", "delivery_type": "快递", "stock": 1},

    # 课外阅读
    {"user_id": 1, "title": "百年孤独", "author": "加西亚·马尔克斯", "category": "课外阅读", "condition": "九成新", "price": 25.0, "description": "经典文学名著，几乎全新", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "追风筝的人", "author": "卡勒德·胡赛尼", "category": "课外阅读", "condition": "八成新", "price": 18.0, "description": "感人至深的小说", "delivery_type": "快递", "stock": 1},
    {"user_id": 1, "title": "活着", "author": "余华", "category": "课外阅读", "condition": "九成新", "price": 15.0, "description": "余华经典之作", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "三体", "author": "刘慈欣", "category": "课外阅读", "condition": "八成新", "price": 30.0, "description": "科幻巨著全套", "delivery_type": "自提", "stock": 1},
    {"user_id": 1, "title": "人类简史", "author": "尤瓦尔·赫拉利", "category": "课外阅读", "condition": "七成新", "price": 22.0, "description": "通俗易懂的历史科普", "delivery_type": "快递", "stock": 1},
    {"user_id": 1, "title": "解忧杂货店", "author": "东野圭吾", "category": "课外阅读", "condition": "九成新", "price": 20.0, "description": "温情推理小说", "delivery_type": "自提+快递", "stock": 1},

    # 其他
    {"user_id": 1, "title": "牛津高阶英汉双解词典", "author": "牛津大学出版社", "category": "其他", "condition": "八成新", "price": 50.0, "description": "经典词典，工具书", "delivery_type": "自提+快递", "stock": 1},
    {"user_id": 1, "title": "新概念英语(全套)", "author": "亚历山大", "category": "其他", "condition": "七成新", "price": 60.0, "description": "1-4册全，包含自学指导", "delivery_type": "快递", "stock": 1},
    {"user_id": 1, "title": "日语N2语法精讲", "author": "日本语能力测试", "category": "其他", "condition": "九成新", "price": 35.0, "description": "日语N2考试资料", "delivery_type": "自提", "stock": 1},
    {"user_id": 1, "title": "吉他入门教程", "author": "人民音乐出版社", "category": "其他", "condition": "八成新", "price": 25.0, "description": "吉他初学者教材，含光盘", "delivery_type": "自提+快递", "stock": 1},
]

print("开始插入测试数据...")
for i, book in enumerate(books, 1):
    resp = requests.post(f"{base_url}/books", json=book)
    result = resp.json()
    if result.get('code') == 200:
        print(f"[{i}/{len(books)}] 成功: {book['title']}")
    else:
        print(f"[{i}/{len(books)}] 失败: {book['title']} - {result}")

print("\n测试数据插入完成!")
