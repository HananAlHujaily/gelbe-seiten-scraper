# Dockerfile for GelbeSeiten AI Scraper

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required for lxml and spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Install Python dependencies and spaCy model, then clean pip cache
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download de_core_news_sm \
    && pip cache purge

# Optional: Run tests (uncomment to use as build stage)
#RUN pytest -s -q

CMD ["python", "src/scraper.py"]
