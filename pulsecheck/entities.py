"""Extract named entities (people, organizations, places) from text."""

from typing import Dict, List

# Use HuggingFace transformers NER pipeline (works on Python 3.14, unlike spaCy)
# Uses multilingual model for multi-language support
_ner_pipeline = None


def _get_ner_pipeline():
    """Lazy-load the multilingual NER pipeline on first use."""
    global _ner_pipeline
    if _ner_pipeline is None:
        from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

        # Multilingual NER model — supports 10+ languages including
        # English, Hindi, Spanish, French, German, Chinese, Arabic, etc.
        model_name = "Davlan/bert-base-multilingual-cased-ner-hrl"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTokenClassification.from_pretrained(model_name)
            _ner_pipeline = pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                aggregation_strategy="max",
            )
        except Exception:
            # Fall back to English-only model if multilingual fails to download
            tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
            model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
            _ner_pipeline = pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                aggregation_strategy="max",
            )
    return _ner_pipeline


# Mapping from NER entity labels to our categories
# Both multilingual and English models use these labels
_LABEL_MAP = {
    "PER": "people",
    "ORG": "organizations",
    "LOC": "places",
}


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract named entities using a multilingual transformer NER model.
    Supports English, Hindi, Spanish, French, German, Chinese, Arabic, and more.
    Returns dict with 'people', 'organizations', 'places' lists.
    """
    result: Dict[str, List[str]] = {
        "people": [],
        "organizations": [],
        "places": [],
    }

    try:
        ner = _get_ner_pipeline()
    except Exception:
        # Model download or load failed – return empty gracefully
        return result

    # Transformer models have a max token length; process first ~5000 chars
    chunk = text[:5000]

    try:
        entities = ner(chunk)
    except Exception:
        return result

    # De-duplicate while preserving order
    seen: Dict[str, set] = {"people": set(), "organizations": set(), "places": set()}

    for ent in entities:
        label = ent.get("entity_group", "")
        word = ent.get("word", "").strip()
        category = _LABEL_MAP.get(label)

        if not category or not word:
            continue

        # Clean up sub-word artefacts produced by BERT tokenizer
        word = word.replace(" ##", "").replace("##", "")

        # Skip garbage fragments (single char, starts with punctuation, etc.)
        if len(word) < 2 or not word[0].isalnum():
            continue

        # Normalize whitespace
        word = " ".join(word.split())

        lower_word = word.lower()
        if lower_word not in seen[category]:
            seen[category].add(lower_word)
            result[category].append(word)

    # Limit to top 10 each
    for key in result:
        result[key] = result[key][:10]

    return result
