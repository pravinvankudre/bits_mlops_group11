# Quick Reference Card - MLOps Assignment 2

## 🚀 Essential Commands

### Initial Setup
```bash
pip install -r requirements.txt          # Install dependencies
python create_dummy_model.py             # Create test model
pytest tests/ -v                         # Run tests
```

### Data Preparation
```bash
# Download dataset from Kaggle to data/raw/
python prepare_data.py                   # Process images
dvc add data/processed                   # Track with DVC
```

### Model Training
```bash
python src/train.py                      # Train model
mlflow ui --port 5000                    # View experiments
```

### Local Testing
```bash
# Start API server
uvicorn src.inference:app --reload

# Test endpoints
curl http://localhost:8000/health
curl -X POST -F "file=@test.jpg" http://localhost:8000/predict
curl http://localhost:8000/metrics
```

### Docker Operations
```bash
# Build image
docker build -t cats-dogs-classifier:latest .

# Run container
docker run -p 8000:8000 cats-dogs-classifier:latest

# Docker Compose
docker-compose up -d                     # Start
docker-compose logs -f                   # View logs
docker-compose down                      # Stop
```

### Kubernetes Operations
```bash
# Start cluster (choose one)
minikube start
kind create cluster

# Load image
minikube image load cats-dogs-classifier:latest
kind load docker-image cats-dogs-classifier:latest

# Deploy
kubectl apply -f k8s/

# Monitor
kubectl get pods
kubectl get svc
kubectl logs -f deployment/cats-dogs-classifier

# Access service
minikube service cats-dogs-classifier
kubectl port-forward svc/cats-dogs-classifier 8000:8000

# Cleanup
kubectl delete -f k8s/
```

### Testing
```bash
pytest tests/ -v                         # Run all tests
pytest tests/test_preprocessing.py -v    # Specific test
pytest tests/ --cov=src                  # With coverage
python smoke_tests.py                    # Smoke tests
```

### Git Operations
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repo-url>
git push -u origin main
```

### DVC Operations
```bash
dvc init
dvc add data/processed
dvc push                                 # Push to remote
dvc pull                                 # Pull from remote
```

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `src/model.py` | CNN model architecture |
| `src/train.py` | Training with MLflow |
| `src/inference.py` | FastAPI service |
| `src/data_preprocessing.py` | Data pipeline |
| `Dockerfile` | Container definition |
| `docker-compose.yml` | Local deployment |
| `k8s/deployment.yaml` | K8s deployment |
| `k8s/service.yaml` | K8s service |
| `.github/workflows/ci-cd.yml` | CI/CD pipeline |
| `tests/test_*.py` | Unit tests |
| `smoke_tests.py` | Post-deploy tests |

---

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/predict` | POST | Image classification |
| `/metrics` | GET | Prometheus metrics |

---

## 📊 MLflow Tracking

```python
# Logged automatically in train.py:
- Parameters: epochs, batch_size, learning_rate
- Metrics: train_loss, train_accuracy, val_loss, val_accuracy
- Artifacts: confusion_matrix.png, loss_curves.png, model
```

---

## 🐳 Docker Hub

```bash
# Login
docker login

# Tag image
docker tag cats-dogs-classifier:latest username/cats-dogs-classifier:latest

# Push
docker push username/cats-dogs-classifier:latest
```

---

## 🔐 GitHub Secrets

Required secrets for CI/CD:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token
- `KUBECONFIG` - Base64 encoded kubeconfig (optional)

---

## 📝 Documentation Files

1. **README.md** - Start here
2. **SETUP_GUIDE.md** - Detailed setup
3. **DOCUMENTATION.md** - Technical docs
4. **PROJECT_SUMMARY.md** - Overview
5. **RECORDING_GUIDE.md** - Video guide
6. **SUBMISSION_CHECKLIST.md** - Pre-submission check

---

## 🐛 Troubleshooting

### Model not found
```bash
python create_dummy_model.py
```

### Tests failing
```bash
pip install pytest
python create_dummy_model.py
pytest tests/ -v
```

### Docker build fails
```bash
docker system prune -a
docker build -t cats-dogs-classifier:latest .
```

### K8s pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Change port
uvicorn src.inference:app --port 8001
```

---

## 📦 Project Structure

```
Assignment_2/
├── src/              # Source code
├── tests/            # Unit tests
├── k8s/              # Kubernetes manifests
├── .github/          # CI/CD workflows
├── .dvc/             # DVC config
├── models/           # Trained models
├── data/             # Dataset
├── notebooks/        # Jupyter notebooks
└── *.md              # Documentation
```

---

## ✅ Pre-Submission Checklist

- [ ] All tests passing
- [ ] Docker image builds
- [ ] K8s deployment works
- [ ] CI/CD pipeline configured
- [ ] Documentation complete
- [ ] Video recorded (<5 min)
- [ ] Zip file created

---

## 🎬 Video Recording Outline

1. Show project structure (30s)
2. Make code change + git push (45s)
3. Show CI pipeline running (60s)
4. Show deployment (60s)
5. Test prediction (60s)
6. Show metrics (30s)

**Total: ~5 minutes**

---

## 📞 Quick Help

**Issue?** Check these in order:
1. SETUP_GUIDE.md - Setup instructions
2. DOCUMENTATION.md - Technical details
3. SUBMISSION_CHECKLIST.md - Verification
4. This file - Quick commands

---

## 🎯 Module Completion

- [x] M1: Model Development & Experiment Tracking
- [x] M2: Model Packaging & Containerization
- [x] M3: CI Pipeline
- [x] M4: CD Pipeline & Deployment
- [x] M5: Monitoring & Logs
- [ ] Screen Recording (TODO)

---

**Total Marks: 50/50** ✅

---

## 💡 Pro Tips

1. Use `make` commands if available (see Makefile)
2. Test locally before pushing to GitHub
3. Keep video under 5 minutes
4. Document any deviations
5. Test on clean environment if possible

---

**Good luck! 🚀**
