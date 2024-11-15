from flask import Flask, Response
import requests
import os      

app = Flask(__name__)

API_KEY = os.getenv("METALS_API_KEY")  # Đặt API key cho Metals-API
BASE = "VND"
SYMBOL = "XAU"  # Ký hiệu quốc tế của vàng

@app.route('/metrics')
def metrics():
    url = f"https://metals-api.com/api/latest?access_key={API_KEY}&base={BASE}&symbols={SYMBOL}"
    response = requests.get(url)
    data = response.json()

    # Lấy giá vàng từ response JSON
    gold_price = data["rates"][SYMBOL]
    
    # Trả về định dạng metric của Prometheus
    return Response(f"gold_price_vnd {gold_price}\n", mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
