"""Scrape and extract text from news article URLs."""

from typing import Dict, Optional
from urllib.parse import urlparse

import trafilatura


def scrape_article(url: str) -> Dict[str, str]:
    """
    Scrape article text and detect source from URL.
    Returns dict with 'text', 'headline', 'source', and 'html_language'.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError(f"Failed to fetch content from {url}")
        
        # Extract text – set target_language=None so trafilatura does NOT
        # discard non-English content.
        extracted = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_links=False,
            target_language=None,
        )
        if not extracted:
            raise ValueError(f"No text extracted from {url}")
        
        # Get headline and language hint from HTML metadata
        headline = ""
        html_language = None
        try:
            from trafilatura import extract_metadata
            meta = extract_metadata(downloaded)
            if meta:
                if meta.title:
                    headline = meta.title
                # trafilatura metadata may carry the page language
                if hasattr(meta, "language") and meta.language:
                    html_language = str(meta.language).lower().strip()
        except Exception:
            pass
        
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
            "html_language": html_language,
        }
    except Exception as e:
        raise ValueError(f"Scraping failed: {str(e)}")
