"""
detection/face_matching.py
==========================

• Detects and affine-aligns faces
• Extracts 128-D embeddings with DeepFace Facenet
• Works with every DeepFace release (≤0.0.45, 0.0.46-0.0.92, ≥0.0.93)
• Thread-safe (global TensorFlow lock)
"""

from __future__ import annotations

import os
import cv2
import dlib
import numpy as np
import threading
import inspect
from typing import List, Dict, Tuple, Any, Optional
from scipy.spatial.distance import cosine
from deepface import DeepFace

# ------------------------------------------------------------------
# Resources ---------------------------------------------------------
# ------------------------------------------------------------------
datFile = os.path.join(
    os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat"
)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
predictor = dlib.shape_predictor(datFile)

# ------------------------------------------------------------------
# DeepFace (build once, guard with lock) ---------------------------
# ------------------------------------------------------------------
_TF_LOCK = threading.Lock()

_HAS_MODEL_KW = "model" in inspect.signature(DeepFace.represent).parameters
if _HAS_MODEL_KW:                         # DeepFace 0.0.46-0.0.92
    _FACENET_MODEL = DeepFace.build_model("Facenet")
else:                                     # ≤0.0.45 or ≥0.0.93
    _FACENET_MODEL = None                 # DeepFace will use its own cache

# ------------------------------------------------------------------
# Face helpers ------------------------------------------------------
# ------------------------------------------------------------------
def detect_faces(img: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """Return list of (x, y, w, h) rectangles for each detected face."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )


def align_face(img: np.ndarray, face: Tuple[int, int, int, int]) -> np.ndarray:
    """
    Affine-align a face to 256 × 256 BGR.  `face` = (x, y, w, h).
    This variant converts coordinates to plain Python int so
    cv2.getRotationMatrix2D never raises “Can't parse 'center'”.
    """
    x, y, w, h = map(int, face)
    rect = dlib.rectangle(x, y, x + w, y + h)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    land = predictor(gray, rect)
    pts  = np.array([(land.part(i).x, land.part(i).y)
                     for i in range(land.num_parts)])

    # eye centres ---------------------------------------------------
    le = pts[[36, 37, 38, 39, 40, 41]].mean(axis=0)
    re = pts[[42, 43, 44, 45, 46, 47]].mean(axis=0)

    # convert to native int to satisfy OpenCV
    le_x, le_y = map(int, le)
    re_x, re_y = map(int, re)

    dY, dX = re_y - le_y, re_x - le_x
    angle  = np.degrees(np.arctan2(dY, dX))
    dist   = np.hypot(dX, dY)

    out_w = out_h = 256
    desired_dist = out_w * 0.27
    scale = desired_dist / dist if dist else 1.0  # avoid /0

    eyes_c = (int((le_x + re_x) // 2), int((le_y + re_y) // 2))

    M = cv2.getRotationMatrix2D(eyes_c, float(angle), float(scale))
    M[0, 2] += out_w * 0.5 - eyes_c[0]
    M[1, 2] += out_h * 0.3 - eyes_c[1]

    return cv2.warpAffine(img, M, (out_w, out_h), flags=cv2.INTER_CUBIC)


# ------------------------------------------------------------------
# Feature extraction -----------------------------------------------
# ------------------------------------------------------------------
def _prepare_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """Validate & convert BGR → RGB uint8 contiguous array."""
    if img_bgr is None or img_bgr.size == 0:
        raise ValueError("Empty image passed to extract_features()")

    if img_bgr.dtype != np.uint8:
        img_bgr = np.clip(img_bgr, 0, 255).astype("uint8")

    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return np.ascontiguousarray(rgb)


def extract_features(bgr_face: np.ndarray) -> List[Dict[str, Any]]:
    """
    Return [{'embedding': 128-D np.ndarray}] for an aligned BGR face.
    Thread-safe and DeepFace-version-agnostic.
    """
    rgb = _prepare_rgb(bgr_face)

    with _TF_LOCK:
        if _HAS_MODEL_KW:                   # classic API with `model=`
            return DeepFace.represent(
                img_path=rgb,
                model=_FACENET_MODEL,
                detector_backend="skip",
                enforce_detection=False,
                align=False,                # ← disable extra alignment
            )
        else:                               # new / old API without `model`
            return DeepFace.represent(
                img_path=rgb,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False,
                align=False,                # ← disable extra alignment
            )

# ------------------------------------------------------------------
# Face-to-face matching --------------------------------------------
# ------------------------------------------------------------------
def match_face(
    embedding: np.ndarray,
    database: Dict[str, np.ndarray],
    thresh: float = 0.50,
) -> Optional[str]:
    """
    Return the best matching name (cosine distance < `thresh`) or None.
    """
    best_name, best_dist = None, 10.0
    for name, db_emb in database.items():
        dist = cosine(embedding, db_emb)
        if dist < best_dist:
            best_name, best_dist = name, dist
    return best_name if best_dist < thresh else None
