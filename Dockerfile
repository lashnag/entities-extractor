FROM python:3.11-slim

WORKDIR /entities_extractor

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_md

COPY . /entities_extractor

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4319 --workers 4"]