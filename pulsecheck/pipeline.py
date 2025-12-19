"""Main pipeline for article analysis."""

from pulsecheck.bias_predictor import predict_bias
from pulsecheck.entities import extract_entities
from pulsecheck.scraper import scrape_article
from pulsecheck.sentiment import analyze_sentiment
from pulsecheck.summarizer import summarize
from pulsecheck.topic_modeler import extract_topics


def analyze(url: str, summarize_article: bool = False) -> dict:
    """
    Full article analysis: scrape, predict bias, sentiment, topics, entities.
    Returns comprehensive dict with all analysis results.
    """
    # Scrape
    article = scrape_article(url)
    
    # Predict bias
    bias_result = predict_bias(article["text"])
    
    # Sentiment analysis
    sentiment_result = analyze_sentiment(article["text"])
    
    # Extract topics
    topics = extract_topics(article["text"])
    
    # Extract entities
    entities = extract_entities(article["text"])
    
    result = {
        "bias": bias_result["label"],
        "confidence": bias_result["confidence"],
        "sentiment": sentiment_result["sentiment"],
        "polarity": sentiment_result["polarity"],
        "subjectivity": sentiment_result["subjectivity"],
        "topics": topics,
        "entities": entities,
        "source": article["source"],
        "headline": article["headline"],
        "text": article["text"],
    }
    
    if summarize_article:
        result["summary"] = summarize(article["text"])
    
    return result
