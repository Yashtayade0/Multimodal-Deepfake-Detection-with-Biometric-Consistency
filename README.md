<div align="center">

# 🛡️ DeepGuard AI

### Multimodal Deepfake Detection with Biometric Consistency

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Models-FFD21E?style=for-the-badge)](https://huggingface.co/yashtayade0908/deepguard-deepfake-detector)
[![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)](#license--ethics)

> **DeepGuard AI** is a state-of-the-art, open-source platform that detects synthetically generated media (deepfakes) by fusing visual, audio, and biometric signals into a single high-confidence verdict.

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pre-trained Models](#-pre-trained-models)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [License & Ethics](#-license--ethics)

---

## 🧠 Overview

The rapid advancement of generative AI has made it trivially easy to fabricate convincing videos of real people saying or doing things they never did. **DeepGuard AI** combats this threat by analyzing media through **three independent lenses simultaneously**:

1. **Visual artifacts** — frame-level CNN analysis for pixel manipulation
2. **Audio signatures** — spectral decomposition for synthetic voice detection
3. **Biometric consistency** — facial landmark tracking to catch unnatural blink patterns

These signals are then fused by a **Confidence Fusion Engine** that produces a final weighted verdict: `✅ Authentic` or `🚨 Deepfake Detected`.

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                       Input Media                           │
│                  (Video / Image / Audio)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
  ┌─────────┐ ┌─────────┐ ┌──────────────┐
  │ Visual  │ │ Audio   │ │  Blink /     │
  │Analyzer │ │Analyzer │ │  Biometric   │
  │EfficientNet│Librosa │ │  Analyzer    │
  │+ MTCNN  │ │+ MFCC   │ │  MediaPipe   │
  └────┬────┘ └────┬────┘ └──────┬───────┘
       │           │             │
       └─────────┬─┘─────────────┘
                 ▼
     ┌───────────────────────┐
     │  Confidence Fusion    │
     │       Engine          │
     │  (Weighted Aggregation)│
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  Final Verdict +      │
     │  Confidence Score     │
     └───────────────────────┘
```

Each analyzer runs independently and returns its own confidence score. The Fusion Engine weighs these scores based on which modalities are available and relevant for the input type.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 👁️ **Visual Analysis** | EfficientNet-B4 + MTCNN scan facial regions frame-by-frame for blending artifacts, spatial inconsistencies, and pixel-level manipulation |
| 🎙️ **Audio Analysis** | Librosa spectral decomposition and MFCC feature extraction to identify synthetic voice patterns and unnatural pitch variations |
| 📈 **Blink Dynamics** | MediaPipe facial landmark tracking measures micro-expressions and blink rates — behaviors that AI generation still struggles to replicate realistically |
| 🔗 **Biometric Consistency** | Cross-modal consistency checker validates that visual and audio signals are coherent and belong to the same person |
| 🛡️ **Confidence Fusion** | Aggregates all modality signals into a final weighted `Authentic` / `Deepfake` verdict with a numeric confidence score |
| 🌑 **Modern UI** | React + Tailwind dark glassmorphism design with real-time analysis feedback |
| 🔒 **Privacy First** | All media is processed locally or on your own server — never permanently stored |

---

## 🧰 Tech Stack

### Backend
| Library | Purpose |
|---|---|
| **Python 3.9+** | Core runtime |
| **Flask + Flask-CORS** | REST API server |
| **PyTorch** | EfficientNet-B4 visual deepfake model inference |
| **MTCNN** | Face detection and alignment |
| **MediaPipe** | Facial landmark tracking for blink analysis |
| **Librosa** | Audio feature extraction (MFCC, spectral contrast) |
| **OpenCV** | Video frame processing and manipulation |
| **scikit-learn** | Sklearn ensemble model (joblib) |

### Frontend
| Library | Purpose |
|---|---|
| **React 18 + Vite** | Fast, component-based UI |
| **Tailwind CSS** | Utility-first styling |
| **Lucide React** | Icon system |

---

## 📁 Project Structure

```
DeepGuard/
├── backend/                        # Python Flask API & ML Pipelines
│   ├── app.py                      # Main routing, analysis orchestration
│   ├── run.py                      # Development server entrypoint
│   ├── audio_analyzer.py           # Audio MFCC & spectral analysis
│   ├── blink_analyzer.py           # MediaPipe blink dynamics
│   ├── consistency_analyzer.py     # Cross-modal biometric consistency
│   ├── config.py                   # Configuration constants
│   ├── test_face_detect.py         # Face detection unit tests
│   ├── test_models.py              # ML model loading & inference tests
│   └── requirements.txt            # Python dependencies
│
├── deepfake-detector/              # React Web Application
│   └── deepfake-detector/
│       ├── src/                    # UI components and pages
│       └── package.json            # Node dependencies
│
├── project1 (1)/                   # ML model weights directory
│   └── project1/                   # (populated by model download script)
│
├── start_backend.bat               # One-click Windows startup script
├── start_backend.sh                # One-click Linux/macOS startup script
├── SETUP_GUIDE.md                  # Detailed installation instructions
└── README.md                       # This file
```

---

## 📦 Pre-trained Models

The ML model weights are hosted on **HuggingFace Hub** (too large for GitHub):

> 🤗 **[yashtayade0908/deepguard-deepfake-detector](https://huggingface.co/yashtayade0908/deepguard-deepfake-detector)**

| Model File | Size | Description |
|---|---|---|
| `best_deepfake_detector.pth` | ~18 MB | EfficientNet-B4 visual deepfake detector |
| `best_deepfake_detector_cnn.pth` | ~65 MB | CNN-based deepfake detector |
| `fake_face_detector_pytorch.joblib` | ~12 MB | Sklearn ensemble face classifier |

### Download Models Automatically

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
print('All models downloaded successfully!')
"
```

---

## 🚀 Getting Started

> 💡 For the full step-by-step installation guide, see [**SETUP_GUIDE.md**](./SETUP_GUIDE.md).

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Yashtayade0/Multimodal-Deepfake-Detection-with-Biometric-Consistency.git
cd Multimodal-Deepfake-Detection-with-Biometric-Consistency
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Download ML Models

Run the download script from the **root** of the project (see [Pre-trained Models](#-pre-trained-models) section above).

### 4. Start the Backend

```bash
# From the backend/ directory
python run.py
```

Or use the one-click scripts from the project root:

```bash
# Windows
start_backend.bat

# Linux/macOS
bash start_backend.sh
```

The API will start at `http://localhost:5000`.

### 5. Start the Frontend

```bash
cd deepfake-detector/deepfake-detector
npm install
npm run dev
```

The web app will be available at `http://localhost:5173`.

---

## 🔌 API Reference

The backend exposes a REST API on port `5000`.

### `POST /analyze`

Analyzes an uploaded media file for deepfake indicators.

**Request:** `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `file` | File | Video, image, or audio file to analyze |

**Response:**

```json
{
  "verdict": "Deepfake Detected",
  "confidence": 0.94,
  "modalities": {
    "visual": { "score": 0.96, "label": "Fake" },
    "audio": { "score": 0.88, "label": "Fake" },
    "blink": { "score": 0.91, "blink_rate": 3.2, "label": "Abnormal" }
  }
}
```

---

## ⚖️ License & Ethics

This project is developed **exclusively for academic research and media authenticity** purposes.

- ✅ Media is **never permanently stored** — all processing is ephemeral
- ✅ Designed to protect against misinformation, not enable it
- ✅ Open-source for transparency and reproducibility
- ❌ **Not intended** for surveillance, unauthorized identification, or any harmful use

> If you use DeepGuard in your research, please credit this repository.

---

<div align="center">

Built with ❤️ by [Yash Tayade](https://github.com/Yashtayade0)

</div>
