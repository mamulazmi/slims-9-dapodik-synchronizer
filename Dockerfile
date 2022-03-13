FROM python:3-slim

ENV TZ=Asia/Makassar

WORKDIR /app

COPY . .

COPY requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "/app/main.py"]
