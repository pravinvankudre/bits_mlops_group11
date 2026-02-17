#!/usr/bin/env python3
"""Smoke tests for deployed service."""

import sys
import requests
from PIL import Image
import io
import time

def test_health_check(base_url):
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health", timeout=10)
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", "Service not healthy"
    print("✓ Health check passed")

def test_prediction(base_url):
    """Test prediction endpoint."""
    print("Testing prediction endpoint...")
    
    # Create test image
    img = Image.new('RGB', (224, 224), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Make prediction request
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    response = requests.post(f"{base_url}/predict", files=files, timeout=30)
    
    assert response.status_code == 200, f"Prediction failed: {response.status_code}"
    data = response.json()
    
    assert "prediction" in data, "Missing prediction in response"
    assert "confidence" in data, "Missing confidence in response"
    assert "probabilities" in data, "Missing probabilities in response"
    
    print(f"✓ Prediction passed: {data['prediction']} (confidence: {data['confidence']:.2f})")

def main():
    if len(sys.argv) < 2:
        base_url = "http://localhost:8000"
    else:
        base_url = sys.argv[1]
    
    print(f"Running smoke tests against {base_url}")
    
    # Wait for service to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            requests.get(f"{base_url}/health", timeout=5)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                print("✗ Service not ready after 30 attempts")
                sys.exit(1)
            time.sleep(2)
    
    try:
        test_health_check(base_url)
        test_prediction(base_url)
        print("\n✓ All smoke tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Smoke tests failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
