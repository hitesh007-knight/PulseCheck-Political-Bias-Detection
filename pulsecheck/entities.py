"""Extract named entities (people, organizations, places) from text."""

try:
    import spacy
    from spacy import displacy
    
    # Try to load model, fallback to blank if not available
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
except ImportError:
    nlp = None


def extract_entities(text: str) -> dict:
    """
    Extract named entities using spaCy.
    Returns dict with 'people', 'organizations', 'places' lists.
    """
    if nlp is None:
        return {"people": [], "organizations": [], "places": []}
    
    doc = nlp(text[:100000])  # Limit length for performance
    
    people = []
    organizations = []
    places = []
    
    for ent in doc.ents:
        if ent.label_ in ["PERSON"]:
            if ent.text not in people:
                people.append(ent.text)
        elif ent.label_ in ["ORG", "NORP"]:
            if ent.text not in organizations:
                organizations.append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            if ent.text not in places:
                places.append(ent.text)
    
    return {
        "people": people[:10],  # Limit to top 10
        "organizations": organizations[:10],
        "places": places[:10],
    }

