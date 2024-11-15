from flask import Flask, Response
import requests
import os

app = Flask(__name__)

CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/VND"

@app.route('/metrics')
def metric():
    response = requests.get(CURRENCY_API_URL)
    data = response.json()
    
    # Ví dụ lấy tỷ giá USD/VND
    usd_to_vnd = data["rates"]["USD"]
    
    # Trả về định dạng metric cho Prometheus
    return Response(f"usd_to_vnd_exchange_rate {usd_to_vnd}\n", mimetype="text/plain")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)