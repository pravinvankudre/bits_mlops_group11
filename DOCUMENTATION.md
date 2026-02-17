# MLOps Assignment 2 - Complete Documentation

## Project Overview

This project implements an end-to-end MLOps pipeline for binary image classification (Cats vs Dogs) covering all aspects from model development to production deployment.

## Architecture

```
┌─────────────────┐
│  Data Versioning│
│      (DVC)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Model Training  │─────▶│ Experiment Track │
│   (PyTorch)     │      │    (MLflow)      │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Model Package  │
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Containerization│
│    (Docker)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   CI Pipeline   │─────▶│  Docker Registry │
│ (GitHub Actions)│      │   (Docker Hub)   │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│   CD Pipeline   │
│  (GitOps/K8s)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   Deployment    │◀─────│   Monitoring     │
│  (Kubernetes)   │      │ (Prometheus/Logs)│
└─────────────────┘      └──────────────────┘
```

## Module Breakdown

### M1: Model Development & Experiment Tracking (10M)

**Components:**
- Git for source code versioning
- DVC for dataset versioning
- PyTorch CNN model
- MLflow for experiment tracking

**Key Files:**
- `src/model.py` - CNN architecture
- `src/train.py` - Training script with MLflow
- `src/data_preprocessing.py` - Data pipeline
- `.dvc/config` - DVC configuration

**Deliverables:**
✓ Git repository with version control
✓ DVC tracking for data
✓ Trained model (model.pth)
✓ MLflow experiment logs
✓ Confusion matrix and loss curves

---

### M2: Model Packaging & Containerization (10M)

**Components:**
- FastAPI REST API
- Docker containerization
- Health check and prediction endpoints

**Key Files:**
- `src/inference.py` - FastAPI service
- `Dockerfile` - Container definition
- `docker-compose.yml` - Local deployment
- `requirements.txt` - Dependencies

**API Endpoints:**
- `GET /health` - Service health status
- `POST /predict` - Image classification
- `GET /metrics` - Prometheus metrics

**Deliverables:**
✓ REST API with FastAPI
✓ Dockerfile with health checks
✓ Docker image builds successfully
✓ Local testing verified

---

### M3: CI Pipeline for Build, Test & Image Creation (10M)

**Components:**
- GitHub Actions workflow
- Automated testing with pytest
- Docker image build and push

**Key Files:**
- `.github/workflows/ci-cd.yml` - CI/CD pipeline
- `tests/test_preprocessing.py` - Data tests
- `tests/test_inference.py` - API tests
- `pytest.ini` - Test configuration

**Pipeline Steps:**
1. Checkout code
2. Install dependencies
3. Run unit tests
4. Build Docker image
5. Push to registry

**Deliverables:**
✓ Unit tests for preprocessing
✓ Unit tests for inference
✓ Automated CI pipeline
✓ Docker image published to registry

---

### M4: CD Pipeline & Deployment (10M)

**Components:**
- Kubernetes deployment
- Automated CD workflow
- Smoke tests

**Key Files:**
- `k8s/deployment.yaml` - K8s deployment
- `k8s/service.yaml` - K8s service
- `smoke_tests.py` - Post-deploy validation

**Deployment Features:**
- 2 replicas for high availability
- Resource limits (CPU/Memory)
- Liveness and readiness probes
- LoadBalancer service

**CD Flow:**
1. Trigger on main branch push
2. Pull new image from registry
3. Update K8s deployment
4. Wait for rollout
5. Run smoke tests

**Deliverables:**
✓ Kubernetes manifests
✓ Automated CD pipeline
✓ Smoke tests implementation
✓ Health checks configured

---

### M5: Monitoring, Logs & Final Submission (10M)

**Components:**
- Request/response logging
- Prometheus metrics
- Performance tracking

**Monitoring Features:**
- Request count by endpoint
- Prediction latency histogram
- Predictions by class counter
- Structured logging

**Metrics Exposed:**
- `prediction_requests_total` - Total requests
- `prediction_latency_seconds` - Latency distribution
- `predictions_by_class` - Predictions per class

**Deliverables:**
✓ Application logging enabled
✓ Prometheus metrics endpoint
✓ Performance tracking
✓ Complete documentation

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.10 |
| ML Framework | PyTorch | 2.0.1 |
| API Framework | FastAPI | 0.104.1 |
| Experiment Tracking | MLflow | 2.8.1 |
| Data Versioning | DVC | 3.30.1 |
| Testing | Pytest | 7.4.3 |
| Containerization | Docker | Latest |
| Orchestration | Kubernetes | 1.28+ |
| CI/CD | GitHub Actions | - |
| Monitoring | Prometheus | - |

---

## Quick Start

### 1. Setup Environment
```bash
# Clone repository
git clone <repo-url>
cd Assignment_2

# Install dependencies
pip install -r requirements.txt

# Initialize DVC
dvc init
```

