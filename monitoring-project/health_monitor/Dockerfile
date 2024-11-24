FROM python:3.9-slim


# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8003
CMD ["python", "app.py"]