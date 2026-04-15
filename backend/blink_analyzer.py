"""
Blink / Physiological Analysis Module for Deepfake Detection
Uses MediaPipe FaceMesh to track eye landmarks and detect
unnatural blink patterns that are typical of deepfakes.
"""

import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)

# Lazy import for mediapipe
_mp = None
_mp_face_mesh = None


def _ensure_imports():
    """Lazily import mediapipe."""
    global _mp, _mp_face_mesh
    if _mp is None:
        try:
            import mediapipe as mp
            _mp = mp
            _mp_face_mesh = mp.solutions.face_mesh
        except ImportError:
            logger.error("mediapipe is not installed. Run: pip install mediapipe")
            raise


# ---------------------------------------------------------------------------
# MediaPipe FaceMesh eye landmark indices (468-point model)
# ---------------------------------------------------------------------------
# Right eye landmarks (6 points for EAR)
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
# Left eye landmarks (6 points for EAR)
LEFT_EYE = [362, 385, 387, 263, 373, 380]

# EAR thresholds
EAR_BLINK_THRESHOLD = 0.21     # Below this = eyes closed (blink)
EAR_CONSEC_FRAMES = 2          # Minimum consecutive frames for a blink

# Natural blink parameters (from literature)
NATURAL_BLINK_RATE_MIN = 10    # blinks per minute (low end)
NATURAL_BLINK_RATE_MAX = 25    # blinks per minute (high end)
NATURAL_BLINK_DURATION_MIN = 0.1   # seconds
NATURAL_BLINK_DURATION_MAX = 0.4   # seconds


# ---------------------------------------------------------------------------
# Eye Aspect Ratio computation
# ---------------------------------------------------------------------------

def compute_ear(landmarks, eye_indices: list, img_w: int, img_h: int) -> float:
    """
    Compute Eye Aspect Ratio from MediaPipe FaceMesh landmarks.

    EAR = (||p2-p6|| + ||p3-p5||) / (2.0 * ||p1-p4||)

    Where p1-p6 are the 6 eye landmark points:
        p1 = outer corner, p4 = inner corner
        p2, p6 = upper/lower at outer third
        p3, p5 = upper/lower at inner third

    Parameters
    ----------
    landmarks : mediapipe NormalizedLandmarkList
    eye_indices : list of 6 ints
    img_w, img_h : image dimensions for denormalization

    Returns
    -------
    float : EAR value (typically 0.15-0.35 for open eyes)
    """
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        pts.append(np.array([lm.x * img_w, lm.y * img_h]))

    p1, p2, p3, p4, p5, p6 = pts

    # Vertical distances
    v1 = np.linalg.norm(p2 - p6)
    v2 = np.linalg.norm(p3 - p5)
    # Horizontal distance
    h = np.linalg.norm(p1 - p4)

    if h < 1e-6:
        return 0.0

    ear = (v1 + v2) / (2.0 * h)
    return float(ear)


# ---------------------------------------------------------------------------
# Blink detection across video frames
# ---------------------------------------------------------------------------

