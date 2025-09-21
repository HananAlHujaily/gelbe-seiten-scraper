"""
ai_enhancer.py – AI/NLP fallback extraction for GelbeSeiten Scraper

Provides functions to extract business entity information (name, address, phone)
from raw or unstructured text using spaCy (German NER) and regex.

Functions:
- ai_extract_entities: Extracts name, address, and phone from a text block.
- _load_spacy: Loads the German spaCy model (de_core_news_sm).

Usage:
    from ai_enhancer import ai_extract_entities
    result = ai_extract_entities(text_block)

Dependencies:
    - spaCy (de_core_news_sm)
    - re (regex)

Author: 3D Padelt GmbH Test Assignment
Date: 2025-09-21
"""

import re

def _load_spacy():
    """
    Load the German spaCy model for Named Entity Recognition.

    Returns:
        spacy.lang.de.German | None: Loaded spaCy model or None if unavailable.
    """
    try:
        import spacy
        return spacy.load("de_core_news_sm")
    except Exception:
        return None

NLP = _load_spacy()

PHONE_REGEX = re.compile(r"(?:\+49\s?|0)\d{2,4}[\s/-]?\d{2,}([\s/-]?\d+)*")

def ai_extract_entities(text_block: str):
    """
    AI/NLP fallback extractor. Uses spaCy + regex for name, address, phone.

    Args:
        text_block (str): Raw or semi-structured business info.

    Returns:
        dict: {
            "ai_name": str | None,
            "ai_address": str | None,
            "ai_phone": str | None
        }
    """
    name = None
    address = None
    phone = None

    # NER: company name
    if NLP is not None:
        doc = NLP(text_block)
        for ent in doc.ents:
            if ent.label_ == "ORG" and not name:
                name = ent.text

    # Split lines
    lines = [l.strip() for l in text_block.splitlines() if l.strip()]

    # Fallback: first line as name
    if not name and lines:
        name = lines[0]

    # Address: find postal code line
    for line in lines:
        if re.search(r"\b\d{5}\b", line):
            address = line
            break

    # Phone: regex
    match = PHONE_REGEX.search(text_block)
    if match:
        phone = match.group(0)

    return {"ai_name": name, "ai_address": address, "ai_phone": phone}
