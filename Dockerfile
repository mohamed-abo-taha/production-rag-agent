FROM python:3.11-slim

WORKDIR /app

# System deps kept minimal; sentence-transformers pulls torch wheels.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-build the index at image build time so the container is ready to serve on start.
RUN python -m scripts.run_ingest

EXPOSE 8000
CMD ["python", "-m", "scripts.run_api"]
