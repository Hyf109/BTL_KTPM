from prometheus_client import start_http_server, Gauge
import requests
import time

# Tạo metrics
bitcoin_price = Gauge('bitcoin_price_usd', 'Current Bitcoin price in USD')
api_status = Gauge('coingecko_api_up', 'Status of CoinGecko API (1 = up, 0 = down)')

def fetch_bitcoin_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        if response.status_code == 200:
            data = response.json()
            price = data['bitcoin']['usd']
            bitcoin_price.set(price)  # Gán giá Bitcoin vào metrics
            api_status.set(1)  # API hoạt động bình thường
        else:
            api_status.set(0)  # API không phản hồi
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        api_status.set(0)

if __name__ == "__main__":
    # Bắt đầu server Prometheus tại cổng 5000
    start_http_server(5000)
    print("Starting API monitor service on port 5000")
    # Gọi API mỗi 30 giây
    while True:
        fetch_bitcoin_price()
        time.sleep(30)
