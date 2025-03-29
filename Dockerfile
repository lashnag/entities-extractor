FROM python:3.11-slim

WORKDIR /entities_extractor

RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
    --extra-index-url=https://pypi.org/simple \
    -v \  # Добавлен verbose-режим
    -r requirements.txt || \
    (echo "Повторная попытка с x86-эмуляцией..." && \
    pip install --no-cache-dir \
    --platform=linux/amd64 \
    --only-binary=:all: \
    -r requirements.txt)

RUN python -m spacy download --no-cache-dir en_core_web_md || \
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl

COPY . /entities_extractor

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]