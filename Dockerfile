FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip wheel setuptools

# Try to build wheels for our requirements
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# Second stage - actual application image
FROM python:3.11-slim

WORKDIR /entities_extractor

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels
COPY --from=builder /wheels /wheels

# Install the pre-built wheels
RUN pip install --no-index --find-links=/wheels /wheels/*

# Download the spacy model
RUN python -m spacy download en_core_web_md || \
    (echo "Fallback: direct download" && \
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl)

COPY . /entities_extractor

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]