FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
RUN python -m textblob.download_corpora

WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]