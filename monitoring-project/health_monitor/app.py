import eventlet
eventlet.monkey_patch()  # Gọi ngay đầu file, trước khi import bất kỳ thứ gì khác

from flask import Flask
from flask_socketio import SocketIO
from routes import routes, socketio  # socketio được khởi tạo từ routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Khởi tạo Flask app
app = Flask(__name__)
socketio.init_app(app)  # Khởi tạo SocketIO với ứng dụng Flask

# Đăng ký các route từ routes.py
app.register_blueprint(routes)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8003)
