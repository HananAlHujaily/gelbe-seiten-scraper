# GelbeSeiten AI Scraper


It is a local Python tool that scrapes business listings from Gelbe Seiten (German Yellow Pages) for a given profession or industry (e.g., IT, Plumber, Electrician) and saves them as structured data.

📌 **Project Overview**

- **Input:** Profession / industry (e.g., IT, Plumber)
- **Source:** Gelbe Seiten
- **Output:** CSV and/or JSON (user selectable)
- **Metrics:** Scraping metrics (query, pages, rows, timestamp) are saved as JSON in `results/metrics/`.

**Key Features:**
- **Discovery-first parsing:** Fields are saved in the order they appear on the website.
- **AI fallback with spaCy + Regex:** If HTML structure is missing or changes, name, address, and phone are extracted from raw text.
- **Portability:** Results and metrics are always saved in `results/` at the project root.
- **Multiple modes:** CLI, interactive input, or GUI.
- **Metrics tracking:** Each scrape run saves a metrics file with details about the query and results.

---

⚙️ **Setup**

**Clone the repository:**
```bash
git clone https://github.com/HananAlHujaily/gelbe-seiten-scraper.git
cd gelbe-seiten-scraper
```

Download and extract the project

Unzip the folder you received (`gelbe-seiten-scraper.zip`).

Open a terminal and navigate into the extracted folder:
```bash
cd gelbe-seiten-scraper
```

Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download de_core_news_sm
```

---

🚀 **Usage**

**1) CLI Mode**
```bash
python src/scraper.py IT --pages 2
```
**Arguments:**
- `query`: Profession/industry (e.g., Plumber, IT)
- `--pages`: Number of result pages (default=1)
- `--out-dir`: Output directory (default=results/)
- `--formats`: csv,json (choose one or both)
- `--no-ai`: Disable AI fallback

**2) Interactive Mode**
```bash
python src/scraper.py
```
You will be prompted to enter a profession.

**3) GUI Mode**
```bash
python src/gui.py
```
A Tkinter window will open where you can:
- Enter profession/industry
- Enter number of pages
- Select output format (CSV, JSON, or both)
- Click Scrape → A popup will show saved file paths

---

📂 **Outputs**

Results are saved in `results/`:
```
results/
├── csv/
│   └── it_20250920_101500.csv
├── json/
│   └── it_20250920_101500.json
└── metrics/
    └── it_20250920_101500.json
```

**Example JSON entry (business):**
```json
{
  "name": "Bechtle GmbH IT-Systemhaus Köln",
  "address": "Schanzenstr. 41d, 51063 Köln",
  "phone": "0221 31 06 00",
  "website": "https://www.bechtle.com"
}
```

**Example metrics file:**
```json
{
  "query": "IT",
  "pages": 2,
  "rows": 20,
  "timestamp": "20250920_101500"
}
```

---

🧪 **Testing (optional)**

Run tests:
```bash
pip install pytest
pytest -s -q
```
Expected:
```
4 passed in 1.2s
```

---

⚠️ **Note:** This tool is for demonstration and testing purposes. Please respect the Gelbe Seiten terms of service when scraping.
