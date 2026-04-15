import sys
sys.path.insert(0, '.')
import cv2
import os
from pathlib import Path
import app

app.load_models()

test_dirs = [
    Path(r'e:\TY\sem1\Project 1\Proto\project1 (1)\project1\photo\Dataset\Test\Real'),
    Path(r'e:\TY\sem1\Project 1\Proto\project1 (1)\project1\photo\Dataset\Test\Fake'),
]

for d in test_dirs:
    if d.exists():
        imgs = [f for f in d.iterdir() if f.suffix.lower() in ('.jpg', '.png', '.jpeg')][:3]
        print(f'\nDir: {d.name}')
        for img_path in imgs:
            print(f'  Testing: {img_path.name}')
            image = cv2.imread(str(img_path))
            if image is None:
                print('    cv2.imread returned None!')
                continue
            print(f'    Shape: {image.shape}')
            faces = app.detect_faces(image)
            print(f'    Faces found: {len(faces)}')
            if faces:
                for i, face_data in enumerate(faces):
                    bb = face_data['bbox']
                    print(f'    Face {i}: bbox={bb}')
            else:
                # Try with lower size threshold
                print('    Trying with MTCNN directly...')
                import cv2 as cv
                img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                boxes, probs = app.mtcnn_detector.detect(img_rgb)
                print(f'    Raw MTCNN boxes: {boxes}')
                print(f'    Raw MTCNN probs: {probs}')
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.astype(int)
                        w = x2 - x1
                        h = y2 - y1
                        print(f'    Box size: {w}x{h} (min filter is 50x50)')
    else:
        print(f'Dir not found: {d}')

# Also test uploads folder
uploads = Path('uploads')
if uploads.exists():
    for f in uploads.iterdir():
        print(f'\nUploads dir file: {f.name}')
