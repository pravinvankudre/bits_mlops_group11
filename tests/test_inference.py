import pytest
import torch
from PIL import Image
import io
import os
from fastapi.testclient import TestClient

from src.model import get_model, CatsDogsCNN
from src.inference import app

# Create dummy model before tests
@pytest.fixture(scope="module", autouse=True)
def setup_model():
    os.makedirs("models", exist_ok=True)
    model = get_model(num_classes=2)
    torch.save(model.state_dict(), "models/model.pth")
    with open("models/classes.txt", "w") as f:
        f.write("cat\ndog")
    # Manually trigger startup to load model
    from src.inference import load_model
    load_model()
    yield

client = TestClient(app)

def test_model_creation():
    """Test model instantiation."""
    model = get_model(num_classes=2)
    
    assert isinstance(model, CatsDogsCNN), "Model should be instance of CatsDogsCNN"
    assert model.fc2.out_features == 2, "Model should have 2 output classes"

def test_model_forward_pass():
    """Test model forward pass with dummy input."""
    model = get_model(num_classes=2)
    model.eval()
    
    # Create dummy input (batch_size=1, channels=3, height=224, width=224)
    dummy_input = torch.randn(1, 3, 224, 224)
    
    with torch.no_grad():
        output = model(dummy_input)
    
    assert output.shape == (1, 2), f"Expected output shape (1, 2), got {output.shape}"

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200, "Health check should return 200"
    data = response.json()
    assert "status" in data, "Response should contain status"
    assert data["status"] == "healthy", "Status should be healthy"

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200, "Root endpoint should return 200"
    data = response.json()
    assert "message" in data, "Response should contain message"
    assert "endpoints" in data, "Response should contain endpoints info"

def test_predict_endpoint_with_invalid_file():
    """Test prediction endpoint with non-image file."""
    # Create a text file
    file_content = b"This is not an image"
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post("/predict", files=files)
    
    # Should return error (either 400 or 500 is acceptable for invalid input)
    assert response.status_code in [400, 500], "Should return error for non-image file"

def test_predict_endpoint_with_image():
    """Test prediction endpoint with valid image."""
    # Create a test image
    img = Image.new('RGB', (224, 224), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    files = {"file": ("test.jpg", img_byte_arr, "image/jpeg")}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200, "Should return 200 for valid image"
    data = response.json()
    assert "prediction" in data, "Response should contain prediction"
    assert "confidence" in data, "Response should contain confidence"
    assert "probabilities" in data, "Response should contain probabilities"
