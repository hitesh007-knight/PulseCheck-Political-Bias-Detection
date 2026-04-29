"""Smoke test for transformer bias predictor.

Usage (run from project root):
    python tests/test_transformer_smoke.py

Prerequisites:
    python scripts/train_transformer.py --train_samples 12000 --eval_samples 3000 --epochs 1
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pulsecheck.config import TRANSFORMER_DIR

transformer_dir = TRANSFORMER_DIR


def check_model_files():
    """Check if required model files exist."""
    required_files = [
        "config.json",
        "pytorch_model.bin",  # or model.safetensors
        "tokenizer_config.json",
        "vocab.json",
    ]

    missing = []
    found = []

    for file in required_files:
        file_path = transformer_dir / file
        if file_path.exists():
            found.append(file)
        else:
            # Check for alternative names
            if file == "pytorch_model.bin":
                alt_files = ["model.safetensors", "pytorch_model.bin"]
                if any((transformer_dir / alt).exists() for alt in alt_files):
                    found.append("model weights")
                    continue
            missing.append(file)

    return found, missing


def main() -> None:
    """Test transformer model availability."""

    print("=" * 60)
    print("Transformer Model Smoke Test")
    print("=" * 60)

    # Check if directory exists
    if not transformer_dir.exists():
        print("\n[ERROR] Transformer model directory not found!")
        print(f"   Expected location: {transformer_dir.resolve()}")
        print("\n   Please train the model first:")
        print("   python scripts/train_transformer.py --train_samples 12000 --eval_samples 3000 --epochs 1")
        sys.exit(1)

    print(f"\n[OK] Model directory found: {transformer_dir.resolve()}")

    # Check for required files
    found, missing = check_model_files()

    if missing:
        print(f"\n[WARNING] Some model files are missing:")
        for file in missing:
            print(f"   - {file}")
        print("\n   The model may not be fully trained.")
        print("   Please run: python scripts/train_transformer.py")
        sys.exit(1)

    print(f"\n[OK] All required model files found!")
    print(f"   Found: {len(found)} files")

    # Try to import and test
    print("\n" + "=" * 60)
    print("Testing Model Import...")
    print("=" * 60)

    try:
        from pulsecheck.transformer_bias_predictor import predict_bias_transformer

        sample = (
            "The government announced a new policy proposal today, highlighting expected economic "
            "benefits while critics raised concerns about long-term impacts."
        )

        print(f"\n   Testing prediction on sample text...")
        result = predict_bias_transformer(sample)

        print("\n[OK] Prediction test passed!")
        print(f"\n   Sample text: {sample[:60]}...")
        print(f"   Predicted bias: {result['label'].upper()}")
        print(f"   Confidence: {result['confidence']:.2%}")
        if 'probabilities' in result:
            print(f"   Probabilities:")
            for label, prob in result['probabilities'].items():
                print(f"     - {label}: {prob:.2%}")

        print("\n" + "=" * 60)
        print("[OK] All tests passed! Transformer model is ready to use.")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
