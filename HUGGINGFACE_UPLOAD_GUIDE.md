# HuggingFace Model Upload Guide

This guide provides two methods to upload your DeepGuard models to HuggingFace Hub.

## ⚠️ Network Issue Detected

Your college/institute network is blocking HuggingFace (SSL ConnectionResetError 10054). You have two options:

---

## 🔥 Option A: Upload via Mobile Hotspot (Recommended for CLI)

### Step 1: Connect to Mobile Hotspot
1. Enable hotspot on your phone
2. Connect your laptop to the hotspot
3. Verify internet connection

### Step 2: Authenticate with HuggingFace

```bash
# Login with your token
hf auth login
```

When prompted, paste your HuggingFace token: `hf_YOUR_TOKEN_HERE`

### Step 3: Run the Upload Script

```bash
# Make the script executable (if on Linux/Mac)
chmod +x upload_to_huggingface.sh

# Run the script
bash upload_to_huggingface.sh
```

**OR** run commands manually:

```bash
# Create the repository
hf repo create deepguard-deepfake-detector --repo-type model

# Navigate to model directory
cd "project1 (1)/project1"

# Upload each model file
hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector.pth best_deepfake_detector.pth

hf upload yashtayade0908/deepguard-deepfake-detector best_deepfake_detector_cnn.pth best_deepfake_detector_cnn.pth

hf upload yashtayade0908/deepguard-deepfake-detector fake_face_detector_pytorch.joblib fake_face_detector_pytorch.joblib
```

---

## 🌐 Option B: Upload via Browser (Easiest - No Network Issues)

This method bypasses CLI and network restrictions entirely.

### Step 1: Create Repository

1. Go to [https://huggingface.co/new](https://huggingface.co/new)
2. Fill in the form:
   - **Owner**: yashtayade0908
   - **Model name**: deepguard-deepfake-detector
   - **License**: Choose appropriate license (e.g., MIT)
   - **Visibility**: Public
3. Click **Create model**

### Step 2: Upload Files via Web Interface

1. On your new repo page, click the **Files** tab
2. Click **Add file** → **Upload files**
3. Drag and drop these 3 files:
   - `E:\TY\sem1\Project 1\deepfake_proto\project1 (1)\project1\best_deepfake_detector.pth`
   - `E:\TY\sem1\Project 1\deepfake_proto\project1 (1)\project1\best_deepfake_detector_cnn.pth`
   - `E:\TY\sem1\Project 1\deepfake_proto\project1 (1)\project1\fake_face_detector_pytorch.joblib`
4. Add a commit message: "Upload DeepGuard model weights"
5. Click **Commit changes to main**

### Step 3: Add Model Card (Optional but Recommended)

1. On the repo page, click **Edit model card**
2. Add this content:

```markdown
---
license: mit
tags:
- deepfake-detection
- computer-vision
- pytorch
- efficientnet
---

# DeepGuard Deepfake Detector

Pre-trained models for the DeepGuard AI multimodal deepfake detection system.

## Model Files

- `best_deepfake_detector.pth` - EfficientNet-B4 visual detector (~18 MB)
- `best_deepfake_detector_cnn.pth` - CNN deepfake detector (~65 MB)
- `fake_face_detector_pytorch.joblib` - Sklearn ensemble model (~12 MB)

## Usage

```python
from huggingface_hub import hf_hub_download

# Download models
model_path = hf_hub_download(
    repo_id="yashtayade0908/deepguard-deepfake-detector",
    filename="best_deepfake_detector.pth"
)
```

## Project Repository

Full source code: [GitHub - DeepGuard](https://github.com/yashtayade0908/deepguard)
```

3. Click **Save**

---

## ✅ Verification

After upload (either method), verify your models are accessible:

1. Visit: https://huggingface.co/yashtayade0908/deepguard-deepfake-detector
2. You should see all 3 model files listed
3. Test download with:

```bash
pip install huggingface_hub

python -c "from huggingface_hub import hf_hub_download; print(hf_hub_download(repo_id='yashtayade0908/deepguard-deepfake-detector', filename='best_deepfake_detector.pth'))"
```

---

## 🔧 Troubleshooting

### "401 Unauthorized"
- Re-run `hf auth login` with a fresh token
- Get token from: https://huggingface.co/settings/tokens

### "ConnectionResetError 10054"
- Your network is blocking HuggingFace
- **Solution**: Use mobile hotspot or browser upload (Option B)

### "Repository already exists"
- Skip the `hf repo create` command
- Proceed directly to upload commands

---

## 📝 Next Steps

After successful upload, commit the README update:

```bash
cd "E:\TY\sem1\Project 1\deepfake_proto"
git add README.md HUGGINGFACE_UPLOAD_GUIDE.md
git commit -m "docs: add HuggingFace Hub model download instructions"
git push
```

---

**Recommendation**: Use **Option B (Browser Upload)** for the most reliable experience, especially on restricted networks.
