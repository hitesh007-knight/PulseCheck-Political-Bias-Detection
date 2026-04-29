"""Quick test to check if everything is set up correctly.

Usage (run from project root):
    python tests/test_setup.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("Checking PulseCheck Setup...\n")

# Check Python
print(f"[OK] Python {sys.version.split()[0]}")

# Check basic packages
for pkg_name, import_name, install_hint in [
    ("pandas", "pandas", "pip install pandas"),
    ("scikit-learn", "sklearn", "pip install scikit-learn"),
    ("flask", "flask", "pip install flask flask-cors"),
    ("streamlit", "streamlit", "pip install streamlit"),
    ("textblob", "textblob", "pip install textblob"),
    ("plotly", "plotly", "pip install plotly"),
    ("trafilatura", "trafilatura", "pip install trafilatura"),
    ("langdetect", "langdetect", "pip install langdetect"),
    ("deep-translator", "deep_translator", "pip install deep-translator"),
]:
    try:
        __import__(import_name)
        print(f"[OK] {pkg_name}")
    except ImportError:
        print(f"[MISSING] {pkg_name} - Run: {install_hint}")

# Check dataset
from pulsecheck.config import DATASET_FILE, MODELS_DIR

if DATASET_FILE.exists():
    print("[OK] Dataset file found")
else:
    print(f"[MISSING] Dataset file missing: {DATASET_FILE}")

# Check model artifacts
if (MODELS_DIR / "vectorizer.pkl").exists():
    print("[OK] SVM model artifacts found")
else:
    print("[WARNING] SVM model artifacts not found - Run: python scripts/train.py")

if (MODELS_DIR / "transformer").is_dir():
    print("[OK] Transformer model directory found")
else:
    print("[WARNING] Transformer model not found - Run: python scripts/setup_bert_model.py")

print("\n" + "=" * 50)
print("If all checks pass, you're ready to run!")
print("=" * 50)
