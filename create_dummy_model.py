"""Create dummy model for testing purposes."""

import torch
from pathlib import Path
from src.model import get_model

def create_dummy_model():
    """Create and save a dummy model for testing."""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Create model
    model = get_model(num_classes=2)
    
    # Save model
    torch.save(model.state_dict(), models_dir / "model.pth")
    print(f"Saved model to {models_dir / 'model.pth'}")
    
    # Save classes
    with open(models_dir / "classes.txt", "w") as f:
        f.write("cat\ndog")
    print(f"Saved classes to {models_dir / 'classes.txt'}")

if __name__ == "__main__":
    create_dummy_model()
