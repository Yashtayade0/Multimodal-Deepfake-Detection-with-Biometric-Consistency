"""
Configuration file for the Deepfake Detection API
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'deepfake-detection-secret-key-2024'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'wav', 'mp3'}
    
    # Model paths (relative to backend directory)
    PYTORCH_MODEL_PATH = '../project1 (1)/project1/best_deepfake_detector.pth'
    SKLEARN_MODEL_PATH = '../project1 (1)/project1/fake_face_detector_pytorch.joblib'
    CNN_MODEL_PATH = '../project1 (1)/project1/best_deepfake_detector_cnn.pth'
    
    # Model settings
    IMG_SIZE = (224, 224)
    MIN_IMG_SIZE = 32
    CONFIDENCE_THRESHOLD = 0.5
    
    # API settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
