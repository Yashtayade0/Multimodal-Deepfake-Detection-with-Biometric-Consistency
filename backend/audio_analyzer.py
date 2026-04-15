"""
Audio Analysis Module for Deepfake Detection
Extracts audio from video files and analyzes spectral features
for synthetic speech / voice-cloning artifacts.
"""

import numpy as np
import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)

# Lazy imports – these are heavy; only load when actually needed
_librosa = None
_sf = None


def _ensure_imports():
    """Lazily import librosa and soundfile."""
    global _librosa, _sf
    if _librosa is None:
        try:
            import librosa
            _librosa = librosa
        except ImportError:
            logger.error("librosa is not installed. Run: pip install librosa")
            raise
    if _sf is None:
        try:
            import soundfile as sf
            _sf = sf
        except ImportError:
            logger.warning("soundfile not installed; falling back to librosa audioread")


# ---------------------------------------------------------------------------
# Audio extraction
# ---------------------------------------------------------------------------

def extract_audio(video_path: str, sr: int = 22050, max_duration: float = 60.0):
    """
    Extract audio waveform from a video file.

    Parameters
    ----------
    video_path : str
        Path to the video file.
    sr : int
        Target sample rate.
    max_duration : float
        Maximum seconds of audio to load (caps processing time).

    Returns
    -------
    tuple (np.ndarray, int)
        Mono waveform array and sample rate, or (None, sr) on failure.
    """
    _ensure_imports()

    # Strategy 1: Try using ffmpeg to extract a wav, then load it with librosa.
    #             This is the most reliable path on Windows.
    tmp_wav = None
    try:
        tmp_wav = tempfile.mktemp(suffix='.wav')
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vn',               # no video
            '-acodec', 'pcm_s16le',
            '-ar', str(sr),
            '-ac', '1',          # mono
            '-t', str(max_duration),
            tmp_wav
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        if result.returncode == 0 and os.path.exists(tmp_wav) and os.path.getsize(tmp_wav) > 0:
            y, loaded_sr = _librosa.load(tmp_wav, sr=sr, mono=True, duration=max_duration)
            logger.info(f"Audio extracted via ffmpeg: {len(y)} samples @ {loaded_sr} Hz")
            return y, loaded_sr
        else:
            logger.warning("ffmpeg audio extraction returned non-zero or empty file")
    except FileNotFoundError:
        logger.warning("ffmpeg not found on PATH; trying librosa directly")
    except subprocess.TimeoutExpired:
        logger.warning("ffmpeg audio extraction timed out")
    except Exception as e:
        logger.warning(f"ffmpeg extraction failed: {e}")
    finally:
        if tmp_wav and os.path.exists(tmp_wav):
            try:
                os.remove(tmp_wav)
            except OSError:
                pass

    # Strategy 2: Let librosa try to load directly (requires audioread/ffmpeg in PATH).
    try:
        y, loaded_sr = _librosa.load(video_path, sr=sr, mono=True, duration=max_duration)
        if len(y) > 0:
            logger.info(f"Audio loaded via librosa directly: {len(y)} samples")
            return y, loaded_sr
    except Exception as e:
        logger.warning(f"librosa direct load failed: {e}")

    logger.error("Could not extract audio from video.")
    return None, sr


# ---------------------------------------------------------------------------
# Feature computation
# ---------------------------------------------------------------------------

