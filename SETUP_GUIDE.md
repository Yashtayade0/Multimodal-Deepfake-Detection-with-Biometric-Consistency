# Deepfake Detection System - Setup Guide

This guide will help you set up and run the complete Deepfake Detection system with both frontend and backend components.

## System Overview

The system consists of:
- **Frontend**: React-based web application (`deepfake-detector/`)
- **Backend**: Flask API server (`backend/`)
- **ML Models**: Trained deepfake detection models (`project1 (1)/project1/`)

## Prerequisites

### Required Software
- **Python 3.8+** (for backend and ML models)
- **Node.js 16+** (for frontend)
- **npm** or **yarn** (package manager)
- **Git** (optional, for version control)

### Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space
- **GPU**: Optional but recommended for faster processing (CUDA-compatible)

## Quick Start

### 1. Backend Setup

#### Windows:
```bash
# Run the automated setup script
start_backend.bat
```

#### Linux/Mac:
```bash
# Make script executable and run
chmod +x start_backend.sh
./start_backend.sh
```

#### Manual Setup:
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python run.py
```

### 2. Frontend Setup

```bash
cd deepfake-detector/deepfake-detector
npm install
npm start
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## Detailed Setup Instructions

### Backend Configuration

1. **Model Files**: Ensure these files exist in `project1 (1)/project1/`:
   - `best_deepfake_detector.pth` (PyTorch model)
   - `fake_face_detector_pytorch.joblib` (scikit-learn model)

2. **Environment Variables** (optional):
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=True
   ```

3. **GPU Support** (optional):
   ```bash
   # Install CUDA-compatible PyTorch
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Frontend Configuration

1. **API Endpoint**: The frontend is configured to connect to `http://localhost:5000`
2. **File Upload**: Supports images (PNG, JPG) and videos (MP4, AVI, MOV)
3. **File Size Limit**: Maximum 500MB per file

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and model information.

### Analyze Media
```
POST /api/analyze
Content-Type: multipart/form-data
Body: file (image or video)
```

### Model Status
```
GET /api/models/status
```
Returns loaded model status.

## Troubleshooting

### Common Issues

#### 1. Backend Won't Start
- **Check Python version**: `python --version` (should be 3.8+)
- **Check dependencies**: `pip list` to verify all packages installed
- **Check model files**: Ensure model files exist in correct location
- **Check ports**: Ensure port 5000 is not in use

#### 2. Models Not Loading
- Verify model file paths in `backend/app.py`
- Check file permissions
- Ensure sufficient memory (4GB+ recommended)

#### 3. Frontend Connection Issues
- Verify backend is running on port 5000
- Check browser console for CORS errors
- Ensure both frontend and backend are running

#### 4. File Upload Errors
- Check file size (max 500MB)
- Verify file format is supported
- Check backend logs for specific errors

#### 5. Performance Issues
- Use GPU acceleration if available
- Reduce file size for faster processing
- Close other applications to free memory

### Logs and Debugging

#### Backend Logs
- Check console output when running `python run.py`
- Logs include model loading status and processing information

#### Frontend Logs
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request/response details

## Development

### Adding New Features

#### Backend
1. Add new endpoints in `app.py`
2. Implement analysis functions
3. Update response format
4. Test with frontend integration

#### Frontend
1. Add new components in `src/components/`
2. Update API calls in `App.jsx`
3. Modify UI to display new features
4. Test with backend integration

### Model Integration

To add new ML models:
1. Place model files in appropriate directory
2. Update `load_models()` function in `app.py`
3. Implement prediction function
4. Update API response format
5. Test with sample data

## Production Deployment

### Backend
```bash
# Use Gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
# Build for production
npm run build

# Serve with a web server (nginx, Apache, etc.)
```

### Security Considerations
- Configure proper CORS settings
- Implement authentication if needed
- Use HTTPS in production
- Validate all uploaded files
- Implement rate limiting

## Support

### Getting Help
1. Check this setup guide first
2. Review error logs and console output
3. Verify all prerequisites are met
4. Test with sample files

### File Structure
```
Proto/
├── backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Startup script
├── deepfake-detector/      # React frontend
│   └── deepfake-detector/
│       ├── src/
│       └── package.json
├── project1 (1)/           # ML models and training
│   └── project1/
│       ├── best_deepfake_detector.pth
│       ├── fake_face_detector_pytorch.joblib
│       └── ...
├── start_backend.bat       # Windows startup script
├── start_backend.sh        # Linux/Mac startup script
└── SETUP_GUIDE.md         # This file
```

## License

This project is part of the Deepfake Detection system. Please refer to the main project documentation for license information.
