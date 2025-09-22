"""
scraper.py GelbeSeiten AI Scraper (Discovery Mode)

This script scrapes business listings from Gelbe Seiten for a given profession
or industry (e.g., "IT", "Rohrleger") and saves results into CSV and JSON.

Features:
- Discovery-first parsing (fields are added in the order discovered).
- AI fallback using spaCy + regex (from ai_enhancer.py) if selectors fail.
- Results saved in project-root-level results/ folder (portable across devices).
- User-friendly CLI with interactive fallback if no query is given.
"""

import argparse
import csv
import json
import os
import time
from collections import OrderedDict
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from ai_enhancer import ai_extract_entities
from metrics import save_metrics   # NEW: metrics integration

# Base URL for Gelbe Seiten search
BASE_URL = "https://www.gelbeseiten.de/suche/{}/"

# Custom User-Agent (polite scraping practice)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GelbeSeitenScraper/1.0)"}


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------
def scrape_page(query: str, page: int = 1) -> str | None:
    """
    Download a Gelbe Seiten search results page.
    """
    url = BASE_URL.format(query) + f"?page={page}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            return resp.text
        print(f"[WARN] Failed to fetch page {page}: HTTP {resp.status_code}")
        return None
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def _add_field_in_order(order_list: list, key: str):
    """Add key to order_list if not present (preserve discovery order)."""
    if key not in order_list:
        order_list.append(key)


# -----------------------------------------------------------------------------
# Parsing
# -----------------------------------------------------------------------------
def parse_page_discovery(html: str, global_field_order: list) -> list[OrderedDict]:
    """
    Parse a Gelbe Seiten HTML page into structured OrderedDict rows.
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    results = []
    entries = soup.find_all("article", class_="mod-Treffer")

    for entry in entries:
        row = OrderedDict()
        raw_text = entry.get_text("\n", strip=True)

        # Name
        name_el = entry.find("h2")
        if name_el:
            row["name"] = name_el.get_text(strip=True)
            _add_field_in_order(global_field_order, "name")

        # Category
        category_el = entry.select_one("div.mod-Treffer__kategorie, div.mod-Treffer__branche, p")
        if category_el:
            row["category"] = category_el.get_text(strip=True)
            _add_field_in_order(global_field_order, "category")

        # Address
        address_el = entry.select_one("address.mod-AdresseKompakt, div.mod-AdresseKompakt__adress-text")
        if address_el:
            row["address"] = address_el.get_text(" ", strip=True)
            _add_field_in_order(global_field_order, "address")

        # Phone
        phone_el = entry.select_one("a.mod-TelefonnummerKompakt__phoneNumber, a[href^='tel:']")
        if phone_el:
            row["phone"] = phone_el.get_text(strip=True)
            _add_field_in_order(global_field_order, "phone")

        # Website
        website = None
        web_el = entry.select_one("span.mod-WebseiteKompakt__text")
        if web_el and web_el.has_attr("data-websitelink"):
            website = web_el["data-websitelink"]
        if not website:
            site_a = entry.select_one("a[href^='http']")
            if site_a:
                href = site_a.get("href")
                if href and "gelbeseiten" not in href:
                    website = href
        if website:
            row["website"] = website
            _add_field_in_order(global_field_order, "website")

        # Email
        mail_el = entry.select_one("a[href^='mailto:']")
        if mail_el:
            email = mail_el.get("href")
            if email:
                row["email"] = email.replace("mailto:", "")
                _add_field_in_order(global_field_order, "email")

        # Badge
        for t in entry.stripped_strings:
            if "Partner" in t or "PARTNER" in t:
                row["badge"] = t
                _add_field_in_order(global_field_order, "badge")
                break

        # AI fallback if missing essentials
        if ("name" not in row) or ("address" not in row) or ("phone" not in row):
            ai = ai_extract_entities(raw_text)
            if ai.get("ai_name") and "name" not in row:
                row["name"] = ai.get("ai_name")
                _add_field_in_order(global_field_order, "name")
            if ai.get("ai_address") and "address" not in row:
                row["address"] = ai.get("ai_address")
                _add_field_in_order(global_field_order, "address")
            if ai.get("ai_phone") and "phone" not in row:
                row["phone"] = ai.get("ai_phone")
                _add_field_in_order(global_field_order, "phone")

        if row:
            results.append(row)

    return results


# -----------------------------------------------------------------------------
# Export
# -----------------------------------------------------------------------------
def export_rows_discovery(rows: list[OrderedDict], query: str, out_dir: str,
                          formats: list[str], field_order: list):
    """
    Save results to CSV and JSON under results/csv and results/json.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(project_root, out_dir)

    os.makedirs(os.path.join(out_dir, "csv"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "json"), exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = query.replace(" ", "_").lower() + "_" + ts
    paths = {}

    # Column order
    if not field_order:
        field_order = list(rows[0].keys()) if rows else []

    all_keys = list(field_order)
    for r in rows:
        for k in r.keys():
            if k not in all_keys:
                all_keys.append(k)

    if "csv" in formats:
        csv_path = os.path.join(out_dir, "csv", f"{stem}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(rows)
        paths["csv"] = csv_path

    if "json" in formats:
        json_path = os.path.join(out_dir, "json", f"{stem}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([dict(r) for r in rows], f, indent=2, ensure_ascii=False)
        paths["json"] = json_path

    return paths


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------
def run_discovery(query: str, pages: int = 1, out_dir: str = "results",
                  formats: list[str] | None = None):
    """Run scraping for multiple pages."""
    if formats is None:
        formats = ["csv", "json"]

    all_rows: list[OrderedDict] = []
    global_field_order: list = []

    for p in range(1, pages + 1):
        html = scrape_page(query, p)
        if not html:
            continue
        page_rows = parse_page_discovery(html, global_field_order)
        all_rows.extend(page_rows)
        time.sleep(1.0)  # polite delay

    # Export CSV/JSON
    export_paths = export_rows_discovery(all_rows, query, out_dir, formats, global_field_order)

    # Save metrics
    metrics_path = save_metrics(query, pages, len(all_rows), out_dir)
    print(f" - METRICS: {metrics_path}")

    return export_paths


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def main():
    print("🔎 Welcome to the GelbeSeiten AI Scraper (Discovery mode)")

    parser = argparse.ArgumentParser(description="Scrape Gelbe Seiten for a given profession/industry.")
    parser.add_argument("query", nargs="?", help="Profession, e.g., 'Rohrleger', 'IT'")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("--out-dir", default="results", help="Output directory (relative to project root)")
    parser.add_argument("--formats", default="csv,json", help="Comma-separated: csv,json")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI fallback")

    args = parser.parse_args()
    if not args.query:
        args.query = input("Enter a profession or industry: ").strip()

    fmts = [x.strip() for x in args.formats.split(",") if x.strip()]

    # Optionally disable AI fallback
    global ai_extract_entities
    if args.no_ai:
        def _noop_ai(text): return {"ai_name": None, "ai_address": None, "ai_phone": None}
        ai_extract_entities = _noop_ai

    paths = run_discovery(args.query, pages=args.pages, out_dir=args.out_dir, formats=fmts)

    print("\n✅ Scraping completed! Files saved:")
    for k, v in paths.items():
        print(f" - {k.upper()}: {v}")


if __name__ == "__main__":
    main()
