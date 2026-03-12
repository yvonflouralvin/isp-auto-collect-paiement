# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

# Commande par défaut (on peut override dans docker-compose)
CMD ["python", "scripts/historical_sync.py"]