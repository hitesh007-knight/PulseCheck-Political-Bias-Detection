"""Scrape and extract text from news article URLs."""

from urllib.parse import urlparse

import trafilatura


def scrape_article(url: str) -> dict:
    """
    Scrape article text and detect source from URL.
    Returns dict with 'text', 'headline', 'source'.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError(f"Failed to fetch content from {url}")
        
        extracted = trafilatura.extract(downloaded, include_comments=False, include_links=False)
        if not extracted:
            raise ValueError(f"No text extracted from {url}")
        
        # Get headline if available
        doc = trafilatura.extract(downloaded, output_format="xml", include_comments=False)
        headline = ""
        if doc:
            from trafilatura import extract_metadata
            meta = extract_metadata(doc)
            if meta and meta.title:
                headline = meta.title
        
        # Detect source from domain (better parsing)
        domain = urlparse(url).netloc
        domain = domain.replace("www.", "")
        parts = domain.split(".")
        # For domains like "edition.cnn.com", get "cnn" not "edition"
        # For domains like "www.bbc.com", get "bbc"
        if len(parts) >= 2:
            # Skip common subdomains
            skip_subdomains = ["edition", "www", "mobile", "m", "news", "www2"]
            if parts[0].lower() in skip_subdomains:
                source = parts[1].title()
            else:
                source = parts[0].title()
        else:
            source = parts[0].title()
        
        return {
            "text": extracted.strip(),
            "headline": headline,
            "source": source,
        }
    except Exception as e:
        raise ValueError(f"Scraping failed: {str(e)}")
