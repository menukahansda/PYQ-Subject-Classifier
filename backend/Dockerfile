FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 && \
    rm -rf /var/lib/apt/lists/*

ENV POPPLER_PATH=/usr/bin

COPY requirements.prod.txt .

RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]