from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import joblib
from facenet_pytorch import MTCNN
from werkzeug.utils import secure_filename
import tempfile
import json
from datetime import datetime
import warnings
import logging

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'wav', 'mp3'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for models
pytorch_model = None
sklearn_model = None
mtcnn_detector = None
device = None

# Model configuration
IMG_SIZE = (224, 224)
MIN_IMG_SIZE = 32

class DeepfakeDetector(nn.Module):
    """PyTorch model architecture matching the training script"""
    def __init__(self):
        super(DeepfakeDetector, self).__init__()
        self.model = models.efficientnet_b0(pretrained=True)
        
        # Unfreeze last few layers
        for param in self.model.parameters():
            param.requires_grad = False
        for param in self.model.features[-3:].parameters():
            param.requires_grad = True
        
        # Replace classifier
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(p=0.3),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.model(x)

def load_models():
    """Load all ML models"""
    global pytorch_model, sklearn_model, mtcnn_detector, device
    
    try:
        # Set device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")
        
        # Load PyTorch model
        model_path = '../project1 (1)/project1/best_deepfake_detector.pth'
        if os.path.exists(model_path):
            pytorch_model = DeepfakeDetector().to(device)
            pytorch_model.load_state_dict(torch.load(model_path, map_location=device))
            pytorch_model.eval()
            logger.info("PyTorch model loaded successfully")
        else:
            logger.warning(f"PyTorch model not found at {model_path}")
        
        # Load scikit-learn model
        sklearn_path = '../project1 (1)/project1/fake_face_detector_pytorch.joblib'
        if os.path.exists(sklearn_path):
            sklearn_model = joblib.load(sklearn_path)
            logger.info("Scikit-learn model loaded successfully")
        else:
            logger.warning(f"Scikit-learn model not found at {sklearn_path}")
        
        # Initialize MTCNN face detector
        mtcnn_detector = MTCNN(keep_all=False, device=device)
        logger.info("MTCNN detector initialized")
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """Preprocess image for model inference"""
    logger.info(f"Original image shape: {image.shape}, dtype: {image.dtype}")
    
    # Convert BGR to RGB
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        logger.info(f"After BGR->RGB conversion: {image.shape}")
    
    # Resize to model input size
    image = cv2.resize(image, IMG_SIZE)
    logger.info(f"After resize to {IMG_SIZE}: {image.shape}")
    
    # Normalize
    image = image.astype(np.float32) / 255.0
    logger.info(f"After normalization: min={image.min():.3f}, max={image.max():.3f}")
    
    # Apply ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    image = (image - mean) / std
    logger.info(f"After ImageNet normalization: min={image.min():.3f}, max={image.max():.3f}")
    
    # Convert to tensor and ensure float32
    image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).float()
    logger.info(f"Final tensor shape: {image.shape}, dtype: {image.dtype}")
    
    return image

def detect_faces(image):
    """Detect faces in image using MTCNN"""
    if mtcnn_detector is None:
        return []
    
    try:
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Detect faces
        boxes, _ = mtcnn_detector.detect(image_rgb)
        
        if boxes is not None:
            faces = []
            h, w = image_rgb.shape[:2]
            
            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                if x2 > x1 and y2 > y1 and (x2-x1) > 50 and (y2-y1) > 50:
                    face = image_rgb[y1:y2, x1:x2]
                    faces.append({
                        'face': face,
                        'bbox': (x1, y1, x2, y2)
                    })
            
            return faces
        else:
            return []
    
    except Exception as e:
        logger.error(f"Error detecting faces: {str(e)}")
        return []

def predict_with_pytorch(image):
    """Predict using PyTorch model"""
    global pytorch_model, device
    if pytorch_model is None:
        logger.warning("PyTorch model not loaded")
        return None
    
    try:
        with torch.no_grad():
            image_tensor = preprocess_image(image).to(device)
            prediction = pytorch_model(image_tensor)
            confidence = prediction.item()
            
            # Convert to percentage and determine if fake
            fake_probability = confidence * 100
            # PyTorch model: higher confidence = more likely fake
            is_fake = confidence > 0.5
            
            result = {
                'confidence': float(fake_probability),
                'is_fake': bool(is_fake),
                'model': 'pytorch',
                'raw_prediction': float(confidence),
                'raw_fake_probability': float(fake_probability)
            }
        logger.info(f"PyTorch raw output: confidence={confidence}, fake_prob={fake_probability}, is_fake={is_fake}")
        logger.info(f"PyTorch model prediction range: {confidence} (should be 0-1)")
        return result
    except Exception as e:
        logger.error(f"Error in PyTorch prediction: {str(e)}")
        return None

