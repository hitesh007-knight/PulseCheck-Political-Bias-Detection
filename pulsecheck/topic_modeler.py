"""Extract topics from article text using LDA."""

import re
from collections import Counter

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def extract_topics(text: str, num_topics: int = 3, num_words: int = 5) -> list:
    """
    Extract topics using sklearn LDA.
    Returns list of dicts with 'topic_id' and 'keywords'.
    """
    # Simple preprocessing
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    if len(words) < 20:
        return []
    
    # Create document
    doc = ' '.join(words)
    
    # Vectorize
    vectorizer = CountVectorizer(max_features=50, stop_words='english', ngram_range=(1, 2))
    try:
        X = vectorizer.fit_transform([doc])
        
        if X.shape[1] < num_topics:
            return []
        
        # Train LDA
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42, max_iter=10)
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
