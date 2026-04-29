"""Fine-tune a transformer (RoBERTa/BERT) for political bias classification.

Prototype-friendly trainer:
- By default trains on a small subset for quick iteration
- Can be scaled up for final training

Usage (run from project root):
    python scripts/train_transformer.py
    python scripts/train_transformer.py --train_samples 12000 --eval_samples 3000 --epochs 1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the project root is on sys.path so pulsecheck is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

from pulsecheck.config import TRANSFORMER_DIR, DATASET_FILE


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train transformer model for bias detection")
    p.add_argument("--model_name", default="distilroberta-base", help="HF model checkpoint")
    p.add_argument(
        "--text_column",
        default="ImprovedText",
        help="Dataset text column (recommended: ImprovedText; fallback: Text)",
    )
    p.add_argument("--csv_path", default=str(DATASET_FILE))
    p.add_argument("--output_dir", default=str(TRANSFORMER_DIR))
    p.add_argument("--max_length", type=int, default=256)
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--train_samples", type=int, default=12000, help="Prototype mode subset size")
    p.add_argument("--eval_samples", type=int, default=3000)
    p.add_argument("--batch_size", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    try:
        import torch
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            DataCollatorWithPadding,
            Trainer,
            TrainingArguments,
        )
        from datasets import Dataset
    except ImportError as e:
        print(f"ERROR: Transformers dependencies not installed: {e}")
        print("Install with: pip install transformers torch accelerate datasets")
        return

    # Set random seeds
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    # Load dataset
    print(f"Loading dataset from {args.csv_path}...")
    df = pd.read_csv(args.csv_path)

    # Use ImprovedText if available, else Text
    text_col = args.text_column if args.text_column in df.columns else "Text"
    if text_col not in df.columns:
        raise ValueError(f"Column '{text_col}' not found in dataset")

    X = df[text_col].fillna("").astype(str).values
    y = df["Bias"].str.lower().str.strip().values

    print(f"Dataset shape: {len(X)} samples")
    print(f"Bias distribution:\n{pd.Series(y).value_counts()}")

    # Label mapping
    label_map = {"left": 0, "center": 1, "right": 2}
    y_encoded = np.array([label_map[label] for label in y])

    # Subset for prototype mode
    if args.train_samples > 0 and len(X) > args.train_samples:
        print(f"\nPrototype mode: Using {args.train_samples} training samples")
        indices = np.random.choice(len(X), args.train_samples + args.eval_samples, replace=False)
        X_subset = X[indices]
        y_subset = y_encoded[indices]
    else:
        X_subset = X
        y_subset = y_encoded

    # Split
    split_idx = len(X_subset) - args.eval_samples
    X_train = X_subset[:split_idx]
    y_train = y_subset[:split_idx]
    X_eval = X_subset[split_idx:]
    y_eval = y_subset[split_idx:]

    print(f"\nTrain samples: {len(X_train)}")
    print(f"Eval samples: {len(X_eval)}")

    # Load tokenizer and model
    print(f"\nLoading model: {args.model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name, num_labels=3
    )

    # Tokenize
    def tokenize(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=args.max_length,
            padding="max_length",
        )

    train_dataset = Dataset.from_dict({"text": X_train.tolist(), "label": y_train.tolist()})
    eval_dataset = Dataset.from_dict({"text": X_eval.tolist(), "label": y_eval.tolist()})

    train_dataset = train_dataset.map(tokenize, batched=True)
    eval_dataset = eval_dataset.map(tokenize, batched=True)

    # Training arguments
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.lr,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        logging_steps=50,
        save_total_limit=1,
        seed=args.seed,
    )

    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )

    # Train
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)
    trainer.train()

    # Evaluate
    print("\n" + "=" * 60)
    print("Evaluating...")
    print("=" * 60)
    eval_results = trainer.evaluate()
    print(f"\nEval Accuracy: {eval_results.get('eval_accuracy', 0):.4f}")

    # Save final model
    print(f"\nSaving model to {output_dir.resolve()}...")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)

    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Model saved to: {output_dir.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