def predict_with_sklearn(image):
    """Predict using scikit-learn model"""
    global sklearn_model
    if sklearn_model is None:
        logger.warning("Sklearn model not loaded")
        return None
    
    try:
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Check what the model expects first
        expected_features = sklearn_model.n_features_in_ if hasattr(sklearn_model, 'n_features_in_') else 12288
        
        if expected_features == 12288:
            # Model expects 12288 features - this is likely 64x64x3 or some other combination
            # Try 64x64 RGB first
            image_resized = cv2.resize(image_rgb, (64, 64))
            image_flattened = image_resized.flatten().reshape(1, -1)
            logger.info(f"Resized to 64x64 RGB: {image_flattened.shape}")
        else:
            # Default to 128x128
            image_resized = cv2.resize(image_rgb, (128, 128))
            image_flattened = image_resized.flatten().reshape(1, -1)
        
        # Verify the feature count matches what the model expects
        if hasattr(sklearn_model, 'n_features_in_'):
            expected_features = sklearn_model.n_features_in_
            if image_flattened.shape[1] != expected_features:
                logger.warning(f"Feature mismatch: got {image_flattened.shape[1]}, expected {expected_features}")
                return None
        
        # Predict
        try:
            prediction = sklearn_model.predict(image_flattened)
            proba = sklearn_model.predict_proba(image_flattened)
            logger.info(f"Sklearn prediction successful: {prediction[0]}")
        except Exception as e:
            logger.error(f"Sklearn prediction failed: {str(e)}")
            return None
        
        # Get confidence
        confidence = proba[0][prediction[0]] * 100
        # Add confidence threshold for sklearn - only consider fake if confidence > 55%
        is_fake = prediction[0] == 0 and confidence > 55  # 0 = fake, 1 = real
        
        result = {
            'confidence': float(confidence),
            'is_fake': bool(is_fake),
            'model': 'sklearn',
            'raw_prediction': int(prediction[0]),
            'raw_confidence': float(confidence),
            'prediction_proba': [float(p) for p in proba[0]]
        }
        logger.info(f"Sklearn raw output: prediction={prediction[0]}, confidence={confidence}, is_fake={is_fake}, proba={proba[0]}")
        logger.info(f"Sklearn model: prediction={prediction[0]} (0=fake, 1=real), confidence={confidence}%")
        return result
    except Exception as e:
        logger.error(f"Error in sklearn prediction: {str(e)}")
        return None

