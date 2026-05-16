---
license: mit
tags:
- deepfake-detection
- computer-vision
- pytorch
- efficientnet
- video-analysis
- audio-analysis
library_name: pytorch
---

# DeepGuard: Multimodal Deepfake Detector

Pre-trained models for the **DeepGuard AI** multimodal deepfake detection system.

## 🎯 Model Description

DeepGuard uses a multi-modal approach to detect synthetically generated media (deepfakes) by analyzing:
- **Visual artifacts** using EfficientNet-B4
- **Audio signatures** using spectral analysis
- **Physiological behaviors** like blink dynamics

## 📦 Model Files

| File | Size | Description |
|------|------|-------------|
| `best_deepfake_detector.pth` | ~18 MB | EfficientNet-B4 visual detector |
| `best_deepfake_detector_cnn.pth` | ~65 MB | CNN deepfake detector |
| `fake_face_detector_pytorch.joblib` | ~12 MB | Sklearn ensemble model |

## 🚀 Usage

### Download Models

```python
from huggingface_hub import hf_hub_download

# Download a specific model
model_path = hf_hub_download(
    repo_id="yashtayade0908/deepguard-deepfake-detector",
    filename="best_deepfake_detector.pth"
)

# Or download all models
import os
dest = './models/'
os.makedirs(dest, exist_ok=True)

for filename in ['best_deepfake_detector.pth', 
                 'best_deepfake_detector_cnn.pth', 
                 'fake_face_detector_pytorch.joblib']:
    hf_hub_download(
        repo_id="yashtayade0908/deepguard-deepfake-detector",
        filename=filename,
        local_dir=dest
    )
```

### Load Model in PyTorch

```python
import torch

# Load the model
model = torch.load('best_deepfake_detector.pth')
model.eval()

# Use for inference
# (See full project repository for complete usage)
```

## 🛠️ Tech Stack

- **PyTorch** - Deep learning framework
- **EfficientNet-B4** - Visual feature extraction
- **scikit-learn** - Ensemble methods
- **MediaPipe** - Facial landmark detection
- **Librosa** - Audio analysis

## 📊 Performance

The models are trained on a large dataset of real and synthetic faces, achieving high accuracy in detecting various types of deepfakes including:
- Face swaps
- Face reenactment
- Synthetic face generation
- Audio deepfakes

## 🔗 Project Repository

**Full source code and documentation:**
- GitHub: [Multimodal-Deepfake-Detection-with-Biometric-Consistency](https://github.com/Yashtayade0/Multimodal-Deepfake-Detection-with-Biometric-Consistency)

**Features:**
- React web interface
- Flask REST API
- Real-time video analysis
- Audio deepfake detection
- Blink pattern analysis

## 📝 Citation

If you use these models in your research, please cite:

```bibtex
@misc{deepguard2024,
  author = {Yash Tayade},
  title = {DeepGuard: Multimodal Deepfake Detection},
  year = {2024},
  publisher = {HuggingFace},
  howpublished = {\url{https://huggingface.co/yashtayade0908/deepguard-deepfake-detector}}
}
```

## 📄 License

MIT License - See repository for full license text.

## 🤝 Contributing

Contributions are welcome! Please see the main repository for contribution guidelines.

## ⚠️ Ethical Use

These models are intended for:
- Academic research
- Media authenticity verification
- Educational purposes

Please use responsibly and respect privacy and consent when analyzing media.
