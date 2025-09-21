# GelbeSeiten AI Scraper

This project was developed as part of the 3D Padelt GmbH test assignment.  
It is a local Python tool that scrapes business listings from Gelbe Seiten (German Yellow Pages) for a given profession or industry (e.g., IT, Plumber, Electrician) and saves them as structured data.

📌 **Project Overview**

- **Input:** Profession / industry (e.g., IT, Plumber)
- **Source:** Gelbe Seiten
- **Output:** CSV and/or JSON (user selectable)

**Key Features:**
- **Discovery-first parsing:** Fields are saved in the order they appear on the website.
- **AI fallback with spaCy + Regex:** If HTML structure is missing or changes, name, address, and phone are extracted from raw text.
- **Portability:** Results are always saved in `results/` at the project root.
- **Multiple modes:** CLI, interactive input, or GUI.

---

⚙️ **Setup**

Clone or download this project

Create a virtual environment:
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
└── json/
    └── it_20250920_101500.json
```

**Example JSON entry:**
```json
{
  "name": "Bechtle GmbH IT-Systemhaus Köln",
  "address": "Schanzenstr. 41d, 51063 Köln",
  "phone": "0221 31 06 00",
  "website": "https://www.bechtle.com"
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

⏱️ **Development Effort**

- The core development was efficient because I previously completed similar projects during my university NLP course and my internship at KLAO.
- Most of the time was spent enhancing the solution with features like the AI-based entity extraction (`ai_enhancer.py`).
- For the final version, I leveraged tools such as ChatGPT and GitHub Copilot to improve code quality and documentation.
- **Total time spent:** ~4h (including design, implementation, testing, and documentation)
---

🧠 **AI Systems Used**

- **spaCy (de_core_news_sm):** Named Entity Recognition (company names)
- **Regex:** German phone numbers & postal codes

---

⚠️ **Note:** This tool is for demonstration and testing purposes. Please respect the Gelbe Seiten terms of service when scraping.

✅ This is a complete README that fulfills all