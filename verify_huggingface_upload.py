#!/usr/bin/env python3
"""
HuggingFace Model Upload Verification Script
Checks if models are accessible and provides download instructions
"""

import os
import sys

def check_huggingface_hub():
    """Check if huggingface_hub is installed"""
    try:
        import huggingface_hub
        print("✓ huggingface_hub is installed")
        return True
    except ImportError:
        print("✗ huggingface_hub not found")
        print("\nInstall with: pip install huggingface_hub")
        return False

def verify_models_exist():
    """Check if model files exist locally"""
    model_dir = os.path.join("project1 (1)", "project1")
    models = [
        "best_deepfake_detector.pth",
        "best_deepfake_detector_cnn.pth",
        "fake_face_detector_pytorch.joblib"
    ]
    
    print("\n" + "="*60)
    print("LOCAL MODEL FILES CHECK")
    print("="*60)
    
    all_exist = True
    for model in models:
        path = os.path.join(model_dir, model)
        exists = os.path.exists(path)
        size = os.path.getsize(path) / (1024 * 1024) if exists else 0
        
        status = "✓" if exists else "✗"
        print(f"{status} {model}")
        if exists:
            print(f"  Size: {size:.2f} MB")
            print(f"  Path: {path}")
        else:
            print(f"  NOT FOUND at: {path}")
            all_exist = False
    
    return all_exist

def test_download_from_hub():
    """Test downloading a model from HuggingFace Hub"""
    try:
        from huggingface_hub import hf_hub_download, list_repo_files
        
        repo_id = "yashtayade0908/deepguard-deepfake-detector"
        
        print("\n" + "="*60)
        print("HUGGINGFACE HUB CHECK")
        print("="*60)
        print(f"Repository: {repo_id}")
        print(f"URL: https://huggingface.co/{repo_id}")
        
        try:
            # List files in the repository
            print("\nAttempting to list repository files...")
            files = list_repo_files(repo_id)
            
            print(f"\n✓ Repository is accessible!")
            print(f"\nFiles found in repository:")
            for f in files:
                print(f"  - {f}")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Cannot access repository")
            print(f"Error: {str(e)}")
            print("\nPossible reasons:")
            print("  1. Repository doesn't exist yet")
            print("  2. Repository is private and you're not authenticated")
            print("  3. Network connectivity issues")
            print("\nTo upload models, use one of these methods:")
            print("  • Browser upload: https://huggingface.co/new")
            print("  • CLI upload: See HUGGINGFACE_UPLOAD_GUIDE.md")
            return False
            
    except ImportError:
        print("\n✗ Cannot test - huggingface_hub not installed")
        return False

def print_upload_instructions():
    """Print quick upload instructions"""
    print("\n" + "="*60)
    print("UPLOAD INSTRUCTIONS")
    print("="*60)
    
    print("\n🌐 BROWSER UPLOAD (Recommended):")
    print("  1. Go to: https://huggingface.co/new")
    print("  2. Create repo: deepguard-deepfake-detector")
    print("  3. Upload files via web interface")
    print("  4. Files to upload:")
    print("     - project1 (1)/project1/best_deepfake_detector.pth")
    print("     - project1 (1)/project1/best_deepfake_detector_cnn.pth")
    print("     - project1 (1)/project1/fake_face_detector_pytorch.joblib")
    
    print("\n💻 CLI UPLOAD (Requires mobile hotspot):")
    print("  1. Connect to mobile hotspot")
    print("  2. Run: hf auth login")
    print("  3. Run: bash upload_to_huggingface.sh")
    
    print("\n📖 Full guide: See HUGGINGFACE_UPLOAD_GUIDE.md")

def main():
    print("="*60)
    print("DEEPGUARD HUGGINGFACE UPLOAD VERIFICATION")
    print("="*60)
    
    # Check dependencies
    has_hf = check_huggingface_hub()
    
    # Check local files
    models_exist = verify_models_exist()
    
    if not models_exist:
        print("\n⚠️  WARNING: Some model files are missing locally!")
        print("Make sure you're running this from the correct directory.")
        return 1
    
    # Test HuggingFace Hub access
    if has_hf:
        hub_accessible = test_download_from_hub()
        
        if hub_accessible:
            print("\n" + "="*60)
            print("✓ SUCCESS - Models are uploaded and accessible!")
            print("="*60)
            print("\nYour models can be downloaded with:")
            print("""
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="yashtayade0908/deepguard-deepfake-detector",
    filename="best_deepfake_detector.pth"
)
""")
        else:
            print_upload_instructions()
    else:
        print_upload_instructions()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
