# Deepfake Detection API Backend

This is the backend API server for the Deepfake Detection application. It provides RESTful endpoints to analyze images and videos for deepfake detection using machine learning models.

## Features

- **Multi-Model Support**: Uses both PyTorch and scikit-learn models for robust detection
- **Face Detection**: Automatic face detection using MTCNN
- **Image & Video Analysis**: Supports common image and video formats
- **Real-time Processing**: Fast analysis with progress tracking
- **RESTful API**: Clean API endpoints for frontend integration

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster processing)
- At least 4GB RAM
- 2GB free disk space

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify model files exist:**
   Make sure the following model files are present in the `../project1 (1)/project1/` directory:
   - `best_deepfake_detector.pth` (PyTorch model)
   - `fake_face_detector_pytorch.joblib` (scikit-learn model)

## Running the Server

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and model loading information.

### Analyze Media
```
POST /api/analyze
```
Upload and analyze an image or video file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image or video)

**Response:**
```json
{
  "overall": {
    "verdict": "DEEPFAKE DETECTED",
    "confidence": 87.3,
    "authentic": false
  },
  "visual": {
    "score": 72.5,
    "status": "suspicious",
    "artifacts": ["Inconsistent lighting", "Facial warping"],
    "timeline": [45, 62, 78, 72, 69]
  },
  "audio": {
    "score": 91.2,
    "status": "fake",
    "features": ["Synthetic timbre", "Abnormal shimmer"],
    "timeline": [88, 92, 89, 95, 91]
  },
  "physiological": {
    "score": 98.1,
    "status": "fake",
    "metrics": ["Irregular blink rate", "Missing micro-movements"],
    "timeline": [95, 98, 97, 99, 98]
  },
  "consistency": {
    "visualAudio": 0.68,
    "visualBlink": 0.45,
    "audioBlink": 0.52,
    "threshold": 0.75
  }
}
```

### Model Status
```
GET /api/models/status
```
Returns the status of loaded ML models.

## Supported File Formats

### Images
- PNG
- JPG/JPEG

### Videos
- MP4
- AVI
- MOV

### Audio (Future Support)
- WAV
- MP3

## Configuration

Edit `config.py` to modify:
- File upload limits
- Model paths
- API settings
- Logging configuration

## Troubleshooting

### Common Issues

1. **Models not loading:**
   - Check if model files exist in the correct path
   - Verify file permissions
   - Check console logs for specific error messages

2. **CUDA errors:**
   - Install CUDA-compatible PyTorch version
   - Or run on CPU (slower but functional)

3. **Memory issues:**
   - Reduce batch size in processing
   - Use smaller input images
   - Close other applications

4. **File upload errors:**
   - Check file size (max 500MB)
   - Verify file format is supported
   - Ensure stable internet connection

### Logs

Check the console output for detailed error messages and processing information.

## Performance Tips

1. **GPU Acceleration:**
   - Install CUDA toolkit
   - Use GPU-compatible PyTorch
   - Ensure sufficient GPU memory

2. **Optimization:**
   - Use smaller input images for faster processing
   - Limit video frame sampling
   - Enable model caching

## Security Notes

- The API runs on all interfaces (0.0.0.0) by default
- For production, configure proper authentication
- Implement rate limiting for public deployments
- Validate all uploaded files

## Development

### Adding New Models

1. Add model loading logic in `load_models()`
2. Implement prediction function
3. Update API response format
4. Add model status endpoint

### Extending Analysis

1. Add new analysis functions
2. Update the main analysis pipeline
3. Modify response format
4. Update frontend integration

## License

This project is part of the Deepfake Detection system. See the main project for license information.