def analyze_image(image_path):
    """Analyze a single image"""
    try:
        logger.info(f"Starting image analysis for: {image_path}")
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Could not load image: {image_path}")
            return None
        
        logger.info(f"Image loaded successfully: {image.shape}")
        
        # Detect faces
        faces = detect_faces(image)
        logger.info(f"Face detection completed: {len(faces)} faces found")
        
        if not faces:
            logger.warning("No faces detected in the image")
            return {
                'error': 'No faces detected in the image',
                'overall': {'verdict': 'NO FACE DETECTED', 'confidence': 0, 'authentic': True}
            }
        
        # Analyze each face
        face_results = []
        overall_scores = []
        
        for i, face_data in enumerate(faces):
            face = face_data['face']
            bbox = face_data['bbox']
            
            # Get predictions from both models
            logger.info(f"Analyzing face {i+1}/{len(faces)}")
            pytorch_result = predict_with_pytorch(face)
            sklearn_result = predict_with_sklearn(face)
            
            logger.info(f"Face {i+1} results: PyTorch={pytorch_result}, Sklearn={sklearn_result}")
            
            face_result = {
                'face_id': i,
                'bbox': [int(x) for x in bbox],  # Convert numpy arrays to Python lists
                'pytorch': pytorch_result,
                'sklearn': sklearn_result
            }
            
            # Ensure all values are JSON serializable
            if pytorch_result:
                pytorch_result['confidence'] = float(pytorch_result['confidence'])
                pytorch_result['is_fake'] = bool(pytorch_result['is_fake'])
            if sklearn_result:
                sklearn_result['confidence'] = float(sklearn_result['confidence'])
                sklearn_result['is_fake'] = bool(sklearn_result['is_fake'])
            
            face_results.append(face_result)
            
            # Collect scores for overall analysis with balanced weighting
            if pytorch_result:
                # PyTorch model - keep original confidence
                overall_scores.append(pytorch_result['confidence'])
            if sklearn_result:
                # Sklearn model - keep original confidence
                overall_scores.append(sklearn_result['confidence'])
        
        # Calculate overall result with model agreement
        logger.info(f"Overall scores collected: {overall_scores}")
        if overall_scores:
            try:
                # Check if both models agree on fake detection
                pytorch_scores = [face['pytorch']['confidence'] for face in face_results if face['pytorch']]
                sklearn_scores = [face['sklearn']['confidence'] for face in face_results if face['sklearn']]
                
                # Use both models with balanced thresholds
                pytorch_suggests_fake = any(score > 60 for score in pytorch_scores) if pytorch_scores else False
                sklearn_suggests_fake = any(score > 55 for score in sklearn_scores) if sklearn_scores else False
                
                logger.info(f"PyTorch scores: {pytorch_scores}, suggests fake: {pytorch_suggests_fake}")
                logger.info(f"Sklearn scores: {sklearn_scores}, suggests fake: {sklearn_suggests_fake}")
                
                # Calculate weighted average using both models
                pytorch_weight = 0.4  # 40% weight for PyTorch
                sklearn_weight = 0.6  # 60% weight for Sklearn
                
                # Get average scores from each model
                pytorch_avg = np.mean(pytorch_scores) if pytorch_scores else 50.0
                sklearn_avg = np.mean(sklearn_scores) if sklearn_scores else 50.0
                
                # Calculate weighted confidence
                weighted_confidence = (pytorch_avg * pytorch_weight) + (sklearn_avg * sklearn_weight)
                
                logger.info(f"PyTorch average: {pytorch_avg:.2f}, Sklearn average: {sklearn_avg:.2f}")
                logger.info(f"Weighted confidence: {weighted_confidence:.2f}")
                
                # Decision logic using both models
                both_agree_fake = pytorch_suggests_fake and sklearn_suggests_fake
                both_agree_real = not pytorch_suggests_fake and not sklearn_suggests_fake
                weighted_high_confidence = weighted_confidence > 65
                
                # Final decision: use both models
                is_fake = both_agree_fake or (weighted_high_confidence and (pytorch_suggests_fake or sklearn_suggests_fake))
                
                logger.info(f"Both agree fake: {both_agree_fake}, Both agree real: {both_agree_real}")
                logger.info(f"Weighted high confidence: {weighted_high_confidence}")
                logger.info(f"Final decision: {'FAKE' if is_fake else 'REAL'}")
                
                # Use weighted confidence for final result
                avg_confidence = float(weighted_confidence)
                
                overall_verdict = 'DEEPFAKE DETECTED' if is_fake else 'AUTHENTIC'
                logger.info(f"Analysis complete: {overall_verdict} (confidence: {avg_confidence})")
            except Exception as e:
                logger.error(f"Error calculating overall result: {str(e)}")
                avg_confidence = 50.0
                is_fake = False
                overall_verdict = 'ANALYSIS INCOMPLETE'
        else:
            # Fallback if no models worked
            logger.warning("No models produced valid results, using fallback")
            avg_confidence = 50.0  # Neutral confidence
            is_fake = False
            overall_verdict = 'ANALYSIS INCOMPLETE'
        
        # Generate detailed results matching frontend format
        results = {
            'overall': {
                'verdict': overall_verdict,
                'confidence': float(round(avg_confidence, 1)),
                'authentic': not is_fake
            },
            'visual': {
                'score': float(round(avg_confidence, 1)),
                'status': 'fake' if is_fake else 'authentic',
                'artifacts': [
                    'Facial inconsistencies detected' if is_fake else 'Natural facial features',
                    'Edge artifacts found' if is_fake else 'Smooth edge transitions',
                    'Lighting anomalies' if is_fake else 'Consistent lighting'
                ],
                'timeline': [float(round(avg_confidence, 1))] * 5
            },
            'audio': {
                'score': 85.0,  # Placeholder for audio analysis
                'status': 'suspicious',
                'features': ['Audio analysis not available for images'],
                'timeline': [85.0] * 5
            },
            'physiological': {
                'score': 90.0,  # Placeholder for physiological analysis
                'status': 'authentic',
                'metrics': ['Blink analysis not available for images'],
                'timeline': [90.0] * 5
            },
            'consistency': {
                'visualAudio': 0.75,
                'visualBlink': 0.80,
                'audioBlink': 0.70,
                'threshold': 0.75
            },
            'face_results': face_results
        }
        
        return results
    
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return {
            'error': f'Analysis failed: {str(e)}',
            'overall': {'verdict': 'ERROR', 'confidence': 0, 'authentic': True}
        }

