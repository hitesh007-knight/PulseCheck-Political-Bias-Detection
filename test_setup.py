"""Quick test to check if everything is set up correctly."""

print("Checking PulseCheck Setup...\n")

# Check Python
import sys
print(f"[OK] Python {sys.version.split()[0]}")

# Check basic packages
try:
    import pandas
    print("[OK] pandas")
except ImportError:
    print("[MISSING] pandas - Run: pip install pandas")

try:
    import sklearn
    print("[OK] scikit-learn")
except ImportError:
    print("[MISSING] scikit-learn - Run: pip install scikit-learn")

try:
    import flask
    print("[OK] flask")
except ImportError:
    print("[MISSING] flask - Run: pip install flask flask-cors")

try:
    import streamlit
    print("[OK] streamlit")
except ImportError:
    print("[MISSING] streamlit - Run: pip install streamlit")

try:
    from textblob import TextBlob
    print("[OK] textblob")
except ImportError:
    print("[MISSING] textblob - Run: pip install textblob")

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        print("[OK] spacy + en_core_web_sm model")
    except OSError:
        print("[WARNING]  spacy installed but model missing - Run: python -m spacy download en_core_web_sm")
except ImportError:
    print("[MISSING] spacy - Run: pip install spacy")

try:
    import plotly
    print("[OK] plotly")
except ImportError:
    print("[MISSING] plotly - Run: pip install plotly")

try:
    import trafilatura
    print("[OK] trafilatura")
except ImportError:
    print("[MISSING] trafilatura - Run: pip install trafilatura")

# Check dataset
import os
if os.path.exists("improved_political_dataset.csv"):
    print("[OK] Dataset file found")
else:
    print("[MISSING] Dataset file missing: improved_political_dataset.csv")

# Check artifacts
if os.path.exists("artifacts/vectorizer.pkl"):
    print("[OK] Model artifacts found (model already trained)")
else:
    print("[WARNING]  Model artifacts not found - Run: python train.py")

print("\n" + "="*50)
print("If all checks pass, you're ready to run!")
print("="*50)

