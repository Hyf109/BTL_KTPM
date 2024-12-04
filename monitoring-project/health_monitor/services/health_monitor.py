import time
from flask_socketio import SocketIO
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.data_store import history_data, start_time, monitored_apis

def monitor_health_check(app, socketio_instance):
    with app.app_context():
        while True:
            try:
                for name, api in monitored_apis.items():
                    url = api["url"]
                    api_status = ExternalAPI.check_external_api(url)
                    
                    history = api["history_data"]
                    history["timestamps"].append(time.time())
                    history["status"].append("connected" if api_status else "disconnected")
                    
                    if len(history["timestamps"]) > 100:
                        for key in history.keys():
                            history[key].pop(0)
                    
                    socketio_instance.emit(f'update_health_{name}', {
                        "name": name,
                        "status": "connected" if api_status else "disconnected"
                    })
            
                time.sleep(10)
            
            except Exception as e:
                print(f"Lỗi khi giám sát API: {e}")
                
                # # Kiểm tra sức khỏe hệ thống
                # uptime = time.time() - start_time
                # exchange_api_status = ExternalAPI.check_external_api("http://exchange_rate_api:8000/exchange-rates")
                # gold_api_status = ExternalAPI.check_external_api("http://gold_rate_api:8000/gold-prices")

                # exchange_docker_status = ContainerAPI.check_docker_status("exchange_rate_api")
                # gold_docker_status = ContainerAPI.check_docker_status("gold_rate_api")

                # system_health = SystemAPI.check_system_health()
                # is_healthy = gold_api_status and exchange_api_status and system_health["status"] == "healthy"

                # # Cập nhật lịch sử dữ liệu
                # history_data["is_healthy"].append(system_health["status"])
                # history_data["timestamps"].append(time.time())
                # history_data["cpu_usage"].append(system_health["cpu_usage"])
                # history_data["memory_usage"].append(system_health["memory_usage"])
                # history_data["gold_api"].append(int(gold_api_status))
                # history_data["exchange_api"].append(int(exchange_api_status))
                # history_data["gold_docker"].append(int(gold_docker_status))
                # history_data["exchange_docker"].append(int(exchange_docker_status))

                # # Đảm bảo không lưu quá nhiều dữ liệu
                # if len(history_data["timestamps"]) > 100:
                #     for key in history_data.keys():
                #         history_data[key].pop(0)

                # # Phát thông tin qua WebSocket
                # socketio_instance.emit('update_health', {
                #     "status": "healthy" if is_healthy else "unhealthy",
                #     "uptime": f"{uptime:.2f} seconds",
                #     "gold_api": "connected" if gold_api_status else "disconnected",
                #     "exchange_api": "connected" if exchange_api_status else "disconnected",
                #     "gold_docker": "running" if gold_docker_status else "stopped",
                #     "exchange_docker": "running" if exchange_docker_status else "stopped",
                #     "system": {
                #         "cpu_usage": f"{system_health['cpu_usage']}%",
                #         "memory_usage": f"{system_health['memory_usage']}%"
                #     }
                # })

                # Chờ 10 giây trước khi thực hiện lại