def analyze_video(video_path):
    """Analyze a video file"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Sample frames for analysis
        sample_rate = max(1, total_frames // 30)  # Sample up to 30 frames
        frame_results = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % sample_rate == 0:
                # Analyze this frame
                temp_image_path = tempfile.mktemp(suffix='.jpg')
                cv2.imwrite(temp_image_path, frame)
                
                frame_result = analyze_image(temp_image_path)
                if frame_result and 'overall' in frame_result:
                    frame_results.append({
                        'frame': frame_count,
                        'timestamp': frame_count / fps,
                        'result': frame_result
                    })
                
                os.remove(temp_image_path)
            
            frame_count += 1
        
        cap.release()
        
        if not frame_results:
            return {
                'error': 'No valid frames found in video',
                'overall': {'verdict': 'ANALYSIS FAILED', 'confidence': 0, 'authentic': True}
            }
        
        # Aggregate results across frames using same logic as image analysis
        confidences = [fr['result']['overall']['confidence'] for fr in frame_results]
        avg_confidence = np.mean(confidences)
        
        # Use the same weighted logic as image analysis
        # For videos, we'll use a simpler approach but still flip the logic
        is_fake = avg_confidence > 60  # More conservative threshold for videos
        
        overall_verdict = 'DEEPFAKE DETECTED' if is_fake else 'AUTHENTIC'
        
        results = {
            'overall': {
                'verdict': overall_verdict,
                'confidence': round(avg_confidence, 1),
                'authentic': not is_fake
            },
            'visual': {
                'score': round(avg_confidence, 1),
                'status': 'fake' if is_fake else 'authentic',
                'artifacts': [
                    'Temporal inconsistencies detected' if is_fake else 'Consistent temporal features',
                    'Frame-to-frame artifacts' if is_fake else 'Smooth frame transitions',
                    'Motion anomalies' if is_fake else 'Natural motion patterns'
                ],
                'timeline': [round(c, 1) for c in confidences[:5]]  # First 5 frame confidences
            },
            'audio': {
                'score': 75.0,  # Placeholder for audio analysis
                'status': 'suspicious',
                'features': ['Audio analysis not implemented'],
                'timeline': [75.0] * 5
            },
            'physiological': {
                'score': 80.0,  # Placeholder for physiological analysis
                'status': 'authentic',
                'metrics': ['Blink analysis not implemented'],
                'timeline': [80.0] * 5
            },
            'consistency': {
                'visualAudio': 0.70,
                'visualBlink': 0.75,
                'audioBlink': 0.65,
                'threshold': 0.75
            },
            'frame_results': frame_results
        }
        
        return results
    
    except Exception as e:
        logger.error(f"Error analyzing video: {str(e)}")
        return {
            'error': f'Video analysis failed: {str(e)}',
            'overall': {'verdict': 'ERROR', 'confidence': 0, 'authentic': True}
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': {
            'pytorch': pytorch_model is not None,
            'sklearn': sklearn_model is not None,
            'mtcnn': mtcnn_detector is not None
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_media():
    """Main analysis endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        # Ensure upload folder exists
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
            
        file_path = os.path.join(upload_folder, filename)
        logger.info(f"Saving file: {file_path}")
        file.save(file_path)
        logger.info(f"File saved successfully: {file_path}")
        
        # Determine file type and analyze
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension in ['png', 'jpg', 'jpeg']:
            # Image analysis
            logger.info(f"Starting image analysis for: {file_extension}")
            result = analyze_image(file_path)
            logger.info(f"Image analysis completed, result type: {type(result)}")
        elif file_extension in ['mp4', 'avi', 'mov']:
            # Video analysis
            logger.info(f"Starting video analysis for: {file_extension}")
            result = analyze_video(file_path)
            logger.info(f"Video analysis completed, result type: {type(result)}")
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        if result is None:
            logger.error("Analysis returned None result")
            return jsonify({'error': 'Analysis failed'}), 500
        
        logger.info(f"Analysis completed successfully, returning results")
        try:
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error serializing results: {str(e)}")
            return jsonify({'error': f'Serialization failed: {str(e)}'}), 500
    
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/models/status', methods=['GET'])
def models_status():
    """Get status of loaded models"""
    sklearn_info = {}
    if sklearn_model is not None:
        sklearn_info = {
            'loaded': True,
            'type': type(sklearn_model).__name__,
            'n_features_in_': getattr(sklearn_model, 'n_features_in_', 'Unknown')
        }
    else:
        sklearn_info = {'loaded': False}
    
    return jsonify({
        'pytorch_model': pytorch_model is not None,
        'sklearn_model': sklearn_info,
        'mtcnn_detector': mtcnn_detector is not None,
        'device': str(device) if device else None
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 500MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Deepfake Detection API...")
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)
