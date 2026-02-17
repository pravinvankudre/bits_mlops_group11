# MLOps Assignment 2 - Cats vs Dogs Classification

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

## Setup

### Quick Setup (Automated)
```bash
pip install -r requirements.txt
python setup_all.py
```
This will automatically:
- Download dataset from Kaggle
- Preprocess images to 224x224
- Create initial model

### Manual Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize DVC
```bash
dvc init
dvc remote add -d storage ./dvc-storage
```

### 3. Download Dataset
```bash
python download_dataset.py
```
This will automatically download from Kaggle. First time setup:
1. Get Kaggle API token from https://www.kaggle.com/settings
2. Place kaggle.json in `~/.kaggle/` (or `C:\Users\<user>\.kaggle\` on Windows)

### 4. Train Model
```bash
python src/train.py
```

### 5. Run Inference Service
```bash
uvicorn src.inference:app --host 0.0.0.0 --port 8000
```

### 6. Build Docker Image
```bash
docker build -t cats-dogs-classifier:latest .
```

### 7. Deploy to Kubernetes
```bash
kubectl apply -f k8s/
```

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Prediction endpoint (accepts image file)

## Monitoring

- Request/response logging enabled
- Metrics: request count, latency, predictions
- MLflow UI: `mlflow ui --port 5000`
