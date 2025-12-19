"""Predict political bias using pre-trained model."""

import numpy as np

from pulsecheck.artifacts import load_artifacts


def predict_bias(text: str) -> dict:
    """
    Predict bias label and confidence score.
    Returns dict with 'label' (left/center/right) and 'confidence' (0-1).
    """
    vectorizer, classifier, label_encoder = load_artifacts()
    
    # Transform text
    X = vectorizer.transform([text])
    
    # Predict
    prediction = classifier.predict(X)[0]
    
    # Get confidence from decision function (distance from boundary)
    decision = classifier.decision_function(X)[0]
    # Normalize to 0-1 range using softmax-like approach
    exp_decision = np.exp(decision - np.max(decision))
    probabilities = exp_decision / np.sum(exp_decision)
    confidence = float(np.max(probabilities))
    
    # Get label
    label = label_encoder.inverse_transform([prediction])[0]
    
    return {"label": label, "confidence": confidence}
