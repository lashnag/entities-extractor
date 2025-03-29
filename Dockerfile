FROM python:3.11-slim

WORKDIR /entities_extractor

# Установка необходимых системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Обновление pip
RUN pip install --upgrade pip setuptools wheel

# Сначала устанавливаем numpy и другие базовые зависимости
RUN pip install --no-cache-dir numpy==1.26.4 cython

# Установка не-spaCy зависимостей
RUN pip install --no-cache-dir fastapi==0.89.1 pydantic==1.10.21 dateparser==1.2.1
RUN pip install --no-cache-dir python-logstash-async==4.0.1 uvicorn==0.32.1 gunicorn==23.0.0
RUN pip install --no-cache-dir pullenti-wrapper==0.9.0 python-dateutil==2.9.0.post0

# Ключевой момент: установка спецификации для пропуска компиляции blis
ENV BLIS_ARCH="generic"

# Установка spaCy с явным указанием использовать вариант для arm64
RUN python -m pip install --no-cache-dir spacy==3.8.2 --config-settings="--build-option=--cpu=generic"

# Скачивание модели spacy
RUN python -m spacy download en_core_web_md || \
    (echo "Fallback: direct download" && \
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl)

COPY . /entities_extractor

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]