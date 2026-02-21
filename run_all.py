#!/usr/bin/env python3
"""
End-to-End MLOps Pipeline Runner
Executes complete workflow: Data -> Training -> Testing -> Docker -> Deployment
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """Execute command and handle errors."""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print('='*70)
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            cwd=cwd,
            capture_output=False,
            text=True
        )
        print(f" {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f" {description} - FAILED")
        print(f"Error: {e}")
        return False

def check_prerequisites():
    """Check if required tools are installed."""
    print("\n" + "="*70)
    print("  Checking Prerequisites")
    print("="*70)
    
    tools = {
        'python': 'python --version',
        'docker': 'docker --version',
        'kubectl': 'kubectl version --client',
    }
    
    missing = []
    for tool, cmd in tools.items():
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f" {tool} found")
        except:
            print(f" {tool} not found")
            if tool != 'kubectl':  # kubectl optional for local testing
                missing.append(tool)
    
    if missing:
        print(f"\n Missing required tools: {', '.join(missing)}")
        return False
    return True

def main():
    """Run complete MLOps pipeline."""
    
    print("\n" + "="*70)
    print("  MLOps Assignment 2 - End-to-End Pipeline")
    print("  Cats vs Dogs Classification")
    print("="*70)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n Prerequisites check failed. Install missing tools and retry.")
        sys.exit(1)
    
    # Pipeline steps
    steps = [
        # Step 1: Setup and Data Preparation
        {
            'cmd': f'{sys.executable} -m pip install -r requirements.txt',
            'desc': 'Step 1: Install Dependencies',
            'critical': True
        },
        {
            'cmd': f'{sys.executable} download_dataset.py',
            'desc': 'Step 2: Download Dataset from Kaggle',
            'critical': True
        },
        {
            'cmd': f'{sys.executable} prepare_data.py',
            'desc': 'Step 3: Preprocess Images (224x224)',
            'critical': True
        },
        
        # Step 2: DVC Tracking
        {
            'cmd': 'dvc add data/processed',
            'desc': 'Step 4: Track Data with DVC',
            'critical': False
        },
        
        # Step 3: Model Training
        {
            'cmd': f'{sys.executable} src/train.py',
            'desc': 'Step 5: Train Model with MLflow Tracking (3 epochs, 50 batches each)',
            'critical': True
        },
        
        # Step 4: Testing
        {
            'cmd': 'pytest tests/ -v --cov=src --cov-report=term',
            'desc': 'Step 6: Run Unit Tests',
            'critical': True
        },
        
        # Step 5: Docker Build
        {
            'cmd': 'docker build -t cats-dogs-classifier:latest .',
            'desc': 'Step 7: Build Docker Image',
            'critical': True
        },
        
        # Step 6: Local Deployment Test
        {
            'cmd': 'docker-compose up -d',
            'desc': 'Step 8: Deploy with Docker Compose',
            'critical': True
        },
    ]
    
    # Execute pipeline
    failed_steps = []
    for i, step in enumerate(steps, 1):
        success = run_command(step['cmd'], step['desc'])
        
        if not success:
            if step['critical']:
                print(f"\n✗ Critical step failed: {step['desc']}")
                print("Pipeline execution stopped.")
                sys.exit(1)
            else:
                failed_steps.append(step['desc'])
                print(f"⚠ Non-critical step failed: {step['desc']}")
                print("Continuing with next step...")
    
    # Wait for service to start
    print("\n" + "="*70)
    print("  Waiting for service to start...")
    print("="*70)
    time.sleep(10)
    
    # Run smoke tests
    smoke_test_success = run_command(
        f'{sys.executable} smoke_tests.py http://localhost:8000',
        'Step 9: Run Smoke Tests (Health + Prediction)',
    )
    
    if not smoke_test_success:
        print("\n SMOKE TESTS FAILED - Pipeline failed")
        print("Check service logs: docker-compose logs")
        sys.exit(1)
    
    # Start MLflow UI
    print("\n" + "="*70)
    print("  Starting MLflow UI")
    print("="*70)
    try:
        subprocess.Popen(
            'mlflow ui --port 5000',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[OK] MLflow UI started at http://localhost:5000")
    except:
        print("[WARN] Could not start MLflow UI")
    
    # Final Summary
    print("\n" + "="*70)
    print("  PIPELINE EXECUTION SUMMARY")
    print("="*70)
    
    if not failed_steps:
        print("\n[OK] ALL STEPS COMPLETED SUCCESSFULLY!")
        print("\nDeployment Status:")
        print("  - Service running at: http://localhost:8000")
        print("  - Health check: http://localhost:8000/health")
        print("  - API docs: http://localhost:8000/docs")
        print("  - MLflow UI: http://localhost:5000")
        print("\nNext Steps:")
        print("  - Test prediction: curl -X POST http://localhost:8000/predict -F 'file=@test_image.jpg'")
        print("  - View logs: docker-compose logs -f")
        print("  - Stop service: docker-compose down")
        print("  - Deploy to K8s: kubectl apply -f k8s/")
    else:
        print("\n[WARN] PIPELINE COMPLETED WITH WARNINGS")
        print("\nFailed non-critical steps:")
        for step in failed_steps:
            print(f"  - {step}")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Pipeline interrupted by user")
        print("Cleaning up...")
        subprocess.run("docker-compose down", shell=True, capture_output=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        sys.exit(1)
