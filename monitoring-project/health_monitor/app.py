from flask import Flask
from routes import routes
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Khởi tạo Flask app
app = Flask(__name__)

# Đăng ký các route từ routes.py
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)  # Ứng dụng chạy trên cổng 8003
