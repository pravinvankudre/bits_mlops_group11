# Assignment 2 - Submission Checklist

## Module 1: Model Development & Experiment Tracking (10M)

### Data & Code Versioning
- [ ] Git repository initialized
- [ ] All source code committed to Git
- [ ] DVC initialized and configured
- [ ] Dataset tracked with DVC (data.dvc file)
- [ ] .gitignore properly configured

### Model Building
- [ ] Baseline CNN model implemented (src/model.py)
- [ ] Model architecture documented
- [ ] Training script created (src/train.py)
- [ ] Model saved in .pth format
- [ ] Data preprocessing implemented with augmentation

### Experiment Tracking
- [ ] MLflow integrated in training script
- [ ] Parameters logged (epochs, batch_size, lr)
- [ ] Metrics logged (train/val/test accuracy, loss)
- [ ] Artifacts saved (confusion matrix, loss curves)
- [ ] MLflow runs visible in UI

**Files to verify:**
- src/model.py
- src/train.py
- src/data_preprocessing.py
- .dvc/config
- models/model.pth
- mlruns/ directory

---

## Module 2: Model Packaging & Containerization (10M)

### Inference Service
- [ ] FastAPI application created (src/inference.py)
- [ ] Health check endpoint implemented (/health)
- [ ] Prediction endpoint implemented (/predict)
- [ ] Accepts image file and returns predictions
- [ ] Returns class probabilities and confidence

### Environment Specification
- [ ] requirements.txt with pinned versions
- [ ] All dependencies listed
- [ ] Version compatibility verified

### Containerization
- [ ] Dockerfile created
- [ ] Docker image builds successfully
- [ ] Container runs locally
- [ ] Health check configured in Dockerfile
- [ ] Predictions verified via curl/Postman
- [ ] docker-compose.yml created

**Files to verify:**
- src/inference.py
- Dockerfile
- docker-compose.yml
- requirements.txt

**Test commands:**
```bash
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest
curl http://localhost:8000/health
```

---

## Module 3: CI Pipeline for Build, Test & Image Creation (10M)

### Automated Testing
- [ ] Unit test for preprocessing function (test_preprocessing.py)
- [ ] Unit test for inference function (test_inference.py)
- [ ] Tests run successfully with pytest
- [ ] Test coverage adequate
- [ ] pytest.ini configured

### CI Setup
- [ ] GitHub Actions workflow created (.github/workflows/ci-cd.yml)
- [ ] Pipeline checks out repository
- [ ] Pipeline installs dependencies
- [ ] Pipeline runs unit tests
- [ ] Pipeline builds Docker image
- [ ] Pipeline triggers on push/merge

### Artifact Publishing
- [ ] Docker Hub account created
- [ ] GitHub secrets configured (DOCKER_USERNAME, DOCKER_PASSWORD)
- [ ] Pipeline pushes image to registry
- [ ] Image tagged properly
- [ ] Build cache configured

**Files to verify:**
- tests/test_preprocessing.py
- tests/test_inference.py
- .github/workflows/ci-cd.yml
- pytest.ini

**Test commands:**
```bash
pytest tests/ -v
```

---

## Module 4: CD Pipeline & Deployment (10M)

### Deployment Target
- [ ] Kubernetes chosen as deployment target
- [ ] Deployment manifest created (k8s/deployment.yaml)
- [ ] Service manifest created (k8s/service.yaml)
- [ ] Resource limits configured
- [ ] Replicas configured (2+)
- [ ] Liveness/readiness probes configured

### CD / GitOps Flow
- [ ] CD pipeline extends CI workflow
- [ ] Pipeline pulls new image from registry
- [ ] Pipeline updates Kubernetes deployment
- [ ] Deployment triggers on main branch changes
- [ ] Rollout status checked

### Smoke Tests / Health Check
- [ ] Smoke test script created (smoke_tests.py)
- [ ] Health endpoint tested post-deploy
- [ ] Prediction endpoint tested post-deploy
- [ ] Pipeline fails if smoke tests fail

**Files to verify:**
- k8s/deployment.yaml
- k8s/service.yaml
- smoke_tests.py

