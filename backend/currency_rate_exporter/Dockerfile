FROM python:3.8-slim
WORKDIR /app

# Sao chép mã nguồn của exporter vào container
COPY currency_rate_exporter.py .

# Cài đặt các thư viện cần thiết
RUN pip install requests flask

# Khởi động exporter tỷ giá ngoại tệ
CMD ["python", "currency_rate_exporter.py"]
