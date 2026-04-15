# DeepGuard Setup & Installation Guide

This guide will walk you through setting up and running the DeepGuard Multimodal Deepfake Detection platform locally. This comprises setting up the Python Flask background processor and the React frontend.

## Prerequisites

Before starting, ensure your system has the following installed:
- **Python 3.8 to 3.10**: Required for the ML pipelines, PyTorch, and MediaPipe.
- **Node.js (v16+)** & **npm**: Required for the React interface.
- **Git**

***Note on GPU hardware***: While a GPU (NVIDIA + CUDA) is not strictly required, deep learning model inference (EfficientNet, MTCNN) will be significantly faster with a CUDA-capable GPU.

---

## 1. Backend Setup (Flask + ML Models)

The backend handles the heavy lifting: running face extraction, blink rate calculation, and image classification.

1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Create a Virtual Environment**:
   It is highly recommended to isolate your Python dependencies.
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Optional)* If you have an NVIDIA GPU, you may want to install the CUDA-accelerated version of PyTorch by following the instructions at [pytorch.org](https://pytorch.org/).

5. **Start the API Server**:
   ```bash
   python run.py
   ```
   The backend should start and listen on `http://localhost:5000`. Keep this terminal window open.

---

## 2. Frontend Setup (React.js)

The React frontend provides the sleek dark-mode glassmorphism UI for uploading media and visualizing the results.

1. **Open a New Terminal Window**.

2. **Navigate to the Frontend Directory**:
   ```bash
   cd deepfake-detector/deepfake-detector
   ```

3. **Install Node Packages**:
   ```bash
   npm install
   ```

4. **Start the Development Server**:
   ```bash
   npm start
   ```
   *(If prompted that port 3000 is taken, type `Y` to automatically start on another port like 3001).*

5. **Open the Application**:
   Open a web browser and navigate to `http://localhost:3000`. You should see the DeepGuard interface and a green "Backend Connected" pill.

---

## Troubleshooting

- **"Backend Offline" on the Frontend**:
  Ensure the Python server is running, listening on port 5000, and is not producing errors. Ensure you haven't closed the backend terminal.

- **Missing Model Errors**:
  Ensure that you have extracted the `deepfake.zip` models payload and placed the necessary `.pth`, `.joblib`, or `.h5` model weight files in the directory referenced by `app.py` or the `backend/models/` folder as structured in your local implementation.

- **MediaPipe / OpenCV Camera Errors**:
  These dependencies sometimes require specific OS libraries (e.g., `libgl1-mesa-glx` on Linux headless servers). On Windows/Mac, pip usually handles the binary installations flawlessly.

- **CORS Issues**:
  If the frontend blocks the request on upload, verify `Flask-CORS` is active in `backend/app.py`.
