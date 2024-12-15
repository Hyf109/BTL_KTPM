from flask import Blueprint, jsonify
from flask_socketio import SocketIO, emit
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.alert_service import monitor_alerts
from services.data_store import network_data, start_time
from services.network_monitor import monitor_network_bandwidth
from services.health_monitor import monitor_health_check
import time
import threading
import redis
import json

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

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

    health_data = {
        "status": "healthy" if is_healthy else "unhealthy",
        "uptime": f"{uptime:.2f} seconds",
        "gold_api": "connected" if gold_docker_status else "disconnected",
        "exchange_api": "connected" if exchange_docker_status else "disconnected",
        "gold_docker": "running" if gold_docker_status else "stopped",
        "exchange_docker": "running" if exchange_docker_status else "stopped",
        "system": {
            "cpu_usage": f"{system_health['cpu_usage']}%",
            "memory_usage": f"{system_health['memory_usage']}%"
        },
    }
    
    # Retrieve existing health data from Redis
    history_data = redis_client.get('health_check_history')
    if history_data:
        history_data = json.loads(history_data)
    else:
        history_data = []
    
    # Add timestamp to health_data before appending to history
    health_data_with_timestamp = health_data.copy()
    health_data_with_timestamp["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
     
    # Append the new health data to the history
    history_data.append(health_data_with_timestamp)
    
    # Store the updated history data in Redis
    redis_client.set('health_check_history', json.dumps(history_data))
    
    return jsonify(health_data), 200 if is_healthy else 500

# Endpoint trả về dữ liệu băng thông mạng
@routes.route('/network', methods=['GET'])
def get_network_data():
    return jsonify(network_data), 200

# Endpoint trả về lịch sử kiểm tra sức khỏe hệ thống
@routes.route('/history', methods=['GET'])
def get_health_history():
    # Retrieve existing health data from Redis
    history_data = redis_client.get('health_check_history')
    if history_data:
        history_data = json.loads(history_data)
    else:
        history_data = []

    return jsonify(history_data), 200