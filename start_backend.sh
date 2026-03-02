#!/bin/bash

echo "========================================"
echo "Deepfake Detection API Backend"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Check if model files exist
echo "Checking model files..."
if [ ! -f "../project1 (1)/project1/best_deepfake_detector.pth" ]; then
    echo "Warning: PyTorch model not found"
    echo "Expected: ../project1 (1)/project1/best_deepfake_detector.pth"
fi

if [ ! -f "../project1 (1)/project1/fake_face_detector_pytorch.joblib" ]; then
    echo "Warning: Scikit-learn model not found"
    echo "Expected: ../project1 (1)/project1/fake_face_detector_pytorch.joblib"
fi

echo
echo "Starting Deepfake Detection API Server..."
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python run.py
