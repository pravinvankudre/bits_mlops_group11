import io
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

from src.model import get_model
from src.data_preprocessing import get_transforms

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('prediction_requests_total', 'Total prediction requests')
REQUEST_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
PREDICTION_COUNT = Counter('predictions_by_class', 'Predictions by class', ['class_name'])

app = FastAPI(title="Cats vs Dogs Classifier", version="1.0.0")

# Global model and classes
model = None
classes = []
device = None
transform = None

def load_model():
    """Load the trained model."""
    global model, classes, device, transform
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Load classes
    classes_path = Path("models/classes.txt")
    if classes_path.exists():
        with open(classes_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
    else:
        classes = ["cat", "dog"]
    
    # Load model
    model = get_model(num_classes=len(classes))
    model_path = Path("models/model.pth")
    
    if not model_path.exists():
        logger.warning("Model file not found, using untrained model")
    else:
        model.load_state_dict(torch.load(model_path, map_location=device))
        logger.info("Model loaded successfully")
    
    model.to(device)
    model.eval()
    
    # Load transform
    transform = get_transforms(augment=False)

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    load_model()
    logger.info("Application startup complete")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict:
    """Prediction endpoint."""
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Transform and predict
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        predicted_class = classes[predicted.item()]
        confidence_score = confidence.item()
        
        # Update metrics
        PREDICTION_COUNT.labels(class_name=predicted_class).inc()
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
        
        # Log prediction
        logger.info(f"Prediction: {predicted_class}, Confidence: {confidence_score:.4f}, "
                   f"Latency: {latency:.4f}s, File: {file.filename}")
        
        result = {
            "prediction": predicted_class,
            "confidence": float(confidence_score),
            "probabilities": {
                classes[i]: float(probabilities[0][i])
                for i in range(len(classes))
            },
            "latency_seconds": latency
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Cats vs Dogs Classifier API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "metrics": "/metrics"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
