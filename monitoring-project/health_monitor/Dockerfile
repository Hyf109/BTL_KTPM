FROM python:3.14.0a2-bookworm

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8003
CMD ["python", "app.py"]
