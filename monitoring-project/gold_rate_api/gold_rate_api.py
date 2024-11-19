import requests

# URL của fake API
BASE_URL = "http://127.0.0.1:8000"

def get_all_gold_prices():
    """
    Lấy danh sách giá vàng tại tất cả các quốc gia.
    """
    try:
        response = requests.get(f"{BASE_URL}/gold-prices")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        gold_prices = response.json()
        print("Danh sách giá vàng tại các quốc gia:")
        for price in gold_prices:
            print(f"- {price['country']}: {price['price_usd_per_gram']} USD/gram ({price['currency']})")
    except Exception as e:
        print(f"Không thể lấy danh sách giá vàng: {e}")

def get_gold_price_by_country(country):
    """
    Lấy giá vàng tại một quốc gia cụ thể.
    """
    try:
        response = requests.get(f"{BASE_URL}/gold-prices/{country}")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        gold_price = response.json()
        if "error" in gold_price:
            print(f"Lỗi: {gold_price['error']}")
        else:
            print(f"Giá vàng tại {gold_price['country']}: {gold_price['price_usd_per_gram']} USD/gram ({gold_price['currency']})")
    except Exception as e:
        print(f"Không thể lấy giá vàng của quốc gia {country}: {e}")

def get_random_gold_price():
    """
    Lấy giá vàng ngẫu nhiên từ danh sách.
    """
    try:
        response = requests.get(f"{BASE_URL}/random-gold-price")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        gold_price = response.json()
        print(f"Giá vàng ngẫu nhiên:")
        print(f"- {gold_price['country']}: {gold_price['price_usd_per_gram']} USD/gram ({gold_price['currency']})")
    except Exception as e:
        print(f"Không thể lấy giá vàng ngẫu nhiên: {e}")

if __name__ == "__main__":
    # Lấy danh sách giá vàng
    get_all_gold_prices()
    
    # Lấy giá vàng của một quốc gia cụ thể
    country_name = "Vietnam"  # Đổi thành tên quốc gia bạn muốn
    get_gold_price_by_country(country_name)
    
    # Lấy giá vàng ngẫu nhiên
    get_random_gold_price()
