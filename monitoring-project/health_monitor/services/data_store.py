import time

network_data = {
    "bytes_sent": 0,
    "bytes_recv": 0
}

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

start_time = time.time()

api_urls = [
    {"name": "exchange_rate_api", "url": "http://exchange_rate_api:8000/exchange-rates"},
    {"name": "gold_rate_api", "url": "http://gold_rate_api:8000/gold-prices"},
]