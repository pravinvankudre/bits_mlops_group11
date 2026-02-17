"""
All-in-one setup script: Download dataset, prepare data, and create model.
"""

import sys
import subprocess

def run_step(name, script):
    """Run a setup step."""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print('='*60)
    try:
        subprocess.run([sys.executable, script], check=True)
        print(f"✓ {name} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {name} failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  MLOps Assignment 2 - Automated Setup")
    print("="*60)
    
    steps = [
        ("Download Dataset", "download_dataset.py"),
        ("Prepare Data", "prepare_data.py"),
        ("Create Model", "create_dummy_model.py"),
    ]
    
    for name, script in steps:
        if not run_step(name, script):
            print(f"\n✗ Setup failed at: {name}")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("  ✓ Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Train model: python src/train.py")
    print("  2. Run tests: pytest tests/ -v")
    print("  3. Build Docker: docker build -t cats-dogs-classifier:latest .")
    print("\n")

if __name__ == "__main__":
    main()
