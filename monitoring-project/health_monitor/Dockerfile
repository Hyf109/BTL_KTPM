FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8003
CMD ["python", "app.py"]