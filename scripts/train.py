"""Train bias classifier on the political dataset.

Usage (run from project root):
    python scripts/train.py
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so pulsecheck is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from pulsecheck.config import MODELS_DIR, CLASSIFIER_FILE, LABEL_ENCODER_FILE, VECTORIZER_FILE, DATASET_FILE

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATASET_FILE)

# Use Text column and Bias column
X = df["Text"].values
y = df["Bias"].str.lower().str.strip().values

print(f"Dataset shape: {len(X)} samples")
print(f"Bias distribution:\n{pd.Series(y).value_counts()}")

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train
print("\nTraining model...")
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)

classifier = LinearSVC(random_state=42, max_iter=2000)
classifier.fit(X_train_vec, y_train)

# Evaluate
X_test_vec = vectorizer.transform(X_test)
y_pred = classifier.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nTest Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# Save artifacts
MODELS_DIR.mkdir(exist_ok=True)
joblib.dump(vectorizer, VECTORIZER_FILE)
joblib.dump(classifier, CLASSIFIER_FILE)
joblib.dump(encoder, LABEL_ENCODER_FILE)

print(f"\nModel artifacts saved to {MODELS_DIR.resolve()}/")
