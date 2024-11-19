import requests

# URL của fake API
BASE_URL = "http://127.0.0.1:8000"

def get_all_exchange_rates():
    """
    Lấy danh sách tỷ giá ngoại tệ so với VND.
    """
    try:
        response = requests.get(f"{BASE_URL}/exchange-rates")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        exchange_rates = response.json()
        print("Danh sách tỷ giá ngoại tệ so với VND:")
        for rate in exchange_rates:
            print(f"- {rate['currency']}: {rate['rate_to_vnd']} VND ({rate['symbol']})")
    except Exception as e:
        print(f"Không thể lấy danh sách tỷ giá: {e}")

def get_exchange_rate_by_currency(currency):
    """
    Lấy tỷ giá của một loại ngoại tệ cụ thể.
    """
    try:
        response = requests.get(f"{BASE_URL}/exchange-rates/{currency}")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        rate = response.json()
        if "error" in rate:
            print(f"Lỗi: {rate['error']}")
        else:
            print(f"Tỷ giá của {rate['currency']}: {rate['rate_to_vnd']} VND ({rate['symbol']})")
    except Exception as e:
        print(f"Không thể lấy tỷ giá của {currency}: {e}")

def get_random_exchange_rate():
    """
    Lấy một tỷ giá ngẫu nhiên từ danh sách.
    """
    try:
        response = requests.get(f"{BASE_URL}/random-exchange-rate")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        rate = response.json()
        print(f"Tỷ giá ngẫu nhiên:")
        print(f"- {rate['currency']}: {rate['rate_to_vnd']} VND ({rate['symbol']})")
    except Exception as e:
        print(f"Không thể lấy tỷ giá ngẫu nhiên: {e}")

if __name__ == "__main__":
    # Lấy danh sách tỷ giá
    get_all_exchange_rates()
    
    # Lấy tỷ giá của một loại ngoại tệ cụ thể
    currency_code = "USD"  # Thay bằng mã tiền tệ bạn muốn
    get_exchange_rate_by_currency(currency_code)
    
    # Lấy một tỷ giá ngẫu nhiên
    get_random_exchange_rate()
