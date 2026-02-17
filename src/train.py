import os
import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from src.data_preprocessing import prepare_dataloaders
from src.model import get_model

def train_epoch(model, loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    return running_loss / len(loader), 100. * correct / total

def validate(model, loader, criterion, device):
    """Validate the model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return running_loss / len(loader), 100. * correct / total, all_preds, all_labels

def plot_confusion_matrix(y_true, y_pred, classes):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]), yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           ylabel='True label', xlabel='Predicted label')
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > cm.max() / 2. else "black")
    fig.tight_layout()
    return fig

def train_model(data_dir='data/processed', epochs=10, batch_size=32, lr=0.001):
    """Main training function with MLflow tracking."""
    
    mlflow.set_experiment("cats-dogs-classification")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("learning_rate", lr)
        
        # Setup
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        # Data
        train_loader, val_loader, test_loader, classes = prepare_dataloaders(
            data_dir, batch_size=batch_size
        )
        mlflow.log_param("num_classes", len(classes))
        
        # Model
        model = get_model(num_classes=len(classes)).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        
        # Training loop
        best_val_acc = 0.0
        train_losses, val_losses = [], []
        
        for epoch in range(epochs):
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            val_loss, val_acc, _, _ = validate(model, val_loader, criterion, device)
            
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            
            print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), "models/best_model.pth")
        
        # Test evaluation
        model.load_state_dict(torch.load("models/best_model.pth"))
        test_loss, test_acc, test_preds, test_labels = validate(model, test_loader, criterion, device)
        
        print(f"\nTest Accuracy: {test_acc:.2f}%")
        mlflow.log_metric("test_accuracy", test_acc)
        
        # Confusion matrix
        cm_fig = plot_confusion_matrix(test_labels, test_preds, classes)
        mlflow.log_figure(cm_fig, "confusion_matrix.png")
        plt.close()
        
        # Loss curves
        fig, ax = plt.subplots()
        ax.plot(train_losses, label='Train Loss')
        ax.plot(val_losses, label='Val Loss')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.legend()
        mlflow.log_figure(fig, "loss_curves.png")
        plt.close()
        
        # Save model
        mlflow.pytorch.log_model(model, "model")
        torch.save(model.state_dict(), "models/model.pth")
        
        # Save class names
        with open("models/classes.txt", "w") as f:
            f.write("\n".join(classes))
        mlflow.log_artifact("models/classes.txt")
        
        print(f"\nModel saved to models/model.pth")
        print(f"Best validation accuracy: {best_val_acc:.2f}%")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    train_model(data_dir="data/processed", epochs=10, batch_size=32, lr=0.001)
