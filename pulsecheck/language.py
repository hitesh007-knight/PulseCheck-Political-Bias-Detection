"""Language detection and translation for multilingual support."""

from __future__ import annotations

from typing import Dict, List, Optional

# ISO-639-1 code → human-readable name (common languages)
LANGUAGE_NAMES: Dict[str, str] = {
    "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French",
    "de": "German", "pt": "Portuguese", "ru": "Russian", "zh-cn": "Chinese",
    "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "it": "Italian",
    "nl": "Dutch", "tr": "Turkish", "pl": "Polish", "uk": "Ukrainian",
    "sv": "Swedish", "da": "Danish", "no": "Norwegian", "fi": "Finnish",
    "el": "Greek", "cs": "Czech", "ro": "Romanian", "hu": "Hungarian",
    "th": "Thai", "vi": "Vietnamese", "id": "Indonesian", "ms": "Malay",
    "ta": "Tamil", "te": "Telugu", "bn": "Bengali", "mr": "Marathi",
    "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam", "pa": "Punjabi",
    "ur": "Urdu", "fa": "Persian", "he": "Hebrew", "sw": "Swahili",
}

# Native script names for display in the UI
NATIVE_NAMES: Dict[str, str] = {
    "hi": "हिन्दी", "ar": "العربية", "zh-cn": "中文", "ja": "日本語",
    "ko": "한국어", "ru": "Русский", "uk": "Українська", "el": "Ελληνικά",
    "th": "ไทย", "ta": "தமிழ்", "te": "తెలుగు", "bn": "বাংলা",
    "mr": "मराठी", "gu": "ગુજરાતી", "kn": "ಕನ್ನಡ", "ml": "മലയാളം",
    "pa": "ਪੰਜਾਬੀ", "ur": "اردو", "fa": "فارسی", "he": "עברית",
}

# Flag emojis keyed by language code (approximate – maps to country)
LANG_FLAGS: Dict[str, str] = {
    "en": "🇺🇸", "hi": "🇮🇳", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪",
    "pt": "🇧🇷", "ru": "🇷🇺", "zh-cn": "🇨🇳", "ja": "🇯🇵", "ko": "🇰🇷",
    "ar": "🇸🇦", "it": "🇮🇹", "nl": "🇳🇱", "tr": "🇹🇷", "pl": "🇵🇱",
    "uk": "🇺🇦", "sv": "🇸🇪", "da": "🇩🇰", "no": "🇳🇴", "fi": "🇫🇮",
    "el": "🇬🇷", "cs": "🇨🇿", "ro": "🇷🇴", "hu": "🇭🇺", "th": "🇹🇭",
    "vi": "🇻🇳", "id": "🇮🇩", "ms": "🇲🇾", "ta": "🇮🇳", "te": "🇮🇳",
    "bn": "🇧🇩", "mr": "🇮🇳", "gu": "🇮🇳", "kn": "🇮🇳", "ml": "🇮🇳",
    "pa": "🇮🇳", "ur": "🇵🇰", "fa": "🇮🇷", "he": "🇮🇱", "sw": "🇰🇪",
}


def get_supported_languages() -> List[Dict[str, str]]:
    """
    Return the list of languages supported for detection & translation.

    Each entry is a dict with:
      - 'code': ISO-639-1 language code
      - 'name': English name
      - 'native_name': Name in native script (if available)
      - 'flag': Emoji flag
    """
    langs = []
    for code, name in sorted(LANGUAGE_NAMES.items(), key=lambda x: x[1]):
        langs.append({
            "code": code,
            "name": name,
            "native_name": NATIVE_NAMES.get(code, name),
            "flag": LANG_FLAGS.get(code, "🌍"),
        })
    return langs


def detect_language(text: str) -> Dict[str, object]:
    """
    Detect the language of the given text.

    Returns dict with:
      - 'code': ISO-639-1 language code (e.g. 'en', 'hi', 'fr')
      - 'name': Human-readable language name
      - 'native_name': Name in native script
      - 'flag': Emoji flag
      - 'confidence': Detection confidence ('high' / 'medium' / 'low')
      - 'confidence_score': Numeric confidence (0-1)
    """
    try:
        from langdetect import detect_langs
        results = detect_langs(text[:3000])  # First 3000 chars is enough
        if not results:
            return _default_lang_info()

        top = results[0]
        code = str(top.lang)
        prob = float(top.prob)
        confidence = "high" if prob > 0.8 else ("medium" if prob > 0.5 else "low")

        return {
            "code": code,
            "name": LANGUAGE_NAMES.get(code, code.upper()),
            "native_name": NATIVE_NAMES.get(code, LANGUAGE_NAMES.get(code, code.upper())),
            "flag": LANG_FLAGS.get(code, "🌍"),
            "confidence": confidence,
            "confidence_score": prob,
        }
    except Exception:
        return _default_lang_info()


def _default_lang_info() -> Dict[str, object]:
    """Return default English language info (fallback)."""
    return {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "flag": "🇺🇸",
        "confidence": "low",
        "confidence_score": 0.0,
    }


def translate_to_english(text: str, source_lang: str = "auto") -> Dict[str, object]:
    """
    Translate text to English using Google Translate (via deep-translator).

    Args:
        text: Text to translate.
        source_lang: Source language code, or 'auto' for auto-detect.

    Returns dict with:
      - 'translated_text': The English translation
      - 'source_lang': Detected/provided source language code
      - 'is_translated': Whether translation was actually performed
    """
    # If source is "auto", detect first
    if source_lang == "auto":
        lang_info = detect_language(text)
        source_lang = lang_info["code"]

    if source_lang == "en":
        return {
            "translated_text": text,
            "source_lang": "en",
            "is_translated": False,
        }

    try:
        from deep_translator import GoogleTranslator

        # Google Translate has a ~5000 char limit per request; chunk if needed
        max_chunk = 4500
        if len(text) <= max_chunk:
            translated = GoogleTranslator(source=source_lang, target="en").translate(text)
        else:
            # Translate in chunks, splitting on sentence boundaries
            chunks = _split_into_chunks(text, max_chunk)
            translated_parts = []
            translator = GoogleTranslator(source=source_lang, target="en")
            for chunk in chunks:
                part = translator.translate(chunk)
                if part:
                    translated_parts.append(part)
            translated = " ".join(translated_parts)

        return {
            "translated_text": translated or text,
            "source_lang": source_lang,
            "is_translated": True,
        }
    except Exception as e:
        # Translation failed — fall back to original text
        return {
            "translated_text": text,
            "source_lang": source_lang,
            "is_translated": False,
            "error": str(e),
        }


def translate_short_text(text: str, source_lang: str = "auto") -> str:
    """
    Translate a short piece of text (headline, keyword) to English.

    Returns the translated string, or the original if translation fails
    or the text is already English.
    """
    if not text or not text.strip():
        return text

    if source_lang == "auto":
        lang_info = detect_language(text)
        source_lang = lang_info["code"]

    if source_lang == "en":
        return text

    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source=source_lang, target="en").translate(text)
        return translated or text
    except Exception:
        return text


def _split_into_chunks(text: str, max_len: int) -> list[str]:
    """Split text into chunks at sentence boundaries."""
    import re

    sentences = re.split(r'(?<=[.!?।।])\s+', text)
    chunks: list[str] = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) + 1 > max_len and current:
            chunks.append(current.strip())
            current = sent
        else:
            current = current + " " + sent if current else sent

    if current:
        chunks.append(current.strip())

    return chunks if chunks else [text[:max_len]]
