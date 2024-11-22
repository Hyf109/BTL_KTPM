from flask import Blueprint, jsonify
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
import time

routes = Blueprint('routes', __name__)
start_time = time.time()  # Lưu thời gian bắt đầu chạy ứng dụng

# Biến lưu trữ lịch sử dữ liệu
history_data = {
    "timestamps": [],
    "cpu_usage": [],
    "memory_usage": [],
    "gold_api": [],
    "exchange_api": []
}

@routes.route('/health', methods=['GET'])
def health_check():
    uptime = time.time() - start_time
    exchange_api_status = ExternalAPI.check_external_api("http://localhost:8001/exchange-rates")
    gold_api_status = ExternalAPI.check_external_api("http://localhost:8002/gold-prices")
    
    exchange_docker_status = ContainerAPI.check_docker_status("exchange_rate_api")
    gold_docker_status = ContainerAPI.check_docker_status("gold_rate_api")
    
    system_health = SystemAPI.check_system_health()

    # Cập nhật lịch sử dữ liệu
    history_data["timestamps"].append(time.time())
    history_data["cpu_usage"].append(system_health["cpu_usage"])
    history_data["memory_usage"].append(system_health["memory_usage"])
    history_data["gold_api"].append(int(gold_api_status))
    history_data["exchange_api"].append(int(exchange_api_status))

    # Đảm bảo không lưu quá nhiều dữ liệu
    if len(history_data["timestamps"]) > 100:
        for key in history_data.keys():
            history_data[key].pop(0)

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
        }
    }), 200 if is_healthy else 500

# @routes.route('/dashboard', methods=['GET'])
# def dashboard():
#     """Trang giao diện hiển thị biểu đồ."""
#     return render_template('dashboard.html', data=history_data)