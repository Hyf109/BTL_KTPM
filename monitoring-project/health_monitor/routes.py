from flask import Blueprint, jsonify
from flask_socketio import SocketIO, emit
from services.external_api import ExternalAPI
from services.system_api import SystemAPI
from services.container_status import ContainerAPI
from services.alert_service import monitor_alerts
from services.data_store import network_data, start_time, api_urls
from services.network_monitor import monitor_network_bandwidth
from services.health_monitor import monitor_health_check
import time
import threading
import redis
import json

redis_client = redis.StrictRedis(host="redis", port=6379, db=0)

# Initialize Blueprint and SocketIO
routes = Blueprint("routes", __name__)
socketio = SocketIO()


# Start monitoring threads
def start_monitor_thread(app, socketio_instance):
    threading.Thread(
        target=monitor_network_bandwidth, args=(app, socketio_instance), daemon=True
    ).start()
    threading.Thread(
        target=monitor_health_check, args=(app, socketio_instance), daemon=True
    ).start()
    threading.Thread(
        target=monitor_alerts, args=(app, socketio_instance, network_data), daemon=True
    ).start()


# Health check endpoint
@routes.route("/health", methods=["GET"])
def health_check():
    uptime = time.time() - start_time

    # Use api_urls for external API checks
    health_statuses = []
    for api in api_urls:
        name = api["name"]
        url = api["url"]

        api_status = ExternalAPI.check_external_api(url)
        docker_status = ContainerAPI.check_docker_status(name)

        health_statuses.append(
            {
                "api_name": name,
                "api_status": "connected" if api_status else "disconnected",
                "docker_status": "running" if docker_status else "stopped",
            }
        )

    system_health = SystemAPI.check_system_health()
    is_healthy = all(
        api["api_status"] == "connected" for api in health_statuses
    ) and system_health["status"] == "healthy"

    health_data = {
        "status": "healthy" if is_healthy else "unhealthy",
        "uptime": f"{uptime:.2f} seconds",
        "system": {
            "cpu_usage": f"{system_health['cpu_usage']}%",
            "memory_usage": f"{system_health['memory_usage']}%",
        },
        "apis": health_statuses,
    }

    # Retrieve and update history data from Redis
    history_data = redis_client.get("health_check_history")
    if history_data:
        history_data = json.loads(history_data)
    else:
        history_data = []

    health_data_with_timestamp = health_data.copy()
    health_data_with_timestamp["timestamp"] = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime()
    )
    history_data.append(health_data_with_timestamp)

    redis_client.set("health_check_history", json.dumps(history_data))

    return jsonify(health_data), 200 if is_healthy else 500


# Network bandwidth endpoint
@routes.route("/network", methods=["GET"])
def get_network_data():
    return jsonify(network_data), 200


# Health check history endpoint
@routes.route("/history", methods=["GET"])
def get_health_history():
    history_data = redis_client.get("health_check_history")
    if history_data:
        history_data = json.loads(history_data)
    else:
        history_data = []

    return jsonify(history_data), 200
