1
# 🧠 Multimodal Deepfake Detection with Biometric Consistency


A full-stack AI-powered system for detecting deepfake media using multimodal analysis and biometric consistency verification.

This project combines **Computer Vision**, **Deep Learning**, and **Biometric Feature Validation** with a **Flask backend** and **React frontend** to provide an interactive deepfake detection platform.

---

## 🚀 Features

- 🎭 Deepfake detection using trained ML/DL models  
- 👁️ Facial biometric consistency verification  
- 🧠 Multimodal analysis (visual + biometric signals)  
- ⚡ REST API powered by Flask  
- 💻 Modern React-based frontend  
- 📂 Upload and analyze media files  
- 📊 Real-time detection results  

---

## 🏗️ Project Architecture

```

Deepfake-Detector-Project/
│
├── backend/                # Flask backend & ML models
│   ├── app.py
│   ├── requirements.txt
│   └── model files
│
├── deepfake-detector/      # React frontend
│   └── deepfake-detector/
│
├── uploads/                # Uploaded media storage
├── start_backend.bat
└── README.md

````

---

## 🛠️ Tech Stack

### 🔹 Backend

- Python  
- Flask  
- OpenCV  
- Deep Learning Models  
- NumPy / Pandas  

### 🔹 Frontend

- React (Vite)  
- JavaScript  
- Axios (API communication)  
- Modern UI components  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Yashtayade0/Multimodal-Deepfake-Detection-with-Biometric-Consistency.git
cd Multimodal-Deepfake-Detection-with-Biometric-Consistency
````

---

## 🖥️ Backend Setup

1. Navigate to backend folder:

```bash
cd backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
python app.py
```

OR simply run:

```bash
start_backend.bat
```

Backend will typically run on:

```
http://localhost:5000
```

---

## 🌐 Frontend Setup

1. Navigate to frontend directory:

```bash
cd deepfake-detector/deepfake-detector
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm run dev
```

Frontend usually runs on:

```
http://localhost:5173
```

---

## 🧪 How It Works

1. User uploads an image/video.
2. Frontend sends media to Flask API.
3. Backend:

   * Extracts facial features
   * Runs deepfake detection model
   * Performs biometric consistency validation
4. Detection results are returned and displayed in UI.

---

## 📊 Example Workflow

* Upload media
* System analyzes facial regions
* Model predicts real/fake probability
* Biometric mismatch detection performed
* Result displayed with confidence score

---

## 🔐 Research Context

This project is based on research in:

* Deepfake Detection
* Biometric Verification
* Multimodal AI Systems
* Computer Vision Security

It can be extended for:

* Social media content verification
* Digital forensics
* Identity fraud detection
* Security systems

---

## 📌 Future Improvements

* 🎥 Real-time video stream detection
* ☁️ Cloud deployment (AWS / GCP)
* 📱 Mobile support
* 🧠 Transformer-based deepfake models
* 📊 Model performance visualization

---

## 👨‍💻 Author

**Yash Tayade**
B.Tech Computer Engineering
Vishwakarma Institute of Information Technology


GitHub: [https://github.com/Yashtayade0](https://github.com/Yashtayade0)

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🤝 Contribute


