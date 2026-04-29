"""Sentiment and subjectivity analysis using TextBlob."""

from typing import Dict

from textblob import TextBlob


def analyze_sentiment(text: str, language_code: str = "en") -> Dict[str, float | str]:
    """
    Analyze sentiment and subjectivity.

    The analysis runs on English text (the pipeline translates before
    calling this function).  The *language_code* parameter is accepted
    for future use and for graceful fallback: if the text couldn't be
    translated and the language isn't English, we return a neutral
    default with a ``sentiment_fallback`` flag.

    Returns dict with 'sentiment' (positive/negative/neutral),
    'polarity', 'subjectivity', and optionally 'sentiment_fallback'.
    """
    try:
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
    except Exception:
        # Graceful fallback — return neutral defaults so the rest of the
        # pipeline doesn't break.
        return {
            "sentiment": "neutral",
            "polarity": 0.0,
            "subjectivity": 0.0,
            "sentiment_fallback": True,
        }
