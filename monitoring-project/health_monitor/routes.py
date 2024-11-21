from flask import Blueprint, jsonify
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
import time

routes = Blueprint('routes', __name__)
start_time = time.time()  # Lưu thời gian bắt đầu chạy ứng dụng

@routes.route('/health', methods=['GET'])
def health_check():
    uptime = time.time() - start_time
    exchange_api_status = ExternalAPI.check_external_api("http://localhost:8001/exchange-rates")
    gold_api_status = ExternalAPI.check_external_api("http://localhost:8002/gold-prices")
    
    system_health = SystemAPI.check_system_health()

    is_healthy = gold_api_status and exchange_api_status and system_health["status"] == "healthy"
    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "uptime": f"{uptime:.2f} seconds",
        "gold_api": "connected" if gold_api_status else "disconnected",
        "exchange_api": "connected" if exchange_api_status else "disconnected",
        "system": {
            "cpu_usage": f"{system_health['cpu_usage']}%",
            "memory_usage": f"{system_health['memory_usage']}%"
        }
    }), 200 if is_healthy else 500