def compute_audio_features(y: np.ndarray, sr: int, n_segments: int = 5) -> dict:
    """
    Compute spectral audio features per temporal segment.

    Features per segment
    --------------------
    - mfcc_mean   : mean of first 13 MFCCs
    - mfcc_std    : std-dev of first 13 MFCCs
    - spectral_centroid : brightness
    - spectral_rolloff  : high-frequency energy boundary
    - zcr         : zero-crossing rate (voiced vs unvoiced)
    - rms_energy  : loudness
    - spectral_bandwidth : spread of the spectrum
    - spectral_flatness  : tonal vs noisy

    Returns
    -------
    dict with keys 'segments' (list of per-segment feature dicts) and
    'global' (aggregated features).
    """
    _ensure_imports()
    lb = _librosa

    total_samples = len(y)
    seg_len = total_samples // n_segments

    if seg_len < sr // 4:
        # Audio too short to split meaningfully
        n_segments = 1
        seg_len = total_samples

    segments = []
    for i in range(n_segments):
        start = i * seg_len
        end = start + seg_len if i < n_segments - 1 else total_samples
        seg = y[start:end]

        if len(seg) < 512:
            continue

        # MFCCs
        mfccs = lb.feature.mfcc(y=seg, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)

        # Spectral features
        centroid = np.mean(lb.feature.spectral_centroid(y=seg, sr=sr))
        rolloff = np.mean(lb.feature.spectral_rolloff(y=seg, sr=sr))
        zcr = np.mean(lb.feature.zero_crossing_rate(seg))
        rms = np.mean(lb.feature.rms(y=seg))
        bandwidth = np.mean(lb.feature.spectral_bandwidth(y=seg, sr=sr))
        flatness = np.mean(lb.feature.spectral_flatness(y=seg))

        segments.append({
            'mfcc_mean': mfcc_mean.tolist(),
            'mfcc_std': mfcc_std.tolist(),
            'spectral_centroid': float(centroid),
            'spectral_rolloff': float(rolloff),
            'zcr': float(zcr),
            'rms_energy': float(rms),
            'spectral_bandwidth': float(bandwidth),
            'spectral_flatness': float(flatness),
        })

    # Global aggregates across segments
    if segments:
        global_features = {
            'avg_centroid': float(np.mean([s['spectral_centroid'] for s in segments])),
            'std_centroid': float(np.std([s['spectral_centroid'] for s in segments])),
            'avg_zcr': float(np.mean([s['zcr'] for s in segments])),
            'std_zcr': float(np.std([s['zcr'] for s in segments])),
            'avg_flatness': float(np.mean([s['spectral_flatness'] for s in segments])),
            'std_flatness': float(np.std([s['spectral_flatness'] for s in segments])),
            'avg_rms': float(np.mean([s['rms_energy'] for s in segments])),
            'std_rms': float(np.std([s['rms_energy'] for s in segments])),
            'avg_bandwidth': float(np.mean([s['spectral_bandwidth'] for s in segments])),
            'mfcc_segment_drift': float(np.mean([
                np.linalg.norm(
                    np.array(segments[j]['mfcc_mean']) - np.array(segments[j - 1]['mfcc_mean'])
                )
                for j in range(1, len(segments))
            ])) if len(segments) > 1 else 0.0,
        }
    else:
        global_features = {}

    return {'segments': segments, 'global': global_features}


# ---------------------------------------------------------------------------
# Anomaly detection (heuristic scoring)
# ---------------------------------------------------------------------------

