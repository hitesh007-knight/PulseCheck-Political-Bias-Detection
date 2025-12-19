"""Load pre-trained model artifacts."""

import joblib
from pathlib import Path

from pulsecheck.config import CLASSIFIER_FILE, LABEL_ENCODER_FILE, VECTORIZER_FILE


def load_artifacts():
    """Load vectorizer, classifier, and label encoder."""
    if not VECTORIZER_FILE.exists():
        raise FileNotFoundError(f"Artifacts not found. Run 'python train.py' first.")
    
    vectorizer = joblib.load(VECTORIZER_FILE)
    classifier = joblib.load(CLASSIFIER_FILE)
    label_encoder = joblib.load(LABEL_ENCODER_FILE)
    
    return vectorizer, classifier, label_encoder
