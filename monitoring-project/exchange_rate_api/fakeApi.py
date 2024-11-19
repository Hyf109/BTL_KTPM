from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Dữ liệu giả lập: tỷ giá các loại tiền tệ so với VND
fake_exchange_rates = [
    {"currency": "USD", "rate_to_vnd": 24000.0, "symbol": "$"},
    {"currency": "EUR", "rate_to_vnd": 28000.0, "symbol": "€"},
    {"currency": "JPY", "rate_to_vnd": 180.0, "symbol": "¥"},
    {"currency": "GBP", "rate_to_vnd": 31000.0, "symbol": "£"},
    {"currency": "AUD", "rate_to_vnd": 16000.0, "symbol": "A$"},
    {"currency": "CNY", "rate_to_vnd": 3400.0, "symbol": "¥"},
    {"currency": "KRW", "rate_to_vnd": 18.0, "symbol": "₩"},
]

# Model dữ liệu tỷ giá
class ExchangeRate(BaseModel):
    currency: str
    rate_to_vnd: float
    symbol: str

# Endpoint lấy danh sách tỷ giá
@app.get("/exchange-rates", response_model=List[ExchangeRate])
async def get_exchange_rates():
    """
    Trả về danh sách tỷ giá các loại ngoại tệ so với VND.
    """
    return fake_exchange_rates

# Endpoint lấy tỷ giá của một loại tiền cụ thể
@app.get("/exchange-rates/{currency}", response_model=ExchangeRate)
async def get_exchange_rate_by_currency(currency: str):
    """
    Trả về tỷ giá của một loại ngoại tệ cụ thể so với VND.
    """
    rate = next((item for item in fake_exchange_rates if item["currency"].upper() == currency.upper()), None)
    if rate:
        return rate
    return {"error": "Currency not found"}

# Endpoint trả về tỷ giá ngẫu nhiên
@app.get("/random-exchange-rate", response_model=ExchangeRate)
async def get_random_exchange_rate():
    """
    Trả về một tỷ giá ngẫu nhiên từ danh sách.
    """
    return random.choice(fake_exchange_rates)