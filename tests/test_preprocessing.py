import pytest
import torch
from PIL import Image
import numpy as np
from pathlib import Path
import tempfile
import os

from src.data_preprocessing import preprocess_image, get_transforms

def test_preprocess_image():
    """Test image preprocessing to target size."""
    # Create a temporary test image
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Test preprocessing
        processed_img = preprocess_image(tmp_path, target_size=(224, 224))
        
        assert processed_img.size == (224, 224), "Image not resized correctly"
        assert processed_img.mode == 'RGB', "Image not in RGB mode"
    finally:
        os.unlink(tmp_path)

def test_get_transforms_with_augmentation():
    """Test transforms with augmentation enabled."""
    transform = get_transforms(augment=True)
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='blue')
    
    # Apply transform
    tensor = transform(img)
    
    assert isinstance(tensor, torch.Tensor), "Output should be a tensor"
    assert tensor.shape == (3, 224, 224), f"Expected shape (3, 224, 224), got {tensor.shape}"
    assert tensor.dtype == torch.float32, "Tensor should be float32"

def test_get_transforms_without_augmentation():
    """Test transforms without augmentation."""
    transform = get_transforms(augment=False)
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='green')
    
    # Apply transform
    tensor = transform(img)
    
    assert isinstance(tensor, torch.Tensor), "Output should be a tensor"
    assert tensor.shape == (3, 224, 224), f"Expected shape (3, 224, 224), got {tensor.shape}"

def test_transform_normalization():
    """Test that transforms apply normalization."""
    transform = get_transforms(augment=False)
    
    # Create white image
    img = Image.new('RGB', (224, 224), color='white')
    tensor = transform(img)
    
    # Check that values are normalized (not in 0-255 range)
    assert tensor.max() <= 3.0, "Values should be normalized"
    assert tensor.min() >= -3.0, "Values should be normalized"
