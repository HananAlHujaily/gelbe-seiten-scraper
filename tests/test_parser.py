"""
test_parser.py – Unit tests for GelbeSeiten AI Scraper

This module contains tests for the HTML parser and AI entity extraction
used in the GelbeSeiten AI Scraper project.

Tests cover:
- Basic parsing of structured HTML business entries
- Handling of missing fields (e.g., phone number)
- AI fallback extraction using spaCy and regex
- Robustness against unstructured/raw HTML

Usage:
    pytest -s -q tests/test_parser.py

Author: 3D Padelt GmbH Test Assignment
Date: 2025-09-21
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from scraper import parse_page_discovery
from ai_enhancer import ai_extract_entities

# Sample HTML with two business entries, one missing a phone number
SAMPLE_HTML = """
<html><body>
  <article class="mod-Treffer">
    <h2>Bechtle GmbH IT-Systemhaus Köln</h2>
    <div class="mod-AdresseKompakt__adress-text">Schanzenstr. 41d, 51063 Köln</div>
    <a class="mod-TelefonnummerKompakt__phoneNumber" href="tel:0221310600">0221 31 06 00</a>
    <span class="mod-WebseiteKompakt__text" data-websitelink="https://www.bechtle.com"></span>
  </article>
  <article class="mod-Treffer">
    <h2>Example Without Phone</h2>
    <div class="mod-AdresseKompakt__adress-text">Musterstraße 1, 10115 Berlin</div>
  </article>
</body></html>
"""

# Raw HTML to test AI fallback (no structured tags)
RAW_HTML = """
<html><body>
  <article class="mod-Treffer">
    Super IT Service GmbH
    Musterstraße 99, 10115 Berlin
    Tel: 030 1234567
  </article>
</body></html>
"""


def test_parse_page_basic():
    """
    Test parsing a full entry with all fields present.

    Verifies that the parser correctly extracts name, address, phone, and website.
    """
    rows = parse_page_discovery(SAMPLE_HTML, global_field_order=[])
    print("\n[DEBUG] Parsed rows (basic):", rows)

    assert isinstance(rows, list)
    assert len(rows) == 2
    first = rows[0]
    assert first.get("name") == "Bechtle GmbH IT-Systemhaus Köln"
    assert "Köln" in first.get("address", "")
    assert first.get("phone", "").startswith("0221")
    assert "bechtle.com" in first.get("website", "")


def test_parse_page_missing_data():
    """
    Test parsing an entry that is missing a phone number.

    Verifies that missing fields are handled gracefully.
    """
    rows = parse_page_discovery(SAMPLE_HTML, global_field_order=[])
    second = rows[1]
    print("\n[DEBUG] Parsed row (missing data):", second)

    assert second.get("name") == "Example Without Phone"
    assert "Berlin" in second.get("address", "")
    assert "phone" not in second


def test_ai_enhancer():
    """
    Test the fallback AI entity extraction on raw text.

    Verifies that spaCy and regex extract name, address, and phone from unstructured text.
    """
    text = "Bechtle GmbH IT-Systemhaus Köln\nSchanzenstr. 41d, 51063 Köln\nTel: 0221 31 06 00"
    data = ai_extract_entities(text)
    print("\n[DEBUG] AI Enhancer output:", data)

    assert "Bechtle" in data.get("ai_name", "")
    assert "51063 Köln" in data.get("ai_address", "")
    assert "0221" in data.get("ai_phone", "")


def test_ai_fallback_on_raw_html():
    """
    Test parsing when no structured tags exist (forces AI fallback).

    Verifies that the AI fallback extracts useful info from raw HTML.
    """
    rows = parse_page_discovery(RAW_HTML, global_field_order=[])
    print("\n[DEBUG] AI Fallback parsed rows:", rows)

    assert len(rows) == 1
    row = rows[0]

    # The AI should still extract useful info
    assert "Super IT" in row.get("name", "")
    assert "10115 Berlin" in row.get("address", "")
    assert "030" in row.get("phone", "")
