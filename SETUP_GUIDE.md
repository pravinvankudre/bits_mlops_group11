# MLOps Assignment 2 - Setup & Execution Guide

## Module 1: Model Development & Experiment Tracking

### Setup
1. **Initialize Git repository:**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Initialize DVC:**
```bash
pip install dvc
dvc init
dvc remote add -d storage ./dvc-storage
git add .dvc/config
git commit -m "Initialize DVC"
```

3. **Download and prepare dataset:**
- Download from: https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset
- Extract to `data/raw/` with folders `Cat/` and `Dog/`
- Run: `python prepare_data.py`

4. **Track data with DVC:**
```bash
dvc add data/processed
git add data/processed.dvc .gitignore
git commit -m "Track processed data with DVC"
```

5. **Train model with MLflow tracking:**
```bash
python src/train.py
```

6. **View MLflow experiments:**
```bash
mlflow ui --port 5000
```
Open http://localhost:5000

---

## Module 2: Model Packaging & Containerization

### Build and test locally

1. **Test inference service:**
```bash
uvicorn src.inference:app --reload
```

2. **Test endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Prediction (Windows PowerShell)
curl -X POST -F "file=@test_image.jpg" http://localhost:8000/predict
```

3. **Build Docker image:**
```bash
docker build -t cats-dogs-classifier:latest .
```

4. **Run container:**
```bash
docker run -p 8000:8000 cats-dogs-classifier:latest
```

5. **Test with docker-compose:**
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Module 3: CI Pipeline

### Setup GitHub Actions

1. **Create GitHub repository and push code:**
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Add GitHub Secrets:**
- Go to Settings → Secrets and variables → Actions
- Add:
  - `DOCKER_USERNAME`: Your Docker Hub username
  - `DOCKER_PASSWORD`: Your Docker Hub password/token
  - `KUBECONFIG`: Base64 encoded kubeconfig (for CD)

3. **Run tests locally:**
```bash
pytest tests/ -v
```

4. **Pipeline triggers automatically on push to main**

---

## Module 4: CD Pipeline & Deployment

### Local Kubernetes Deployment

1. **Install minikube/kind:**
```bash
# Windows (using Chocolatey)
choco install minikube

# Or kind
choco install kind
```

2. **Start cluster:**
```bash
minikube start
# or
kind create cluster
```

3. **Load Docker image to cluster:**
```bash
# For minikube
minikube image load cats-dogs-classifier:latest

# For kind
kind load docker-image cats-dogs-classifier:latest
```

4. **Deploy to Kubernetes:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

5. **Check deployment:**
```bash
kubectl get pods
kubectl get svc
kubectl logs -f deployment/cats-dogs-classifier
```

6. **Access service:**
```bash
# For minikube
minikube service cats-dogs-classifier

# For kind (port-forward)
kubectl port-forward svc/cats-dogs-classifier 8000:8000
```

7. **Run smoke tests:**
```bash
python smoke_tests.py http://localhost:8000
```

---

## Module 5: Monitoring & Logs

### View Metrics

1. **Prometheus metrics endpoint:**
```bash
curl http://localhost:8000/metrics
```

2. **View application logs:**
```bash
# Docker
docker logs cats-dogs-classifier

# Kubernetes
kubectl logs -f deployment/cats-dogs-classifier
```

3. **Monitor predictions:**
- Check logs for request/response details
- View metrics: request count, latency, predictions by class

---

## Testing the Complete Pipeline

1. **Make a code change**
2. **Commit and push:**
```bash
git add .
git commit -m "Update model"
git push origin main
```
3. **CI/CD pipeline will:**
   - Run tests
   - Build Docker image
   - Push to registry
   - Deploy to Kubernetes
   - Run smoke tests

---

## Deliverables Checklist

- [ ] Source code with all modules
- [ ] DVC configuration for data versioning
- [ ] MLflow experiment tracking logs
- [ ] Dockerfile and docker-compose.yml
- [ ] GitHub Actions CI/CD pipeline
- [ ] Kubernetes manifests
- [ ] Unit tests (pytest)
- [ ] Smoke tests
- [ ] README and documentation
- [ ] Screen recording (<5 min) showing:
  - Code change
  - Git commit/push
  - CI/CD pipeline execution
  - Automated deployment
  - Prediction on deployed model

---

## Troubleshooting

**Issue: Model file not found**
- Ensure you've run `python src/train.py` first
- Check `models/model.pth` exists

**Issue: Docker build fails**
- Ensure models directory exists with model.pth and classes.txt
- Check Docker daemon is running

**Issue: Kubernetes pods not starting**
- Check image is loaded: `kubectl describe pod <pod-name>`
- Verify resource limits
- Check logs: `kubectl logs <pod-name>`

**Issue: Tests failing**
- Install test dependencies: `pip install pytest`
- Ensure dummy model exists for tests
