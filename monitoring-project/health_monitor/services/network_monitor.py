import time
import psutil
from services.data_store import network_data

def monitor_network_bandwidth(app, socketio_instance):
    with app.app_context():
        while True:
            try:
                # Lấy thông tin băng thông mạng
                net_io = psutil.net_io_counters()
                bytes_sent = net_io.bytes_sent
                bytes_recv = net_io.bytes_recv

                network_data["bytes_sent"] = round(bytes_sent / (1024 * 1024), 2)
                network_data["bytes_recv"] = round(bytes_recv / (1024 * 1024), 2)

                # Phát thông tin qua WebSocket
                socketio_instance.emit('update_network', network_data)

                time.sleep(1)
            except Exception as e:
                print(f"Lỗi khi giám sát băng thông mạng: {e}")