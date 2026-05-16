# 🚀 Quick Start - Upload Models to HuggingFace

## TL;DR - Fastest Method

### Option 1: Browser Upload (No CLI, No Network Issues) ⭐ RECOMMENDED

1. **Create repo**: Go to https://huggingface.co/new
   - Name: `deepguard-deepfake-detector`
   - Type: Model
   - Click "Create model"

2. **Upload files**: Click "Files" → "Add file" → "Upload files"
   - Drag these 3 files from `project1 (1)/project1/`:
     - `best_deepfake_detector.pth`
     - `best_deepfake_detector_cnn.pth`
     - `fake_face_detector_pytorch.joblib`

3. **Done!** ✓

---

### Option 2: CLI Upload (Requires Mobile Hotspot)

```bash
# 1. Connect to mobile hotspot first!

# 2. Login
hf auth login
# Paste your token when prompted

# 3. Run upload script
bash upload_to_huggingface.sh
```

---

## Verify Upload

```bash
python verify_huggingface_upload.py
```

---

## After Upload - Commit Changes

```bash
git add .
git commit -m "docs: add HuggingFace model upload guides and scripts"
git push
```

---

**Need help?** See [HUGGINGFACE_UPLOAD_GUIDE.md](./HUGGINGFACE_UPLOAD_GUIDE.md) for detailed instructions.
