from flask import Blueprint, jsonify
from flask_socketio import SocketIO, emit
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.alert_service import monitor_alerts
from services.data_store import network_data
from services.network_monitor import monitor_network_bandwidth
import time
import threading

# Khởi tạo Blueprint và SocketIO
routes = Blueprint('routes', __name__)
socketio = SocketIO()
start_time = time.time()  # Lưu thời gian bắt đầu chạy ứng dụng

# Biến lưu trữ lịch sử dữ liệu
history_data = {
    "is_healthy": [],
    "timestamps": [],
    "cpu_usage": [],
    "memory_usage": [],
    "gold_api": [],
    "exchange_api": [],
    "gold_docker": [],
    "exchange_docker": []
}



# Giám sát health check
def monitor_health_check(app, socketio_instance):
    global history_data
    with app.app_context():
        while True:
            try:
                # Kiểm tra sức khỏe hệ thống
                uptime = time.time() - start_time
                exchange_api_status = ExternalAPI.check_external_api("http://exchange_rate_api:8000/exchange-rates")
                gold_api_status = ExternalAPI.check_external_api("http://gold_rate_api:8000/gold-prices")

                exchange_docker_status = ContainerAPI.check_docker_status("exchange_rate_api")
                gold_docker_status = ContainerAPI.check_docker_status("gold_rate_api")

                system_health = SystemAPI.check_system_health()
                is_healthy = gold_api_status and exchange_api_status and system_health["status"] == "healthy"

                # Cập nhật lịch sử dữ liệu
                history_data["is_healthy"].append(system_health["status"])
                history_data["timestamps"].append(time.time())
                history_data["cpu_usage"].append(system_health["cpu_usage"])
                history_data["memory_usage"].append(system_health["memory_usage"])
                history_data["gold_api"].append(int(gold_api_status))
                history_data["exchange_api"].append(int(exchange_api_status))
                history_data["gold_docker"].append(int(gold_docker_status))
                history_data["exchange_docker"].append(int(exchange_docker_status))

                # Đảm bảo không lưu quá nhiều dữ liệu
                if len(history_data["timestamps"]) > 100:
                    for key in history_data.keys():
                        history_data[key].pop(0)

                # Phát thông tin qua WebSocket
                socketio_instance.emit('update_health', {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "uptime": f"{uptime:.2f} seconds",
                    "gold_api": "connected" if gold_api_status else "disconnected",
                    "exchange_api": "connected" if exchange_api_status else "disconnected",
                    "gold_docker": "running" if gold_docker_status else "stopped",
                    "exchange_docker": "running" if exchange_docker_status else "stopped",
                    "system": {
                        "cpu_usage": f"{system_health['cpu_usage']}%",
                        "memory_usage": f"{system_health['memory_usage']}%"
                    }
                })

                # Chờ 10 giây trước khi thực hiện lại
                time.sleep(10)
            except Exception as e:
                print(f"Lỗi khi giám sát health check: {e}")

# Khởi chạy các luồng giám sát
def start_monitor_thread(app, socketio_instance):
    threading.Thread(
        target=monitor_network_bandwidth,
        args=(app, socketio_instance),
        daemon=True
    ).start()
    threading.Thread(
        target=monitor_health_check,
        args=(app, socketio_instance),
        daemon=True
    ).start()
    threading.Thread(
        target=monitor_alerts,
        args=(app, socketio_instance, network_data),
        daemon=True
    ).start()

# Endpoint kiểm tra sức khỏe hệ thống
@routes.route('/health', methods=['GET'])
def health_check():
    uptime = time.time() - start_time
    exchange_api_status = ExternalAPI.check_external_api("http://exchange_rate_api:8000/exchange-rates")
    gold_api_status = ExternalAPI.check_external_api("http://gold_rate_api:8000/gold-prices")

    exchange_docker_status = ContainerAPI.check_docker_status("exchange_rate_api")
    gold_docker_status = ContainerAPI.check_docker_status("gold_rate_api")

    system_health = SystemAPI.check_system_health()
    is_healthy = gold_api_status and exchange_api_status and system_health["status"] == "healthy"

    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "uptime": f"{uptime:.2f} seconds",
        "gold_api": "connected" if gold_api_status else "disconnected",
        "exchange_api": "connected" if exchange_api_status else "disconnected",
        "gold_docker": "running" if gold_docker_status else "stopped",
        "exchange_docker": "running" if exchange_docker_status else "stopped",
        "system": {
            "cpu_usage": f"{system_health['cpu_usage']}%",
            "memory_usage": f"{system_health['memory_usage']}%"
        },
        # "history data": history_data
    }), 200 if is_healthy else 500

# Endpoint trả về dữ liệu băng thông mạng
@routes.route('/network', methods=['GET'])
def get_network_data():
    return jsonify(network_data), 200
