"""
metrics.py

This module provides a utility function for saving scraping metrics such as query, number of pages, and row count.
Metrics are stored as JSON files under <project_root>/results/metrics/.

Functions:
    save_metrics(query: str, pages: int, rows: int, out_dir: str = "results") -> str
        Saves metrics for a scraping run to a timestamped JSON file.
"""

import os
import json
from datetime import datetime

def save_metrics(query: str, pages: int, rows: int, out_dir: str = "results") -> str:
    """
    Save a simple metrics file with query, number of pages, and row count.
    Stored under <project_root>/results/metrics/<query_timestamp>.json

    Args:
        query (str): The search query used for scraping.
        pages (int): Number of pages scraped.
        rows (int): Number of rows (results) scraped.
        out_dir (str, optional): Output directory relative to project root. Defaults to "results".

    Returns:
        str: Path to the saved metrics JSON file.
    """
    # Ensure output is always relative to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metrics_dir = os.path.join(project_root, out_dir, "metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = query.replace(" ", "_").lower() + "_" + ts
    path = os.path.join(metrics_dir, f"{stem}.json")

    data = {
        "query": query,
        "pages": pages,
        "rows": rows,
        "timestamp": ts,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return path
