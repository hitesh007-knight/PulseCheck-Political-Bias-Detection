"""Configuration paths for model artifacts."""

from pathlib import Path

# Project root (parent of the pulsecheck package)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Trained model artifacts
MODELS_DIR = PROJECT_ROOT / "models"

# SVM model artifacts
VECTORIZER_FILE = MODELS_DIR / "vectorizer.pkl"
CLASSIFIER_FILE = MODELS_DIR / "classifier.pkl"
LABEL_ENCODER_FILE = MODELS_DIR / "label_encoder.pkl"

# Transformer (BERT/RoBERTa) artifacts (HuggingFace format)
TRANSFORMER_DIR = MODELS_DIR / "transformer"

# Training data
DATA_DIR = PROJECT_ROOT / "data"
DATASET_FILE = DATA_DIR / "improved_political_dataset.csv"
