FROM python:3.12-slim-bookworm
WORKDIR /app
COPY . .
EXPOSE 8000
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "fakeApi:app", "--host", "0.0.0.0", "--port", "8000"]