### 2. Prepare Data
```bash
# Download dataset from Kaggle
# Extract to data/raw/

# Process data
python prepare_data.py

# Track with DVC
dvc add data/processed
git add data/processed.dvc
git commit -m "Add processed data"
```

### 3. Train Model
```bash
# Train with MLflow tracking
python src/train.py

# View experiments
mlflow ui --port 5000
```

### 4. Test Locally
```bash
# Run tests
pytest tests/ -v

# Start API
uvicorn src.inference:app --reload

# Test prediction
curl -X POST -F "file=@test.jpg" http://localhost:8000/predict
```

### 5. Build and Deploy
```bash
# Build Docker image
docker build -t cats-dogs-classifier:latest .

# Run with docker-compose
docker-compose up -d

# Deploy to Kubernetes
kubectl apply -f k8s/

# Run smoke tests
python smoke_tests.py
```

---

## CI/CD Workflow

### Continuous Integration
**Trigger:** Push to any branch
**Steps:**
1. Run unit tests
2. Generate coverage report
3. Build Docker image (main branch only)
4. Push to Docker Hub (main branch only)

### Continuous Deployment
**Trigger:** Push to main branch (after CI passes)
**Steps:**
1. Update K8s deployment with new image
2. Wait for rollout completion
3. Run smoke tests
4. Fail pipeline if tests fail

---

## Monitoring & Observability

### Application Logs
```bash
# Docker
docker logs -f cats-dogs-classifier

# Kubernetes
kubectl logs -f deployment/cats-dogs-classifier
```

### Metrics
```bash
# Access metrics endpoint
curl http://localhost:8000/metrics

# Sample output:
# prediction_requests_total 42
# prediction_latency_seconds_bucket{le="0.1"} 35
# predictions_by_class{class_name="cat"} 20
# predictions_by_class{class_name="dog"} 22
```

### Health Monitoring
```bash
# Health check
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Testing Strategy

### Unit Tests
- **Preprocessing tests:** Image resizing, transforms, normalization
- **Model tests:** Architecture, forward pass, output shape
- **API tests:** Endpoints, error handling, response format

### Integration Tests
- **Smoke tests:** Health check, prediction endpoint
- **End-to-end:** Full request/response cycle

### Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_inference.py -v
```

---

## Deployment Options

### Option 1: Docker Compose (Local)
```bash
docker-compose up -d
```
**Use case:** Local development and testing

### Option 2: Kubernetes (Production)
```bash
kubectl apply -f k8s/
```
**Use case:** Production deployment with scaling

### Option 3: Minikube (Local K8s)
```bash
minikube start
minikube image load cats-dogs-classifier:latest
kubectl apply -f k8s/
minikube service cats-dogs-classifier
```
**Use case:** Local Kubernetes testing

---

## Performance Considerations

### Model Optimization
- Input size: 224x224 (standard CNN input)
- Batch inference supported
- GPU acceleration available

### API Performance
- Async FastAPI for concurrency
- Request timeout: 30s
- Health check: 30s interval

### Kubernetes Scaling
- Horizontal Pod Autoscaler ready
- Resource requests: 250m CPU, 512Mi RAM
- Resource limits: 500m CPU, 1Gi RAM

---

## Security Best Practices

✓ No credentials in code
✓ Secrets managed via GitHub Secrets
✓ Docker image scanning (can be added)
✓ RBAC for Kubernetes (can be configured)
✓ API rate limiting (can be added)
✓ Input validation on API endpoints

---

## Troubleshooting

### Common Issues

**1. Model not found**
```bash
# Create dummy model for testing
python create_dummy_model.py
```

**2. Docker build fails**
```bash
# Check Docker daemon
docker info

# Clean build cache
docker system prune -a
```

**3. Kubernetes pods not starting**
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

**4. Tests failing**
```bash
# Install test dependencies
pip install pytest pytest-cov

# Create dummy model
python create_dummy_model.py

# Run tests
pytest tests/ -v
```

---

## Future Enhancements

- [ ] Model versioning with MLflow Model Registry
- [ ] A/B testing deployment strategy
- [ ] Prometheus + Grafana dashboard
- [ ] Automated model retraining pipeline
- [ ] Data drift detection
- [ ] Model performance monitoring
- [ ] API authentication and authorization
- [ ] Rate limiting and throttling
- [ ] Multi-model serving
- [ ] GPU support in Kubernetes

---

## References

- Dataset: https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset
- MLflow: https://mlflow.org/
- DVC: https://dvc.org/
- FastAPI: https://fastapi.tiangolo.com/
- Kubernetes: https://kubernetes.io/

---

## License

This project is for educational purposes as part of MLOps coursework.

## Author

BITS Mtech - MLOps Assignment 2
