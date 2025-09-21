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

### Key Technologies

- **Python 3.12**
- **requests** – HTTP requests
- **beautifulsoup4, lxml** – HTML parsing
- **spaCy** – Named Entity Recognition (German model)
- **regex** – Phone/address extraction
- **Tkinter** – GUI
- **pytest** – Testing

### Design Decisions

- **Discovery-first parsing:**  
  Ensures flexibility for changing website layouts.

- **AI fallback:**  
  Increases robustness against HTML changes or missing fields.

- **Portable outputs:**  
  All results saved in a fixed directory for easy access and sharing.

- **Docker support:**  
  Ensures reproducible environment and easy setup.

### Extensibility

- New output formats can be added easily.
- Additional AI models or heuristics can be integrated in `ai_enhancer.py`.
- GUI can be extended for more features.

---

## File Overview

| Path                | Purpose                                    |
|---------------------|--------------------------------------------|
| README.md           | Project overview, setup, usage             |
| DESIGN.md           | Architecture diagram, technical description|
| src/scraper.py      | Main scraper logic                         |
| src/ai_enhancer.py  | AI entity extraction                       |
| src/gui.py          | GUI interface                              |
| requirements.txt    | Python dependencies                        |
| Dockerfile          | Container setup                            |
| tests/              | Test scripts and cases                     |
| data/sample_input/  | Example input queries                      |
| results/            | Output files (CSV, JSON)                   |

---

## Development Notes

- **AI systems used:** spaCy, regex (see README)

---

## Contact

For questions or improvements, please contact the project