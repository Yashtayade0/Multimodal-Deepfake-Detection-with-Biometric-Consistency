# DeepGuard AI: Multimodal Deepfake Detection

![DeepGuard Banner](https://via.placeholder.com/1000x300/0a0f1c/22d3ee?text=DeepGuard+AI)

**DeepGuard** is a state-of-the-art, open-source AI platform designed to detect synthetically generated media (deepfakes). By leveraging a multi-modal approach — analyzing visual artifacts, audio signatures, and physiological behaviors (like blinking) — DeepGuard delivers high-confidence authenticity verdicts.

## Core Features

- 👁️ **Visual Analysis**: Utilizes **EfficientNet-B4** to analyze facial regions frame-by-frame, detecting pixel-level manipulation, blending artifacts, and spatial inconsistencies invisible to the naked eye.
- 🎙️ **Audio Analysis**: Uses **Librosa** for spectral decomposition and MFCC feature extraction to identify synthetic voice patterns, unnatural pitch shifts, and AI-generated vocal artifacts.
- 📈 **Blink Dynamics**: Leverages **MediaPipe** facial landmark tracking to map micro-expressions and measure eye blink rates over time. Deepfakes often struggle to replicate natural human blink behaviors.
- 🛡️ **Confidence Fusion Engine**: Aggregates signals from all active modalities and yields a final weighted *Authentic* or *Deepfake Detected* verdict.

## Tech Stack

- **Frontend**: React.js, Vite, Tailwind CSS, Lucide React (Dark Glassmorphism Design).
- **Backend**: Python, Flask, Flask-CORS, Werkzeug.
- **Machine Learning**: PyTorch (EfficientNet), scikit-learn, MediaPipe, Librosa, OpenCV, MTCNN.

## Project Structure

```text
DeepGuard/
├── backend/                     # Python Flask API & ML Pipelines
│   ├── app.py                   # Main routing and integration
│   ├── run.py                   # Dev server entrypoint
│   └── requirements.txt         # Minimum Python dependencies
├── deepfake-detector/           # React Web Application
│   └── deepfake-detector/
│       ├── src/                 # UI components and styling
│       └── package.json         # Node dependencies
├── SETUP_GUIDE.md               # Detailed installation & run instructions
└── README.md                    # This file
```

## 📦 Pre-trained Models

The ML model weights are hosted on HuggingFace Hub (too large for GitHub):

👉 **[yashtayade0908/deepguard-deepfake-detector](https://huggingface.co/yashtayade0908/deepguard-deepfake-detector)**

| Model File | Size | Description |
|---|---|---|
| `best_deepfake_detector.pth` | ~18 MB | EfficientNet visual detector |
| `best_deepfake_detector_cnn.pth` | ~65 MB | CNN deepfake detector |
| `fake_face_detector_pytorch.joblib` | ~12 MB | Sklearn ensemble model |

### Download models automatically:

```bash
pip install huggingface_hub

python -c "
from huggingface_hub import hf_hub_download
import os
dest = 'project1 (1)/project1/'
os.makedirs(dest, exist_ok=True)
for f in ['best_deepfake_detector.pth', 'best_deepfake_detector_cnn.pth', 'fake_face_detector_pytorch.joblib']:
    hf_hub_download(repo_id='yashtayade0908/deepguard-deepfake-detector', filename=f, local_dir=dest)
    print(f'Downloaded {f}')
print('All models downloaded!')
"
```

## Getting Started

Please see the [**SETUP_GUIDE.md**](./SETUP_GUIDE.md) for detailed, step-by-step instructions on installing dependencies, downloading the deep learning weights, and running the application locally.

## License & Privacy

This project is built for academic research and media authenticity purposes. Media analyzed through DeepGuard is processed locally or on your deployed server, and is **never permanently stored**, respecting data privacy.
