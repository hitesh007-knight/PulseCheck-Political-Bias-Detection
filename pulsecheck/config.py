"""Configuration paths for model artifacts."""

from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")
VECTORIZER_FILE = ARTIFACTS_DIR / "vectorizer.pkl"
CLASSIFIER_FILE = ARTIFACTS_DIR / "classifier.pkl"
LABEL_ENCODER_FILE = ARTIFACTS_DIR / "label_encoder.pkl"
