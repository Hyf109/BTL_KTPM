import time
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.external_api import ExternalAPI

# Ngưỡng cảnh báo
ALERT_THRESHOLDS = {
    "cpu_usage": 80,         # Ngưỡng CPU tối đa (%)
    "memory_usage": 80,      # Ngưỡng bộ nhớ tối đa (%)
    "bandwidth_usage": 100,  # Ngưỡng băng thông tối đa (MB/s)
}


def monitor_alerts(app, socketio_instance, network_data):

    #Giám sát các chỉ số hệ thống và gửi cảnh báo nếu vượt ngưỡng.

    with app.app_context():
        while True:
            try:
                # Kiểm tra tình trạng hệ thống
                system_health = SystemAPI.check_system_health()
                cpu_usage = system_health.get("cpu_usage", 0)
                memory_usage = system_health.get("memory_usage", 0)

                # Kiểm tra băng thông mạng
                bandwidth_sent = network_data.get("bytes_sent", 0)
                bandwidth_recv = network_data.get("bytes_recv", 0)
                total_bandwidth = bandwidth_sent + bandwidth_recv

                alerts = []

                # Kiểm tra ngưỡng CPU
                if cpu_usage > ALERT_THRESHOLDS["cpu_usage"]:
                    alerts.append(f"High CPU usage: {cpu_usage}%")

                # Kiểm tra ngưỡng bộ nhớ
                if memory_usage > ALERT_THRESHOLDS["memory_usage"]:
                    alerts.append(f"High memory usage: {memory_usage}%")

                # Kiểm tra ngưỡng băng thông
                if total_bandwidth > ALERT_THRESHOLDS["bandwidth_usage"]:
                    alerts.append(
                        f"High network bandwidth usage: {total_bandwidth} MB"
                    )

                # Kiểm tra trạng thái các container và API
                if not ExternalAPI.check_external_api("http://gold_rate_api:8000/gold-prices"):
                    alerts.append("Gold Price API is not responding!")

                if not ExternalAPI.check_external_api("http://exchange_rate_api:8000/exchange-rates"):
                    alerts.append("Exchange Rate API is not responding!")

                if not ContainerAPI.check_docker_status("gold_rate_api"):
                    alerts.append("Gold Price API container is down!")

                if not ContainerAPI.check_docker_status("exchange_rate_api"):
                    alerts.append("Exchange Rate API container is down!")

                # Gửi cảnh báo qua WebSocket nếu có
                if alerts:
                    socketio_instance.emit("alerts", {"alerts": alerts})

                time.sleep(5)  # Chờ 5 giây trước khi kiểm tra lại
            except Exception as e:
                print(f"Lỗi khi giám sát cảnh báo: {e}")
