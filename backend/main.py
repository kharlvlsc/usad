from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import json
from .review_prediction import predict_review

app = FastAPI()

# Enable CORS
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://your-app-name.koyeb.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

class ReviewRequest(BaseModel):
    review: str

class ReviewResponse(BaseModel):
    prediction: str
    cluster: int
    distance: float
    threshold: float
    features: dict
    processed_text: str

@app.post("/api/predict", response_model=ReviewResponse)
def predict(review_request: ReviewRequest):
    review_text = review_request.review
    result = predict_review(review_text)
    return result

@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")

@app.get("/api/feature-basis")
def get_feature_basis():
    try:
        with open("feature_basis.json") as f:
            return json.load(f)
    except:
        return {"normal": {}}

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