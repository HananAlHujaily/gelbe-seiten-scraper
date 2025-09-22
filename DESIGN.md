# GelbeSeiten AI Scraper – Design & Architecture

## Architecture Diagram

```
+-------------------+
|  User / CLI / GUI |
+---------+---------+
          |
          v
+-------------------+
|   scraper.py      | <--- Entry point: CLI, interactive, or GUI
+---------+---------+
          |
          v
+-------------------+
|  Web Scraping     |  (requests, BeautifulSoup)
+---------+---------+
          |
          v
+-------------------+
|  Discovery Parser |  (OrderedDict, dynamic field order)
+---------+---------+
          |
          v
+-------------------+
|  AI Enhancer      |  (ai_enhancer.py: spaCy, regex fallback)
+---------+---------+
          |
          v
+-------------------+
|  Output Writer    |  (CSV, JSON, results/)
+-------------------+
```

## Technical Description

### Components

- **scraper.py**  
  Main script. Handles CLI, interactive, and GUI modes. Orchestrates scraping, parsing, AI fallback, and output.

- **ai_enhancer.py**  
  Provides AI-based entity extraction using spaCy and regex for robust fallback when HTML selectors fail.

- **metrics.py**  
  Utility for saving scraping metrics (query, pages, rows, timestamp) as JSON in `results/metrics/`.

- **GUI (src/gui.py)**  
  Tkinter-based graphical interface for user-friendly scraping.

- **results/**  
  All outputs (CSV, JSON) are saved here for portability.

- **tests/**  
  Contains unit and integration tests for parser and AI fallback.

### Data Flow

1. **User Input:**  
   User provides a profession/industry via CLI, interactive prompt, or GUI.

2. **Scraping:**  
   `scraper.py` downloads result pages from Gelbe Seiten using requests.

3. **Parsing:**  
   HTML is parsed with BeautifulSoup. Fields are discovered and stored in order.

4. **AI Fallback:**  
   If essential fields (name, address, phone) are missing, raw text is sent to `ai_enhancer.py` for extraction using spaCy and regex.

5. **Output:**  
   Results are written to CSV and/or JSON in the `results/` directory.

6. **Metrics Tracking:**  
   After each scrape, metrics (query, pages, rows, timestamp) are saved via `metrics.py` in `results/metrics/`.

### Key Technologies

- **Python 3.12**
- **requests** – HTTP requests
- **beautifulsoup4, lxml** – HTML parsing
- **spaCy** – Named Entity Recognition (German model)
- **regex** – Phone/address extraction
- **Tkinter** – GUI
- **pytest** – Testing
- **json, csv** – Output formats
- **PyInstaller** – Packaging GUI as executable

### Design Decisions

- **Discovery-first parsing:**  
  Ensures flexibility for changing website layouts.

- **AI fallback:**  
  Increases robustness against HTML changes or missing fields.

- **Portable outputs:**  
  All results saved in a fixed directory for easy access and sharing.

- **Docker support:**  
  Ensures reproducible environment and easy setup.

- **Metrics tracking:**  
  Each scrape run saves a metrics file for reproducibility and analysis.

### Extensibility

- New output formats can be added easily.
- Additional AI models or heuristics can be integrated in `ai_enhancer.py`.
- GUI can be extended for more features.
- Metrics logic can be extended for more detailed analytics.
- Packaging can be customized via `gui.spec`.

---

## File Overview

| Path                | Purpose                                    |
|---------------------|--------------------------------------------|
| README.md           | Project overview, setup, usage             |
| DESIGN.md           | Architecture diagram, technical description|
| src/scraper.py      | Main scraper logic                         |
| src/ai_enhancer.py  | AI entity extraction                       |
| src/metrics.py      | Metrics saving utility                     |
| src/gui.py          | GUI interface                              |
| requirements.txt    | Python dependencies                        |
| Dockerfile          | Container setup                            |
| gui.spec            | PyInstaller spec for GUI packaging         |
| tests/              | Test scripts and cases                     |
| data/sample_input/  | Example input queries                      |
| results/            | Output files (CSV, JSON, metrics)          |

---

## Development Notes

- **AI systems used:** spaCy, regex (see README)
- **Metrics tracking:** See `metrics.py` for implementation details.
- **Packaging:** See `gui.spec` for PyInstaller configuration.

