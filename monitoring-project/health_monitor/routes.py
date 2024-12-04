from flask import Blueprint, jsonify, request
from flask_socketio import SocketIO, emit
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.alert_service import monitor_alerts
from services.data_store import network_data, start_time, monitored_apis
from services.network_monitor import monitor_network_bandwidth
from services.health_monitor import monitor_health_check
import time
import threading


# Khởi tạo Blueprint và SocketIO
routes = Blueprint('routes', __name__)
socketio = SocketIO()



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

@routes.route('/add_monitor', methods=['POST'])
def add_monitor():
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of APIs with 'name' and 'url'"}), 400

    for api in data:
        name = api.get('name')
        url = api.get('url')

        if not name or not url:
            return jsonify({"error": f"Missing 'name' or 'url' for API: {api}"}), 400

        if name in monitored_apis:
            return jsonify({"error": f"API '{name}' is already being monitored"}), 400

        # Thêm API vào danh sách theo dõi
        monitored_apis[name] = {
            "url": url,
            "history_data": {
                "is_healthy": [],
                "timestamps": [],
                "status": []
            }
        }

    return jsonify({"message": f"APIs added successfully!", "monitored_apis": list(monitored_apis.keys())}), 201

# Endpoint trả về dữ liệu băng thông mạng
@routes.route('/network', methods=['GET'])
def get_network_data():
    return jsonify(network_data), 200

@routes.route('/get_monitored_apis', methods=['GET'])
def get_monitored_apis():
    
    #Trả về danh sách các API đang được theo dõi.
    
    return jsonify({"monitored_apis": list(monitored_apis.keys())}), 200


@routes.route('/history/<api_name>', methods=['GET'])
def get_api_history(api_name):
    
    #Trả về lịch sử dữ liệu của một API cụ thể.
    
    api = monitored_apis.get(api_name)
    if not api:
        return jsonify({"error": f"API '{api_name}' not found"}), 404

    return jsonify(api["history_data"]), 200