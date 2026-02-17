# Screen Recording Script (<5 minutes)

## Preparation (Before Recording)
1. Have dataset downloaded and processed
2. Train model once: `python src/train.py`
3. Setup GitHub repo with secrets configured
4. Have Kubernetes cluster running (minikube/kind)
5. Have a test image ready

---

## Recording Script (4-5 minutes)

### Part 1: Introduction (30 seconds)
**Show:**
- Project structure in IDE
- README.md overview

**Say:**
"This is an end-to-end MLOps pipeline for Cats vs Dogs classification covering model training, containerization, CI/CD, and deployment."

---

### Part 2: Code Change & Git Push (45 seconds)

**Action:**
```bash
# Make a small change (e.g., update model or add comment)
# Open src/model.py and add a comment

# Git workflow
git status
git add .
git commit -m "Update model architecture"
git push origin main
```

**Show:**
- File modification in IDE
- Git commands in terminal
- Push confirmation

---

### Part 3: CI Pipeline Execution (60 seconds)

**Show:**
- Open GitHub repository in browser
- Navigate to Actions tab
- Show running workflow
- Expand test job - show tests passing
- Expand build job - show Docker image building
- Show successful completion

**Say:**
"The CI pipeline automatically runs tests, builds the Docker image, and pushes to Docker Hub."

---

### Part 4: Deployment (60 seconds)

**Action:**
```bash
# Show Kubernetes deployment
kubectl get pods
kubectl get svc

# Show logs
kubectl logs -f deployment/cats-dogs-classifier

# Port forward if needed
kubectl port-forward svc/cats-dogs-classifier 8000:8000
```

**Show:**
- Pods running
- Service created
- Logs showing application startup

**Say:**
"The CD pipeline automatically deploys the new image to Kubernetes."

---

### Part 5: Testing Deployed Model (60 seconds)

**Action:**
```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST -F "file=@test_cat.jpg" http://localhost:8000/predict
```

**Show:**
- Health check response (JSON)
- Prediction response with confidence scores
- Logs showing the request

**Say:**
"The deployed model successfully predicts cat/dog with confidence scores."

---

### Part 6: Monitoring & Metrics (30 seconds)

**Action:**
```bash
# Show metrics
curl http://localhost:8000/metrics

# Show MLflow UI
mlflow ui --port 5000
# Open browser to localhost:5000
```

**Show:**
- Prometheus metrics output
- MLflow experiments dashboard
- Confusion matrix and loss curves

**Say:**
"All experiments are tracked in MLflow with metrics and artifacts."

---

### Part 7: Conclusion (15 seconds)

**Show:**
- Quick overview of all components:
  - DVC for data versioning
  - MLflow for experiments
  - Docker for containerization
  - GitHub Actions for CI/CD
  - Kubernetes for deployment
  - Prometheus for monitoring

**Say:**
"This completes the end-to-end MLOps pipeline from code change to production deployment."

---

## Recording Tips

1. **Use screen recording software:**
   - Windows: OBS Studio, Xbox Game Bar
   - Mac: QuickTime, ScreenFlow
   - Linux: SimpleScreenRecorder, OBS

2. **Prepare terminal:**
   - Use large font (16-18pt)
   - Clear terminal before recording
   - Use clear, contrasting colors

3. **Browser:**
   - Close unnecessary tabs
   - Zoom in for visibility
   - Use full screen mode

4. **Timing:**
   - Practice once before recording
   - Keep it under 5 minutes
   - Speak clearly and at moderate pace

5. **What to show:**
   - ✓ Code change
   - ✓ Git commit/push
   - ✓ CI pipeline running
   - ✓ Tests passing
   - ✓ Docker build
   - ✓ Deployment to K8s
   - ✓ Prediction on deployed model
   - ✓ Monitoring/metrics

6. **What to skip:**
   - Long build times (fast forward or cut)
   - Repetitive commands
   - Error troubleshooting
   - Detailed code explanation

---

## Alternative: Quick Demo Script (If time is short)

### 2-Minute Version

1. **Show project structure** (15s)
2. **Git push** (15s)
3. **GitHub Actions running** (30s)
4. **Deployed service prediction** (45s)
5. **Metrics dashboard** (15s)

---

## Checklist Before Recording

- [ ] Dataset prepared
- [ ] Model trained
- [ ] Tests passing locally
- [ ] Docker image builds
- [ ] K8s cluster running
- [ ] GitHub repo setup
- [ ] Secrets configured
- [ ] Test image ready
- [ ] Terminal font large
- [ ] Browser tabs cleaned
- [ ] Recording software tested

---

## Post-Recording

1. **Review video:**
   - Check audio quality
   - Verify all steps visible
   - Ensure under 5 minutes

2. **Edit if needed:**
   - Cut long waits
   - Add annotations if helpful
   - Ensure smooth transitions

3. **Export:**
   - Format: MP4 (H.264)
   - Resolution: 1080p
   - Keep file size reasonable (<100MB)

4. **Upload:**
   - If <100MB: Include in zip
   - If >100MB: Upload to Google Drive/OneDrive and share link

---

## Sample Commands Reference

```bash
# Setup
pip install -r requirements.txt
python prepare_data.py
python src/train.py

# Create dummy model for quick testing
python create_dummy_model.py

# Run tests
pytest tests/ -v

# Docker
docker build -t cats-dogs-classifier:latest .
docker run -p 8000:8000 cats-dogs-classifier:latest

# Kubernetes
kubectl apply -f k8s/
kubectl get all
kubectl logs -f deployment/cats-dogs-classifier
kubectl port-forward svc/cats-dogs-classifier 8000:8000

# Testing
curl http://localhost:8000/health
curl -X POST -F "file=@test.jpg" http://localhost:8000/predict
curl http://localhost:8000/metrics

# MLflow
mlflow ui --port 5000

# Smoke tests
python smoke_tests.py

# Git
git add .
git commit -m "Update model"
git push origin main
```
