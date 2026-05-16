@echo off
REM HuggingFace Model Upload Script for Windows
REM Run this after connecting to mobile hotspot

echo ============================================================
echo DeepGuard - HuggingFace Model Upload
echo ============================================================
echo.

echo IMPORTANT: Make sure you are connected to mobile hotspot!
echo College network blocks HuggingFace uploads.
echo.
pause

echo.
echo Step 1: Authenticating with HuggingFace...
echo Please enter your HuggingFace token when prompted
echo Get token from: https://huggingface.co/settings/tokens
echo.
hf auth login

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Authentication failed!
    echo Please check your token and try again.
    pause
    exit /b 1
)

echo.
echo Step 2: Creating model repository...
hf repo create deepguard-deepfake-detector --repo-type model

echo.
echo Step 3: Uploading model files...
cd "project1 (1)\project1"

echo.
echo [1/3] Uploading best_deepfake_detector.pth...
hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector.pth best_deepfake_detector.pth

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to upload best_deepfake_detector.pth
    cd ..\..
    pause
    exit /b 1
)

echo.
echo [2/3] Uploading best_deepfake_detector_cnn.pth...
hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector_cnn.pth best_deepfake_detector_cnn.pth

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to upload best_deepfake_detector_cnn.pth
    cd ..\..
    pause
    exit /b 1
)

echo.
echo [3/3] Uploading fake_face_detector_pytorch.joblib...
hf upload yashtayade0908/deepguard-deepfake-detector fake_face_detector_pytorch.joblib fake_face_detector_pytorch.joblib

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to upload fake_face_detector_pytorch.joblib
    cd ..\..
    pause
    exit /b 1
)

cd ..\..

echo.
echo ============================================================
echo SUCCESS! Upload complete!
echo ============================================================
echo.
echo Your models are now available at:
echo https://huggingface.co/yashtayade0908/deepguard-deepfake-detector
echo.
echo You can verify the upload by running:
echo python verify_huggingface_upload.py
echo.
pause
