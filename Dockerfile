FROM python:3.8.10-slim

WORKDIR /app

# Install system dependencies for librosa, pydub, and speech recognition
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libportaudio2 \
    build-essential \
    python3-dev \
    pkg-config \
    libasound2-dev \
    portaudio19-dev \
    flac \
    libflac-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/src backend/src

# Set Python path for module imports
ENV PYTHONPATH=/app

# Start the application
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "80"]
