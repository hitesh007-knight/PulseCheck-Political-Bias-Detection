"""Simple extractive summarization."""


def summarize(text: str, max_sentences: int = 3) -> str:
    """
    Simple sentence-based summarization.
    Returns top sentences by length and position.
    """
    import re
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return text[:200] + "..." if len(text) > 200 else text
    
    # Score by length and position
    scored = []
    for i, sent in enumerate(sentences):
        score = len(sent) * (1.0 / (i + 1))  # Prefer longer, earlier sentences
        scored.append((score, sent))
    
    scored.sort(reverse=True)
    top_sentences = [sent for _, sent in scored[:max_sentences]]
    
    return ". ".join(top_sentences) + "."
