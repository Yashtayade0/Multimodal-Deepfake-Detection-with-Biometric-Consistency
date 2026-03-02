#!/usr/bin/env python3
"""
Test script to verify model loading and basic functionality
"""

import os
import sys
import cv2
import numpy as np
import torch
import joblib
from facenet_pytorch import MTCNN

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import DeepfakeDetector, preprocess_image, predict_with_pytorch, predict_with_sklearn, load_models

def test_model_loading():
    """Test if models can be loaded"""
    print("=" * 60)
    print("TESTING MODEL LOADING")
    print("=" * 60)
    
    # Test PyTorch model
    pytorch_path = '../project1 (1)/project1/best_deepfake_detector.pth'
    if os.path.exists(pytorch_path):
        print(f"[OK] PyTorch model found at: {pytorch_path}")
        try:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = DeepfakeDetector().to(device)
            model.load_state_dict(torch.load(pytorch_path, map_location=device))
            model.eval()
            print(f"[OK] PyTorch model loaded successfully on {device}")
        except Exception as e:
            print(f"[ERROR] PyTorch model loading failed: {e}")
    else:
        print(f"[ERROR] PyTorch model not found at: {pytorch_path}")
    
    # Test scikit-learn model
    sklearn_path = '../project1 (1)/project1/fake_face_detector_pytorch.joblib'
    if os.path.exists(sklearn_path):
        print(f"[OK] Scikit-learn model found at: {sklearn_path}")
        try:
            model = joblib.load(sklearn_path)
            print(f"[OK] Scikit-learn model loaded successfully")
            print(f"  Model type: {type(model).__name__}")
            if hasattr(model, 'n_features_in_'):
                print(f"  Expected features: {model.n_features_in_}")
            else:
                print("  Expected features: Unknown")
        except Exception as e:
            print(f"[ERROR] Scikit-learn model loading failed: {e}")
    else:
        print(f"[ERROR] Scikit-learn model not found at: {sklearn_path}")
    
    # Test MTCNN
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        detector = MTCNN(keep_all=False, device=device)
        print(f"[OK] MTCNN detector initialized on {device}")
    except Exception as e:
        print(f"[ERROR] MTCNN initialization failed: {e}")

def test_image_processing():
    """Test image processing functions"""
    print("\n" + "=" * 60)
    print("TESTING IMAGE PROCESSING")
    print("=" * 60)
    
    # Create a test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    print(f"[OK] Created test image: {test_image.shape}")
    
    # Test preprocessing
    try:
        processed = preprocess_image(test_image)
        print(f"[OK] Image preprocessing successful: {processed.shape}, dtype: {processed.dtype}")
    except Exception as e:
        print(f"[ERROR] Image preprocessing failed: {e}")
    
    # Test face detection
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        detector = MTCNN(keep_all=False, device=device)
        faces = detector.detect(test_image)
        print(f"[OK] Face detection successful: {len(faces[0]) if faces[0] is not None else 0} faces detected")
    except Exception as e:
        print(f"[ERROR] Face detection failed: {e}")

def test_predictions():
    """Test prediction functions"""
    print("\n" + "=" * 60)
    print("TESTING PREDICTIONS")
    print("=" * 60)
    
    # Load models first
    print("Loading models for prediction testing...")
    load_models()
    
    # Create a test face image
    test_face = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    print(f"[OK] Created test face: {test_face.shape}")
    
    # Test PyTorch prediction
    try:
        result = predict_with_pytorch(test_face)
        if result:
            print(f"[OK] PyTorch prediction successful: {result}")
        else:
            print("[ERROR] PyTorch prediction returned None")
    except Exception as e:
        print(f"[ERROR] PyTorch prediction failed: {e}")
    
    # Test sklearn prediction
    try:
        result = predict_with_sklearn(test_face)
        if result:
            print(f"[OK] Sklearn prediction successful: {result}")
        else:
            print("[ERROR] Sklearn prediction returned None")
    except Exception as e:
        print(f"[ERROR] Sklearn prediction failed: {e}")

if __name__ == '__main__':
    test_model_loading()
    test_image_processing()
    test_predictions()
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
