"""Quick setup to download pre-trained BERT model for demo.

Usage (run from project root):
    python scripts/setup_bert_model.py
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

from pulsecheck.config import TRANSFORMER_DIR

MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = TRANSFORMER_DIR

print(f"Downloading {MODEL_NAME}...")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Download and save tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.save_pretrained(str(OUTPUT_DIR))
print(f"✓ Tokenizer saved")

# Download and save model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
model.save_pretrained(str(OUTPUT_DIR))
print(f"✓ Model saved")

# Create a config file to identify the model
config_file = OUTPUT_DIR / "model_info.json"
config = {
    "base_model": MODEL_NAME,
    "num_labels": 3,
    "labels": ["left", "center", "right"],
    "model_type": "distilbert",
    "status": "pre-trained (not fine-tuned)",
    "note": "This is a pre-trained DistilBERT model. Fine-tune with your political bias dataset for better results."
}
with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print(f"✓ Model info saved")
print(f"\n✅ BERT model ready at: {OUTPUT_DIR}")
