FROM python:3.11-slim

WORKDIR /entities_extractor

RUN apt-get update && apt-get install -y curl build-essential

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir --extra-index-url=https://pypi.org/simple -r requirements.txt
RUN python -m spacy download en_core_web_md

COPY . /entities_extractor

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]