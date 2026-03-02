@echo off
echo ========================================
echo Deepfake Detection API Backend
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if model files exist
echo Checking model files...
if not exist "..\project1 (1)\project1\best_deepfake_detector.pth" (
    echo Warning: PyTorch model not found
    echo Expected: ..\project1 (1)\project1\best_deepfake_detector.pth
)

if not exist "..\project1 (1)\project1\fake_face_detector_pytorch.joblib" (
    echo Warning: Scikit-learn model not found
    echo Expected: ..\project1 (1)\project1\fake_face_detector_pytorch.joblib
)

echo.
echo Starting Deepfake Detection API Server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python run.py

pause
