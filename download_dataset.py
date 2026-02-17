"""
Automated dataset download from Kaggle.
Requires: pip install kaggle
Setup: Place kaggle.json in ~/.kaggle/ or set KAGGLE_USERNAME and KAGGLE_KEY
"""

import os
import zipfile
from pathlib import Path
import subprocess
import sys

def download_dataset():
    """Download and extract Cats vs Dogs dataset from Kaggle."""
    
    # Create directories
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if data already exists
    if (raw_dir / "Cat").exists() and (raw_dir / "Dog").exists():
        print("Dataset already exists in data/raw/")
        return True
    
    print("Downloading dataset from Kaggle...")
    
    try:
        # Install kaggle if not present
        try:
            import kaggle
        except ImportError:
            print("Installing kaggle package...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
            import kaggle
        
        # Download dataset
        dataset_name = "bhavikjikadara/dog-and-cat-classification-dataset"
        
        print(f"Downloading {dataset_name}...")
        subprocess.run([
            "kaggle", "datasets", "download", 
            "-d", dataset_name,
            "-p", str(raw_dir),
            "--unzip"
        ], check=True)
        
        # Check if extraction created nested folders
        extracted_folders = list(raw_dir.glob("*/"))
        if extracted_folders and not (raw_dir / "Cat").exists():
            # Move files from nested directory
            nested_dir = extracted_folders[0]
            if (nested_dir / "Cat").exists():
                import shutil
                shutil.move(str(nested_dir / "Cat"), str(raw_dir / "Cat"))
                shutil.move(str(nested_dir / "Dog"), str(raw_dir / "Dog"))
                shutil.rmtree(nested_dir)
        
        print("✓ Dataset downloaded successfully!")
        print(f"  - Cat images: {len(list((raw_dir / 'Cat').glob('*')))}")
        print(f"  - Dog images: {len(list((raw_dir / 'Dog').glob('*')))}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error downloading dataset: {e}")
        print("\nManual setup required:")
        print("1. Install kaggle: pip install kaggle")
        print("2. Setup Kaggle API credentials:")
        print("   - Go to https://www.kaggle.com/settings")
        print("   - Click 'Create New API Token'")
        print("   - Place kaggle.json in ~/.kaggle/ (Linux/Mac) or C:\\Users\\<user>\\.kaggle\\ (Windows)")
        print("3. Run this script again")
        print("\nOR download manually:")
        print("https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = download_dataset()
    if success:
        print("\nNext step: Run 'python prepare_data.py' to preprocess images")
    sys.exit(0 if success else 1)
