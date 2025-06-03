FROM python:3.8-slim

WORKDIR /app

# Copy requirements files first for better caching
COPY requirements.txt .
COPY backend/requirements.txt backend/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Start the application
CMD uvicorn backend.src.main:app --host 0.0.0.0 --port ${PORT:-80}
