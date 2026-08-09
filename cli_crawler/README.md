# Standalone AdTech CLI Crawler Engine

A lightweight, standalone Playwright stealth scraper for extracting 16 AdTech parameters (GPT slots, Prebid S2S bids, creative iframes, ads.txt) without external database dependencies.

## 🚀 Setup & Execution

### 1. Create Virtual Environment & Install Dependencies
```bash
cd cli_crawler

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r requirements.txt

# Install Playwright Chromium Browser Binaries
python -m playwright install chromium
```

---

### 2. Running Single URL Crawl
Extract complete AdTech metrics and generate JSON & dark-mode HTML dashboard reports:
```bash
python main.py --url https://www.forbes.com
```

---

### 3. Running 20-Publisher Benchmark Suite
Execute multi-threaded batch crawling across top 20 news publishers with concurrency:
```bash
python main.py --test-20 --concurrency 4
```

---

## 📊 Extracted Outputs

- **JSON Payloads**: Saved in `./output/result_<domain>_<timestamp>.json`
- **Interactive HTML Dashboards**: Saved in `./output/report_<domain>_<timestamp>.html`
- **Creative Frame Screenshots**: Saved in `./output/screenshots/`
