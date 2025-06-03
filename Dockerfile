FROM python:3.8.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files first for better caching
COPY requirements.txt .
COPY backend/requirements.txt backend/

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Start the application
CMD uvicorn backend.src.main:app --host 0.0.0.0 --port ${PORT:-80}
