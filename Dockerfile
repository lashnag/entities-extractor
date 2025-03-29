FROM python:3.11-slim

WORKDIR /entities_extractor

# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y curl

# 2. Установка Python-пакетов с явным указанием ARM-совместимых версий
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --extra-index-url=https://pypi.org/simple \
    -r requirements.txt

# 3. Установка модели Spacy с проверкой архитектуры
RUN python -c "import platform; print('Architecture:', platform.machine())" && \
    python -m spacy download --no-cache-dir en_core_web_md || \
    (echo "Fallback: установка x86-версии" && \
     pip install --no-cache-dir \
     --platform=linux/amd64 \
     --only-binary=:all: \
     https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl)

COPY . .

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]