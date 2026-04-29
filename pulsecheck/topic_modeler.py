"""Extract topics from article text using LDA."""

import re
from typing import List, Dict, Any

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Multilingual stop words — used when analysing non-English text that
# may not have been perfectly translated, or when running directly on
# the original text.
_MULTILINGUAL_STOP_WORDS: Dict[str, List[str]] = {
    "hi": [
        "और", "का", "के", "में", "है", "को", "से", "पर", "ने", "की",
        "एक", "यह", "नहीं", "कि", "भी", "इस", "हैं", "लिए", "था",
        "कर", "हो", "या", "अपने", "वह", "तो", "जो", "कुछ", "उन",
    ],
    "es": [
        "de", "la", "el", "en", "que", "los", "del", "las", "por",
        "con", "una", "para", "como", "más", "pero", "fue", "son",
        "este", "entre", "cuando", "muy", "sin", "sobre", "ser",
    ],
    "fr": [
        "de", "la", "le", "les", "des", "en", "un", "une", "est",
        "dans", "que", "qui", "par", "pour", "sur", "son", "pas",
        "plus", "avec", "au", "aux", "ce", "cette", "se", "sont",
    ],
    "de": [
        "der", "die", "und", "den", "von", "ist", "des", "ein",
        "mit", "auf", "für", "eine", "als", "auch", "nach", "wie",
        "dem", "nicht", "noch", "bei", "aus", "aber", "hat", "sich",
    ],
    "ar": [
        "في", "من", "على", "إلى", "أن", "هذا", "التي", "الذي",
        "عن", "هي", "هو", "مع", "كان", "لم", "بين", "ما",
        "أو", "إن", "قد", "ذلك", "بعد", "كل", "لا",
    ],
}


def _get_stop_words(language_code: str = "en"):
    """
    Return stop words suitable for the given language.

    For English we rely on sklearn's built-in list.  For other languages
    we return a custom list.  If the language isn't in our map we return
    ``None`` (no stop words filtering) rather than crashing.
    """
    if language_code == "en":
        return "english"
    return _MULTILINGUAL_STOP_WORDS.get(language_code)


def extract_topics(
    text: str,
    num_topics: int = 3,
    num_words: int = 5,
    language_code: str = "en",
) -> List[Dict[str, Any]]:
    """
    Extract topics using sklearn LDA.

    The *language_code* parameter selects the appropriate stop-word list.
    The tokeniser now uses a Unicode-aware pattern so it works on
    non-Latin scripts (Hindi Devanagari, Arabic, Chinese, etc.) as well
    as Latin.

    Returns list of dicts with 'topic_id' and 'keywords'.
    """
    # Unicode-aware tokenisation: match sequences of word characters
    # (letters + digits) of length ≥ 2 in any script.
    words = re.findall(r'\b\w{2,}\b', text.lower(), flags=re.UNICODE)

    if len(words) < 20:
        return []

    # Create document
    doc = ' '.join(words)

    # Pick stop words
    stop_words = _get_stop_words(language_code)

    # Vectorize
    try:
        vectorizer = CountVectorizer(
            max_features=50,
            stop_words=stop_words,
            ngram_range=(1, 2),
        )
        X = vectorizer.fit_transform([doc])

        if X.shape[1] < num_topics:
            return []

        # Train LDA
        lda = LatentDirichletAllocation(
            n_components=num_topics, random_state=42, max_iter=10
        )
        lda.fit(X)

        # Extract topics
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_id in range(num_topics):
            topic_weights = lda.components_[topic_id]
            top_indices = topic_weights.argsort()[-num_words:][::-1]
            keywords = [feature_names[i] for i in top_indices]
            topics.append({"topic_id": topic_id, "keywords": keywords})

        return topics
    except Exception:
        return []
