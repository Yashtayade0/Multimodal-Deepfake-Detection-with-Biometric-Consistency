#!/bin/bash
# HuggingFace Model Upload Script
# Run this script after connecting to mobile hotspot

echo "Step 1: Authenticating with HuggingFace..."
echo "Please enter your HuggingFace token when prompted"
hf auth login

echo ""
echo "Step 2: Creating model repository..."
hf repo create deepguard-deepfake-detector --repo-type model

echo ""
echo "Step 3: Uploading model files..."
cd "project1 (1)/project1"

echo "Uploading best_deepfake_detector.pth..."
hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector.pth best_deepfake_detector.pth

echo "Uploading best_deepfake_detector_cnn.pth..."
hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector_cnn.pth best_deepfake_detector_cnn.pth

echo "Uploading fake_face_detector_pytorch.joblib..."
hf upload yashtayade0908/deepguard-deepfake-detector fake_face_detector_pytorch.joblib fake_face_detector_pytorch.joblib

echo ""
echo "✓ Upload complete!"
echo "Your models are now available at: https://huggingface.co/yashtayade0908/deepguard-deepfake-detector"
