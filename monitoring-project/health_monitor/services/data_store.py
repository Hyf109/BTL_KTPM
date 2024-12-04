import time

network_data = {
    "bytes_sent": 0,
    "bytes_recv": 0
}

history_data = {
    "is_healthy": [],
    "timestamps": [],
    "status": []
}

start_time = time.time()

monitored_apis = {}
