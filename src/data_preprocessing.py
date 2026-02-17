import os
import shutil
from pathlib import Path
from PIL import Image
import torch
from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess a single image to target size."""
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size, Image.BILINEAR)
    return img

def get_transforms(augment=True):
    """Get data transforms with optional augmentation."""
    if augment:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

def prepare_dataloaders(data_dir, batch_size=32, train_split=0.8, val_split=0.1):
    """Prepare train, validation, and test dataloaders."""
    train_transform = get_transforms(augment=True)
    test_transform = get_transforms(augment=False)
    
    full_dataset = datasets.ImageFolder(data_dir, transform=train_transform)
    
    total_size = len(full_dataset)
    train_size = int(train_split * total_size)
    val_size = int(val_split * total_size)
    test_size = total_size - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = random_split(
        full_dataset, [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(42)
    )
    
    val_dataset.dataset.transform = test_transform
    test_dataset.dataset.transform = test_transform
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    
    return train_loader, val_loader, test_loader, full_dataset.classes
