# MLOps Assignment 2 Group 11- Cats vs Dogs Classification

End-to-end MLOps pipeline for binary image classification with CI/CD deployment.

## Project Structure
```
├── src/
│   ├── data_preprocessing.py    # Data loading and preprocessing
│   ├── model.py                 # Model architecture
│   ├── train.py                 # Training script with MLflow
│   └── inference.py             # FastAPI inference service
├── tests/
│   ├── test_preprocessing.py    # Unit tests for preprocessing
│   └── test_inference.py        # Unit tests for inference
├── k8s/
│   ├── deployment.yaml          # Kubernetes deployment
│   └── service.yaml             # Kubernetes service
├── .github/workflows/
│   └── ci-cd.yaml               # CI/CD pipeline
├── Dockerfile                   # Container image definition
├── docker-compose.yml           # Local deployment
├── requirements.txt             # Python dependencies
└── .dvc/                        # DVC configuration
```

## Quick Start - Single Command

**Option 1: Quick Demo (5-10 minutes) - Recommended for testing**

```bash
python run_quick_demo.py
```

This creates an untrained model and tests the deployment pipeline quickly.

**Option 2: Full Pipeline with Training (30-60 minutes)**

```bash
python run_all.py
```

This runs the complete pipeline including full model training.


**Full Pipeline (`run_all.py`):**
1.  Install dependencies
2.  Download dataset from Kaggle
3.  Preprocess images to 224x224
4.  Track data with DVC
5.  Create quick model + Train with MLflow (3 epochs)
6.  Run unit tests
7.  Build Docker image
8.  Deploy with Docker Compose


**Prerequisites:**
- Python 3.10+
- Docker installed
- Kaggle API credentials in `~/.kaggle/kaggle.json` ([Get it here](https://www.kaggle.com/settings))

---

## Manual Setup (Optional)

If you prefer to run steps individually:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download & Prepare Dataset
```bash
python download_dataset.py
python prepare_data.py
```

### 3. Train Model
```bash
python src/train.py
```

### 4. Run Tests
```bash
pytest tests/ -v --cov=src
```

### 5. Build & Deploy
```bash
# Build Docker image
docker build -t cats-dogs-classifier:latest .

# Deploy locally
docker-compose up -d

# OR deploy to Kubernetes
kubectl apply -f k8s/
```

### 6. Run Smoke Tests
```bash
python smoke_tests.py http://localhost:8000
```

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Prediction endpoint (accepts image file)

## Monitoring & Tracking

### MLflow Experiment Tracking
```bash
mlflow ui --port 5000
```
View at: http://localhost:5000
- Training metrics (accuracy, loss)
- Model parameters
- Confusion matrix and loss curves

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```
Metrics available:
- `prediction_requests_total` - Total requests
- `prediction_latency_seconds` - Response time
- `predictions_by_class` - Predictions per class

### Logs
```bash
# Docker Compose logs
docker-compose logs -f

# Kubernetes logs
kubectl logs -f deployment/cats-dogs-classifier
```

---

##  Testing

### Run Unit Tests
```bash
pytest tests/ -v --cov=src --cov-report=term
```

### Test API Locally
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/image.jpg"
```

---

##  CI/CD Pipeline

The project includes a complete CI/CD pipeline in `.github/workflows/ci-cd.yml`:

**On Push/PR:**
1. Run unit tests with coverage
2. Build Docker image
3. Push to Docker Hub (on main branch)
4. Deploy to Kubernetes
5. Run smoke tests

**Required GitHub Secrets:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `KUBECONFIG` - Kubernetes config (base64 encoded)

---
