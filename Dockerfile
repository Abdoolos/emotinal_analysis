FROM python:3.8.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python build tools
RUN pip install --no-cache-dir \
    setuptools==57.5.0 \
    wheel==0.37.1 \
    pip==23.3.1

# Install dependencies in layers for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ backend/
COPY runtime.txt .

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Start the application
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "80"]
