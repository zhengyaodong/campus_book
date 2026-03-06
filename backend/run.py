# 应用入口
from app import create_app
from flask_cors import CORS  # 1. 导入 CORS

app = create_app()
print("CORS has been initialized!") # 加这行
CORS(app, supports_credentials=True) # 2. 核心：允许跨域请求

if __name__ == '__main__':
    import os
    # 建议使用系统分配的端口，增加稳定性
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)