**Test commands:**
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
python smoke_tests.py
```

---

## Module 5: Monitoring, Logs & Final Submission (10M)

### Basic Monitoring & Logging
- [ ] Request/response logging enabled
- [ ] Structured logging format
- [ ] Sensitive data excluded from logs
- [ ] Logs accessible via kubectl/docker logs

### Model Performance Tracking
- [ ] Prometheus metrics integrated
- [ ] Request count tracked
- [ ] Latency tracked
- [ ] Predictions by class tracked
- [ ] Metrics endpoint exposed (/metrics)

### Documentation
- [ ] README.md comprehensive
- [ ] SETUP_GUIDE.md detailed
- [ ] DOCUMENTATION.md complete
- [ ] All commands documented
- [ ] Architecture diagram included

**Files to verify:**
- src/inference.py (logging and metrics)
- README.md
- SETUP_GUIDE.md
- DOCUMENTATION.md

**Test commands:**
```bash
curl http://localhost:8000/metrics
kubectl logs -f deployment/cats-dogs-classifier
```

---

## Final Deliverables

### 1. Source Code Package
- [ ] All source code files
- [ ] Configuration files
- [ ] Test files
- [ ] Documentation files

### 2. Configuration Files
- [ ] DVC configuration
- [ ] Docker configuration
- [ ] Kubernetes manifests
- [ ] CI/CD pipeline configuration

### 3. Trained Model Artifacts
- [ ] model.pth file
- [ ] classes.txt file
- [ ] MLflow artifacts

### 4. Screen Recording
- [ ] Recording completed
- [ ] Duration < 5 minutes
- [ ] Shows complete workflow:
  - [ ] Code change
  - [ ] Git commit/push
  - [ ] CI pipeline execution
  - [ ] Tests passing
  - [ ] Docker build
  - [ ] Deployment
  - [ ] Prediction on deployed model
- [ ] Audio clear (if narrated)
- [ ] Screen visible and readable
- [ ] File format: MP4
- [ ] File size reasonable

### 5. Submission Package
- [ ] Create zip file with all contents
- [ ] Include video (if <100MB) or link
- [ ] Verify zip extracts correctly
- [ ] Test on clean environment if possible

---

## Pre-Submission Testing

### Local Testing
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create dummy model
python create_dummy_model.py

# 3. Run tests
pytest tests/ -v

# 4. Build Docker
docker build -t cats-dogs-classifier:latest .

# 5. Run container
docker run -p 8000:8000 cats-dogs-classifier:latest

# 6. Test endpoints
curl http://localhost:8000/health
curl -X POST -F "file=@test.jpg" http://localhost:8000/predict

# 7. Run smoke tests
python smoke_tests.py
```

### CI/CD Testing
```bash
# 1. Push to GitHub
git push origin main

# 2. Check GitHub Actions
# - Open repository in browser
# - Go to Actions tab
# - Verify workflow runs successfully

# 3. Check Docker Hub
# - Verify image pushed
# - Check image tags
```

### Kubernetes Testing
```bash
# 1. Start cluster
minikube start  # or kind create cluster

# 2. Load image
minikube image load cats-dogs-classifier:latest

# 3. Deploy
kubectl apply -f k8s/

# 4. Verify
kubectl get pods
kubectl get svc
kubectl logs -f deployment/cats-dogs-classifier

# 5. Test
kubectl port-forward svc/cats-dogs-classifier 8000:8000
python smoke_tests.py
```

---

## Common Issues to Check

- [ ] No hardcoded credentials in code
- [ ] No absolute paths (use relative paths)
- [ ] All imports work correctly
- [ ] Model file exists before Docker build
- [ ] .gitignore excludes large files
- [ ] Requirements.txt has all dependencies
- [ ] Docker image size reasonable (<2GB)
- [ ] Tests don't require actual dataset
- [ ] Documentation is clear and complete
- [ ] All commands in docs are correct

---

## Grading Criteria Mapping

### M1 (10M)
- Git versioning: 2M
- DVC setup: 2M
- Model implementation: 3M
- MLflow tracking: 3M

### M2 (10M)
- FastAPI service: 4M
- Environment spec: 2M
- Dockerization: 4M

### M3 (10M)
- Unit tests: 4M
- CI pipeline: 4M
- Image publishing: 2M

### M4 (10M)
- Deployment setup: 4M
- CD pipeline: 4M
- Smoke tests: 2M

### M5 (10M)
- Logging: 3M
- Metrics: 3M
- Documentation: 2M
- Video: 2M

**Total: 50M**

---

## Final Checklist

- [ ] All 5 modules completed
- [ ] All code tested locally
- [ ] CI/CD pipeline working
- [ ] Deployment successful
- [ ] Screen recording done
- [ ] Documentation complete
- [ ] Zip file created
- [ ] Submission ready

---

## Submission Format

```
Assignment_2_<YourName>.zip
├── src/
├── tests/
├── k8s/
├── .github/
├── .dvc/
├── models/
├── notebooks/
├── README.md
├── SETUP_GUIDE.md
├── DOCUMENTATION.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .gitignore
├── smoke_tests.py
├── prepare_data.py
├── create_dummy_model.py
└── demo_video.mp4 (or link.txt with video URL)
```

---

## Post-Submission

- [ ] Verify submission uploaded successfully
- [ ] Keep local copy as backup
- [ ] Note submission timestamp
- [ ] Confirm file size acceptable

---

Good luck! 🚀
