#!/usr/bin/env python3
"""
Deepfake Detection API Server
Run this script to start the backend server
"""

import os
import sys
import logging
from app import app, load_models

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the server"""
    logger.info("=" * 60)
    logger.info("DEEPFAKE DETECTION API SERVER")
    logger.info("=" * 60)
    
    # Load models
    logger.info("Loading ML models...")
    load_models()
    
    # Check if models loaded successfully
    from app import pytorch_model, sklearn_model, mtcnn_detector
    
    if pytorch_model is None and sklearn_model is None:
        logger.error("No models loaded! Please check model paths.")
        sys.exit(1)
    
    logger.info("Models loaded successfully!")
    logger.info(f"PyTorch model: {'✓' if pytorch_model else '✗'}")
    logger.info(f"Scikit-learn model: {'✓' if sklearn_model else '✗'}")
    logger.info(f"MTCNN detector: {'✓' if mtcnn_detector else '✗'}")
    
    # Start server
    logger.info("Starting server on http://localhost:5000")
    logger.info("API endpoints:")
    logger.info("  GET  /api/health - Health check")
    logger.info("  POST /api/analyze - Analyze media file")
    logger.info("  GET  /api/models/status - Model status")
    logger.info("=" * 60)
    
    try:
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
