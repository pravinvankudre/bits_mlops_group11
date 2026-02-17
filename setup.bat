@echo off
REM Quick Setup Script for MLOps Assignment 2

echo ========================================
echo MLOps Assignment 2 - Quick Setup
echo ========================================
echo.

echo [1/8] Creating directories...
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "models" mkdir models
if not exist "dvc-storage" mkdir dvc-storage
echo Done!
echo.

echo [2/8] Installing Python dependencies...
pip install -r requirements.txt
echo Done!
echo.

echo [3/8] Downloading dataset from Kaggle...
python download_dataset.py
echo Done!
echo.

echo [4/8] Preparing dataset...
python prepare_data.py
echo Done!
echo.

echo [5/8] Initializing Git...
git init
git add .
git commit -m "Initial commit - MLOps Assignment 2"
echo Done!
echo.

echo [6/8] Initializing DVC...
dvc init
echo Done!
echo.

echo [7/8] Creating dummy model for testing...
python create_dummy_model.py
echo Done!
echo.

echo [8/8] Running tests...
pytest tests/ -v
echo Done!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Train model: python src/train.py
echo 2. Build Docker: docker build -t cats-dogs-classifier:latest .
echo 3. Deploy to K8s: kubectl apply -f k8s/
echo.
echo For detailed instructions, see SETUP_GUIDE.md
echo ========================================
