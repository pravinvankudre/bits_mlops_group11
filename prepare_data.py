"""
Script to prepare the Cats vs Dogs dataset.
Download dataset from: https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset
Extract to data/raw/ directory with structure:
  data/raw/Cat/ - cat images
  data/raw/Dog/ - dog images
"""

import os
import shutil
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def prepare_dataset(raw_dir='data/raw', processed_dir='data/processed'):
    """Prepare and organize dataset."""
    
    raw_path = Path(raw_dir)
    processed_path = Path(processed_dir)
    
    # Create processed directory structure
    for split in ['cat', 'dog']:
        (processed_path / split).mkdir(parents=True, exist_ok=True)
    
    print("Processing images...")
    
    # Process cat images
    cat_dir = raw_path / 'Cat'
    if cat_dir.exists():
        cat_images = list(cat_dir.glob('*.jpg')) + list(cat_dir.glob('*.jpeg')) + list(cat_dir.glob('*.png'))
        for img_path in tqdm(cat_images, desc="Processing cats"):
            try:
                img = Image.open(img_path).convert('RGB')
                img = img.resize((224, 224), Image.BILINEAR)
                output_path = processed_path / 'cat' / img_path.name
                img.save(output_path, 'JPEG', quality=95)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    
    # Process dog images
    dog_dir = raw_path / 'Dog'
    if dog_dir.exists():
        dog_images = list(dog_dir.glob('*.jpg')) + list(dog_dir.glob('*.jpeg')) + list(dog_dir.glob('*.png'))
        for img_path in tqdm(dog_images, desc="Processing dogs"):
            try:
                img = Image.open(img_path).convert('RGB')
                img = img.resize((224, 224), Image.BILINEAR)
                output_path = processed_path / 'dog' / img_path.name
                img.save(output_path, 'JPEG', quality=95)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
    
    print(f"\nDataset prepared in {processed_dir}")
    print(f"Cats: {len(list((processed_path / 'cat').glob('*.jpg')))}")
    print(f"Dogs: {len(list((processed_path / 'dog').glob('*.jpg')))}")

if __name__ == "__main__":
    prepare_dataset()