def detect_audio_anomalies(features: dict) -> dict:
    """
    Score audio features for deepfake indicators.

    Scoring heuristics (each contributes to a 0-100 suspicion score):
    1. Spectral flatness — synthetic voices tend to have higher flatness
       (more noise-like) or abnormally low flatness (pure tones).
    2. MFCC segment drift — abrupt changes between segments suggest splicing
       or inconsistent voice synthesis.
    3. ZCR variability — natural speech has moderate ZCR variation; very low
       std indicates unnaturally uniform voicing.
    4. RMS energy variability — natural speech has dynamic loudness; TTS tends
       to be very even.
    5. Spectral bandwidth consistency — synthetic audio often has a narrower
       and more consistent bandwidth.

    Returns dict with 'score' (0-100, higher = more suspicious),
    'indicators' (list of strings), and 'segment_scores' (list of floats).
    """
    g = features.get('global', {})
    segments = features.get('segments', [])

    if not g or not segments:
        return {
            'score': 50.0,
            'indicators': ['Insufficient audio data for analysis'],
            'segment_scores': [50.0] * 5
        }

    score = 0.0
    indicators = []

    # 1. Spectral flatness analysis
    avg_flatness = g.get('avg_flatness', 0)
    if avg_flatness > 0.3:
        score += 20
        indicators.append('High spectral flatness (noise-like, possible synthetic)')
    elif avg_flatness < 0.01:
        score += 15
        indicators.append('Very low spectral flatness (abnormally tonal)')
    else:
        score += max(0, (avg_flatness - 0.05) / 0.25 * 10)

    # 2. MFCC drift between segments
    mfcc_drift = g.get('mfcc_segment_drift', 0)
    if mfcc_drift > 40:
        score += 25
        indicators.append('Large MFCC drift between segments (possible audio splicing)')
    elif mfcc_drift > 20:
        score += 12
        indicators.append('Moderate MFCC variation between segments')
    elif mfcc_drift < 3 and len(segments) > 1:
        score += 18
        indicators.append('Unnaturally consistent voice features across segments')

    # 3. ZCR variability
    std_zcr = g.get('std_zcr', 0)
    if std_zcr < 0.005 and len(segments) > 1:
        score += 15
        indicators.append('Very low ZCR variability (robotic speech pattern)')
    elif std_zcr < 0.01:
        score += 8

    # 4. RMS energy variability
    std_rms = g.get('std_rms', 0)
    avg_rms = g.get('avg_rms', 0.01)
    rms_cv = std_rms / max(avg_rms, 1e-8)  # coefficient of variation
    if rms_cv < 0.05 and len(segments) > 1:
        score += 15
        indicators.append('Unnaturally even loudness (TTS signature)')
    elif rms_cv < 0.1:
        score += 6

    # 5. Spectral bandwidth consistency
    std_bw = g.get('std_bandwidth', float(np.std([s['spectral_bandwidth'] for s in segments])) if segments else 0)
    avg_bw = g.get('avg_bandwidth', 1.0)
    bw_cv = std_bw / max(avg_bw, 1e-8)
    if bw_cv < 0.02 and len(segments) > 1:
        score += 10
        indicators.append('Very consistent spectral bandwidth (possible voice cloning)')

    # Clamp to 0-100
    score = float(np.clip(score, 0, 100))

    # Per-segment scores (based on local flatness + zcr deviation from mean)
    segment_scores = []
    for seg in segments:
        seg_s = 50.0
        # Higher flatness -> more suspicious
        seg_s += (seg['spectral_flatness'] - 0.05) / 0.3 * 30
        # Very low zcr -> suspicious
        if seg['zcr'] < 0.03:
            seg_s += 10
        seg_s = float(np.clip(seg_s, 0, 100))
        segment_scores.append(round(seg_s, 1))

    # Pad/trim to exactly 5 entries for the timeline
    while len(segment_scores) < 5:
        segment_scores.append(segment_scores[-1] if segment_scores else 50.0)
    segment_scores = segment_scores[:5]

    if not indicators:
        indicators.append('Audio appears natural')

    return {
        'score': round(score, 1),
        'indicators': indicators,
        'segment_scores': segment_scores
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def analyze_audio(video_path: str, max_duration: float = 60.0) -> dict:
    """
    Full audio analysis pipeline for deepfake detection.

    Parameters
    ----------
    video_path : str
        Path to the video file.
    max_duration : float
        Max seconds of audio to process.

    Returns
    -------
    dict with keys:
        score     : float 0-100 (higher = more suspicious of being fake)
        status    : 'authentic' | 'suspicious' | 'fake'
        features  : list of human-readable feature descriptions
        timeline  : list of 5 float scores (per-segment)
    """
    logger.info(f"Starting audio analysis for: {video_path}")

    # Extract audio
    y, sr = extract_audio(video_path, max_duration=max_duration)

    if y is None or len(y) < 1024:
        logger.warning("No usable audio extracted from video")
        return {
            'score': 0.0,
            'status': 'authentic',
            'features': ['No audio track found or audio too short'],
            'timeline': [0.0] * 5
        }

    # Compute features
    features = compute_audio_features(y, sr, n_segments=5)
    logger.info(f"Audio features computed: {len(features.get('segments', []))} segments")

    # Detect anomalies
    anomalies = detect_audio_anomalies(features)
    score = anomalies['score']

    # Determine status
    if score >= 60:
        status = 'fake'
    elif score >= 35:
        status = 'suspicious'
    else:
        status = 'authentic'

    result = {
        'score': score,
        'status': status,
        'features': anomalies['indicators'],
        'timeline': anomalies['segment_scores']
    }

    logger.info(f"Audio analysis complete: score={score}, status={status}")
    return result


def analyze_audio_for_image() -> dict:
    """
    Return a neutral audio result for image-only uploads
    (audio analysis is not applicable to still images).
    """
    return {
        'score': 0.0,
        'status': 'authentic',
        'features': ['Audio analysis not applicable for images'],
        'timeline': [0.0] * 5
    }
