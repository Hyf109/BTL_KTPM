FROM python:3.8-slim
WORKDIR /app

# Sao chép mã nguồn của exporter vào container
COPY gold_price_exporter.py .

# Cài đặt các thư viện cần thiết
RUN pip install requests flask

# Khởi động exporter giá vàng
CMD ["python", "gold_price_exporter.py"]
