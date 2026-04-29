"""Main pipeline for article analysis."""

from __future__ import annotations

from typing import Optional

from pulsecheck.bias_predictor import predict_bias
from pulsecheck.language import detect_language, translate_to_english, translate_short_text
from pulsecheck.scraper import scrape_article
from pulsecheck.sentiment import analyze_sentiment
from pulsecheck.summarizer import summarize
from pulsecheck.topic_modeler import extract_topics


def analyze(
    url: Optional[str] = None,
    text: Optional[str] = None,
    summarize_article: bool = False,
    bias_model: str = "svm",
    language_override: Optional[str] = None,
) -> dict:
    """
    Full article analysis: scrape (or accept raw text), detect language,
    translate, predict bias, sentiment, topics, entities.

    Args:
        url: News article URL to analyze (provide url OR text).
        text: Raw article text to analyze directly (provide url OR text).
        summarize_article: Whether to include article summary.
        bias_model: "svm" or "transformer" (BERT/RoBERTa).
        language_override: If set, skip auto-detection and use this
            ISO-639-1 code (e.g. "hi", "fr", "ar").

    Returns:
        Comprehensive dict with all analysis results.
    """
    # ── 1. Get article text ──────────────────────────────────────────
    if text:
        # Direct text input (pasted article)
        original_text = text.strip()
        headline = ""
        source = "Direct Input"
        html_language = None
    elif url:
        article = scrape_article(url)
        original_text = article["text"]
        headline = article.get("headline", "")
        source = article.get("source", "Unknown")
        html_language = article.get("html_language")
    else:
        raise ValueError("Either 'url' or 'text' must be provided.")

    # ── 2. Language detection ────────────────────────────────────────
    if language_override:
        from pulsecheck.language import LANGUAGE_NAMES, NATIVE_NAMES, LANG_FLAGS
        detected_lang = language_override
        lang_info = {
            "code": language_override,
            "name": LANGUAGE_NAMES.get(language_override, language_override.upper()),
            "native_name": NATIVE_NAMES.get(
                language_override,
                LANGUAGE_NAMES.get(language_override, language_override.upper()),
            ),
            "flag": LANG_FLAGS.get(language_override, "🌍"),
            "confidence": "manual",
            "confidence_score": 1.0,
        }
    else:
        lang_info = detect_language(original_text)
        detected_lang = lang_info["code"]

        # Use HTML language hint as a tie-breaker when confidence is low
        if html_language and lang_info["confidence"] == "low":
            # Trust the HTML tag instead
            detected_lang = html_language
            lang_info["code"] = html_language
            from pulsecheck.language import LANGUAGE_NAMES, NATIVE_NAMES, LANG_FLAGS
            lang_info["name"] = LANGUAGE_NAMES.get(html_language, html_language.upper())
            lang_info["native_name"] = NATIVE_NAMES.get(
                html_language,
                LANGUAGE_NAMES.get(html_language, html_language.upper()),
            )
            lang_info["flag"] = LANG_FLAGS.get(html_language, "🌍")

    # ── 3. Translation ───────────────────────────────────────────────
    if detected_lang != "en":
        translation = translate_to_english(original_text, source_lang=detected_lang)
        analysis_text = translation["translated_text"]
        is_translated = translation["is_translated"]
    else:
        analysis_text = original_text
        is_translated = False

    # Translate headline too
    original_headline = headline
    if detected_lang != "en" and headline:
        headline = translate_short_text(headline, source_lang=detected_lang)

    # ── 4. Bias prediction (always on English text) ──────────────────
    if bias_model.lower() in {"bert", "roberta", "transformer"}:
        # Lazy import to avoid triggering full package import chain
        from pulsecheck.transformer_bias_predictor import predict_bias_transformer
        bias_result = predict_bias_transformer(analysis_text)
    else:
        bias_result = predict_bias(analysis_text)

    # ── 5. Sentiment analysis (on English text for accuracy) ─────────
    sentiment_result = analyze_sentiment(analysis_text, language_code=detected_lang)

    # ── 6. Topics (on English text; pass lang code for stop words) ───
    topics = extract_topics(
        analysis_text,
        language_code="en" if is_translated else detected_lang,
    )

    # ── 7. Named entities (on original text — multilingual NER) ──────
    from pulsecheck.entities import extract_entities
    entities = extract_entities(original_text)

    # ── 8. Build result dictionary ───────────────────────────────────
    result = {
        "bias": bias_result["label"],
        "confidence": bias_result["confidence"],
        "bias_model": bias_result.get("model", bias_model),
        "bias_probabilities": bias_result.get("probabilities"),
        "sentiment": sentiment_result["sentiment"],
        "polarity": sentiment_result["polarity"],
        "subjectivity": sentiment_result["subjectivity"],
        "sentiment_fallback": sentiment_result.get("sentiment_fallback", False),
        "topics": topics,
        "entities": entities,
        "source": source,
        "headline": headline,
        "original_headline": original_headline,
        "text": original_text,
        # Language info
        "language": lang_info["name"],
        "language_code": detected_lang,
        "language_native_name": lang_info.get("native_name", lang_info["name"]),
        "language_flag": lang_info.get("flag", "🌍"),
        "language_confidence": lang_info.get("confidence", "low"),
        "language_confidence_score": lang_info.get("confidence_score", 0.0),
        "is_translated": is_translated,
    }

    # Add translated text if translation was performed
    if is_translated:
        result["translated_text"] = analysis_text

    # Add summary if requested (on English text)
    if summarize_article:
        result["summary"] = summarize(analysis_text)

    return result
