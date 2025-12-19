"""Sentiment and subjectivity analysis using TextBlob."""

from textblob import TextBlob


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment and subjectivity.
    Returns dict with 'sentiment' (positive/negative/neutral) and 'subjectivity' (0-1).
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Classify sentiment
    if polarity > 0.1:
        sentiment_label = "positive"
    elif polarity < -0.1:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"
    
    return {
        "sentiment": sentiment_label,
        "polarity": float(polarity),
        "subjectivity": float(subjectivity),
    }