def analyze_blinks(video_path: str, sample_rate: int = 2, max_duration: float = 60.0) -> dict:
    """
    Analyze blink patterns in a video for deepfake detection.

    Parameters
    ----------
    video_path : str
        Path to the video file.
    sample_rate : int
        Process every Nth frame (higher = faster but less precise).
    max_duration : float
        Maximum seconds of video to process.

    Returns
    -------
    dict with keys:
        score    : float 0-100 (higher = more suspicious)
        status   : 'authentic' | 'suspicious' | 'fake'
        metrics  : list of human-readable metric descriptions
        timeline : list of 5 float scores
    """
    _ensure_imports()
    logger.info(f"Starting blink analysis for: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Cannot open video: {video_path}")
        return _fallback_result("Could not open video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 30.0
    if total_frames <= 0:
        return _fallback_result("Empty or unreadable video")

    max_frames = int(max_duration * fps)
    frames_to_process = min(total_frames, max_frames)

    logger.info(f"Video: {fps:.1f} fps, {total_frames} total frames, processing up to {frames_to_process}")

    # Initialize FaceMesh
    face_mesh = _mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    ear_values = []           # EAR per processed frame
    frame_indices = []        # Which frame numbers were processed
    blink_frames = []         # Frame indices where blinks are detected
    in_blink = False
    blink_start_frame = None
    blink_counter = 0         # Consecutive low-EAR frames
    blink_events = []         # List of (start_frame, end_frame) for each blink
    frames_with_face = 0

    frame_idx = 0
    while frame_idx < frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % sample_rate == 0:
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                frames_with_face += 1
                landmarks = results.multi_face_landmarks[0].landmark

                # Compute EAR for both eyes, take average
                left_ear = compute_ear(landmarks, LEFT_EYE, w, h)
                right_ear = compute_ear(landmarks, RIGHT_EYE, w, h)
                avg_ear = (left_ear + right_ear) / 2.0

                ear_values.append(avg_ear)
                frame_indices.append(frame_idx)

                # Blink detection state machine
                if avg_ear < EAR_BLINK_THRESHOLD:
                    blink_counter += 1
                    if not in_blink and blink_counter >= EAR_CONSEC_FRAMES:
                        in_blink = True
                        blink_start_frame = frame_idx - (blink_counter - 1) * sample_rate
                else:
                    if in_blink:
                        blink_end_frame = frame_idx
                        blink_events.append((blink_start_frame, blink_end_frame))
                        in_blink = False
                    blink_counter = 0

        frame_idx += 1

    cap.release()
    face_mesh.close()

    # Close any open blink at end
    if in_blink and blink_start_frame is not None:
        blink_events.append((blink_start_frame, frame_idx))

    logger.info(f"Processed {len(ear_values)} frames with face, {len(blink_events)} blinks detected")

    if len(ear_values) < 10:
        return _fallback_result("Too few frames with detected face for blink analysis")

    # -----------------------------------------------------------------------
    # Compute blink metrics
    # -----------------------------------------------------------------------
    duration_seconds = frames_to_process / fps
    n_blinks = len(blink_events)
    blink_rate_per_min = (n_blinks / duration_seconds) * 60.0 if duration_seconds > 0 else 0

    # Blink durations in seconds
    blink_durations = [(end - start) / fps for start, end in blink_events]
    avg_blink_duration = float(np.mean(blink_durations)) if blink_durations else 0.0

    # Inter-blink intervals
    if len(blink_events) > 1:
        ibi = [(blink_events[i + 1][0] - blink_events[i][1]) / fps
               for i in range(len(blink_events) - 1)]
        ibi_std = float(np.std(ibi))
        ibi_mean = float(np.mean(ibi))
        ibi_cv = ibi_std / max(ibi_mean, 1e-8)  # coefficient of variation
    else:
        ibi_std = 0.0
        ibi_mean = 0.0
        ibi_cv = 0.0

    # EAR statistics
    ear_mean = float(np.mean(ear_values))
    ear_std = float(np.std(ear_values))
    ear_range = float(np.max(ear_values) - np.min(ear_values))

    # -----------------------------------------------------------------------
    # Scoring
    # -----------------------------------------------------------------------
    score = 0.0
    metrics = []

    # 1. Blink rate check
    if n_blinks == 0 and duration_seconds > 5:
        score += 30
        metrics.append(f'No blinks detected in {duration_seconds:.0f}s (highly suspicious)')
    elif blink_rate_per_min < NATURAL_BLINK_RATE_MIN and duration_seconds > 10:
        score += 20
        metrics.append(f'Low blink rate: {blink_rate_per_min:.1f}/min (normal: {NATURAL_BLINK_RATE_MIN}-{NATURAL_BLINK_RATE_MAX})')
    elif blink_rate_per_min > NATURAL_BLINK_RATE_MAX * 2:
        score += 15
        metrics.append(f'Abnormally high blink rate: {blink_rate_per_min:.1f}/min')
    else:
        metrics.append(f'Blink rate: {blink_rate_per_min:.1f}/min (normal range)')

    # 2. Blink duration check
    if blink_durations:
        too_short = sum(1 for d in blink_durations if d < NATURAL_BLINK_DURATION_MIN)
        too_long = sum(1 for d in blink_durations if d > NATURAL_BLINK_DURATION_MAX)
        abnormal_pct = (too_short + too_long) / len(blink_durations)
        if abnormal_pct > 0.5:
            score += 15
            metrics.append(f'Abnormal blink durations ({abnormal_pct * 100:.0f}% outside natural range)')
        else:
            metrics.append(f'Avg blink duration: {avg_blink_duration * 1000:.0f}ms (normal)')

    # 3. Blink regularity (too regular = robotic)
    if len(blink_events) >= 3:
        if ibi_cv < 0.15:
            score += 20
            metrics.append(f'Blinks are unnaturally regular (CV={ibi_cv:.2f})')
        elif ibi_cv < 0.25:
            score += 8
            metrics.append(f'Blinks slightly too regular (CV={ibi_cv:.2f})')
        else:
            metrics.append(f'Blink timing variability is natural (CV={ibi_cv:.2f})')

    # 4. EAR stability (deepfakes often have very stable EAR)
    if ear_std < 0.008 and len(ear_values) > 30:
        score += 20
        metrics.append(f'Eye openness is unnaturally stable (std={ear_std:.4f})')
    elif ear_std < 0.015:
        score += 10
        metrics.append(f'Low eye variability detected (std={ear_std:.4f})')
    else:
        metrics.append(f'Natural eye movement variability (std={ear_std:.4f})')

    # 5. EAR range
    if ear_range < 0.05 and len(ear_values) > 30:
        score += 10
        metrics.append('Very narrow EAR range (minimal eye movement)')

    # Clamp
    score = float(np.clip(score, 0, 100))

    # Status
    if score >= 55:
        status = 'fake'
    elif score >= 30:
        status = 'suspicious'
    else:
        status = 'authentic'

    # -----------------------------------------------------------------------
    # Per-segment timeline (split EAR values into 5 chunks)
    # -----------------------------------------------------------------------
    timeline = _compute_timeline(ear_values, n_segments=5)

    result = {
        'score': round(score, 1),
        'status': status,
        'metrics': metrics,
        'timeline': timeline,
        'details': {
            'blink_count': n_blinks,
            'blink_rate_per_min': round(blink_rate_per_min, 1),
            'avg_blink_duration_ms': round(avg_blink_duration * 1000, 1),
            'ear_mean': round(ear_mean, 4),
            'ear_std': round(ear_std, 4),
            'frames_analyzed': len(ear_values),
            'frames_with_face': frames_with_face,
            'duration_seconds': round(duration_seconds, 1)
        }
    }

    logger.info(f"Blink analysis complete: score={score}, status={status}, "
                f"blinks={n_blinks}, rate={blink_rate_per_min:.1f}/min")
    return result


def _compute_timeline(ear_values: list, n_segments: int = 5) -> list:
    """
    Convert EAR values into a 5-point timeline of 'naturalness' scores.
    Lower EAR std within a segment → higher suspicion score.
    """
    if not ear_values:
        return [50.0] * n_segments

    arr = np.array(ear_values)
    seg_len = len(arr) // n_segments
    if seg_len < 1:
        seg_len = 1

    scores = []
    for i in range(n_segments):
        start = i * seg_len
        end = start + seg_len if i < n_segments - 1 else len(arr)
        seg = arr[start:end]

        if len(seg) < 2:
            scores.append(50.0)
            continue

        seg_std = float(np.std(seg))
        seg_range = float(np.max(seg) - np.min(seg))

        # Score: low variability = higher suspicion
        if seg_std < 0.008:
            s = 75.0
        elif seg_std < 0.015:
            s = 55.0
        elif seg_std < 0.03:
            s = 35.0
        else:
            s = 20.0

        scores.append(round(s, 1))

    return scores


def _fallback_result(reason: str) -> dict:
    """Return a neutral result when analysis cannot proceed."""
    return {
        'score': 0.0,
        'status': 'authentic',
        'metrics': [reason],
        'timeline': [0.0] * 5,
        'details': {}
    }


def analyze_blinks_for_image() -> dict:
    """
    Return a neutral blink result for image-only uploads
    (blink analysis is not applicable to still images).
    """
    return {
        'score': 0.0,
        'status': 'authentic',
        'metrics': ['Blink analysis not applicable for images'],
        'timeline': [0.0] * 5,
        'details': {}
    }
