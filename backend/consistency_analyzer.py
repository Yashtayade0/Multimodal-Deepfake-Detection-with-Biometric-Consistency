"""
Cross-Modal Consistency Analysis Module for Deepfake Detection
Computes actual correlation between modality timelines to detect
inconsistencies that indicate manipulation.
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)


def _pearson_correlation(a: list, b: list) -> float:
    """
    Compute Pearson correlation coefficient between two lists.
    Returns a value in [-1, 1].  On failure or constant arrays, returns 0.
    """
    if len(a) != len(b) or len(a) < 2:
        return 0.0

    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)

    # If either array is constant, correlation is undefined → treat as 0
    if np.std(a_arr) < 1e-10 or np.std(b_arr) < 1e-10:
        return 0.0

    corr = np.corrcoef(a_arr, b_arr)[0, 1]
    if np.isnan(corr):
        return 0.0
    return float(corr)


def _agreement_score(score_a: float, score_b: float) -> float:
    """
    Compute an agreement score between two modality overall scores.
    Both scores should be on a 0-100 scale.

    The idea: if both modalities agree (both high suspicion or both low),
    consistency is high.  If they disagree, consistency is low.

    Returns a value in [0, 1].
    """
    # Normalize to 0-1
    a = score_a / 100.0
    b = score_b / 100.0

    # Simple agreement: 1 - absolute difference
    agreement = 1.0 - abs(a - b)
    return float(np.clip(agreement, 0, 1))


def compute_consistency(
    visual_score: float,
    visual_timeline: list,
    audio_score: float,
    audio_timeline: list,
    blink_score: float,
    blink_timeline: list,
    threshold: float = 0.75
) -> dict:
    """
    Compute cross-modal consistency between the three analysis modalities.

    For genuine media, all modalities should produce consistent results
    (either all indicating authentic or all indicating fake).  In a
    deepfake where only the face is swapped, the visual modality may
    flag it as fake while audio remains authentic — creating a
    consistency mismatch.

    Parameters
    ----------
    visual_score : float
        Overall visual suspicion score (0-100).
    visual_timeline : list of float
        Per-segment visual scores (5 values).
    audio_score : float
        Overall audio suspicion score (0-100).
    audio_timeline : list of float
        Per-segment audio scores (5 values).
    blink_score : float
        Overall blink suspicion score (0-100).
    blink_timeline : list of float
        Per-segment blink scores (5 values).
    threshold : float
        Minimum consistency to be considered "passing" (default 0.75).

    Returns
    -------
    dict with keys:
        visualAudio  : float 0-1
        visualBlink  : float 0-1
        audioBlink   : float 0-1
        threshold    : float
        overall      : float 0-1 (average consistency)
        interpretation : str
    """
    logger.info("Computing cross-modal consistency")

    # Ensure timelines are length-5
    vt = _pad_timeline(visual_timeline)
    at = _pad_timeline(audio_timeline)
    bt = _pad_timeline(blink_timeline)

    # --- Visual ↔ Audio ---
    # Combine timeline correlation with overall score agreement
    va_corr = _pearson_correlation(vt, at)
    va_agreement = _agreement_score(visual_score, audio_score)
    # Weighted blend: 40% timeline correlation, 60% score agreement
    # Map correlation from [-1,1] to [0,1]:  (corr + 1) / 2
    va_corr_norm = (va_corr + 1.0) / 2.0
    visual_audio = 0.4 * va_corr_norm + 0.6 * va_agreement

    # --- Visual ↔ Blink ---
    vb_corr = _pearson_correlation(vt, bt)
    vb_agreement = _agreement_score(visual_score, blink_score)
    vb_corr_norm = (vb_corr + 1.0) / 2.0
    visual_blink = 0.4 * vb_corr_norm + 0.6 * vb_agreement

    # --- Audio ↔ Blink ---
    ab_corr = _pearson_correlation(at, bt)
    ab_agreement = _agreement_score(audio_score, blink_score)
    ab_corr_norm = (ab_corr + 1.0) / 2.0
    audio_blink = 0.4 * ab_corr_norm + 0.6 * ab_agreement

    overall = float(np.mean([visual_audio, visual_blink, audio_blink]))

    # Interpretation
    if overall >= threshold:
        interpretation = "All modalities are consistent — results are reliable"
    elif overall >= 0.5:
        interpretation = ("Moderate cross-modal inconsistency detected — "
                          "some modalities disagree, suggesting partial manipulation")
    else:
        interpretation = ("Significant cross-modal inconsistency — "
                          "modalities strongly disagree, indicating likely deepfake manipulation")

    result = {
        'visualAudio': round(float(np.clip(visual_audio, 0, 1)), 3),
        'visualBlink': round(float(np.clip(visual_blink, 0, 1)), 3),
        'audioBlink': round(float(np.clip(audio_blink, 0, 1)), 3),
        'threshold': threshold,
        'overall': round(float(np.clip(overall, 0, 1)), 3),
        'interpretation': interpretation
    }

    logger.info(f"Consistency: VA={result['visualAudio']}, VB={result['visualBlink']}, "
                f"AB={result['audioBlink']}, overall={result['overall']}")
    return result


def compute_consistency_for_image(visual_score: float, visual_timeline: list) -> dict:
    """
    For image uploads, audio and blink data are unavailable.
    Return consistency based only on the visual modality (always consistent
    with itself).
    """
    return {
        'visualAudio': 1.0,
        'visualBlink': 1.0,
        'audioBlink': 1.0,
        'threshold': 0.75,
        'overall': 1.0,
        'interpretation': 'Only visual modality available for images — consistency is N/A'
    }


def _pad_timeline(timeline: list, length: int = 5) -> list:
    """Ensure a timeline has exactly `length` entries."""
    if not timeline:
        return [50.0] * length
    tl = list(timeline)
    while len(tl) < length:
        tl.append(tl[-1])
    return tl[:length]
