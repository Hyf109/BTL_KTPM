from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

# Dữ liệu giả lập
fake_gold_prices = [
    {"country": "USA", "price_usd_per_gram": 60.5, "currency": "USD"},
    {"country": "India", "price_usd_per_gram": 58.3, "currency": "INR"},
    {"country": "China", "price_usd_per_gram": 61.2, "currency": "CNY"},
    {"country": "Vietnam", "price_usd_per_gram": 59.8, "currency": "VND"},
    {"country": "UK", "price_usd_per_gram": 62.1, "currency": "GBP"},
    {"country": "Canada", "price_usd_per_gram": 60.0, "currency": "CAD"},
]

# Model dữ liệu giá vàng
class GoldPrice(BaseModel):
    country: str
    price_usd_per_gram: float
    currency: str

# Endpoint lấy danh sách giá vàng tại tất cả các quốc gia
@app.get("/gold-prices", response_model=List[GoldPrice])
async def get_gold_prices():
    """
    Trả về danh sách giá vàng tại các quốc gia.
    """
    return fake_gold_prices

# Endpoint lấy giá vàng tại một quốc gia cụ thể
@app.get("/gold-prices/{country}", response_model=GoldPrice)
async def get_gold_price_by_country(country: str):
    """
    Trả về giá vàng tại một quốc gia cụ thể.
    """
    country_price = next((item for item in fake_gold_prices if item["country"].lower() == country.lower()), None)
    if country_price:
        return country_price
    return {"error": "Country not found"}

# Endpoint tạo giá vàng ngẫu nhiên cho một quốc gia
@app.get("/random-gold-price", response_model=GoldPrice)
async def random_gold_price():
    """
    Trả về giá vàng ngẫu nhiên từ danh sách.
    """
    return random.choice(fake_gold_prices)

