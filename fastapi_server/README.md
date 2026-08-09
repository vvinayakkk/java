# Enterprise FastAPI Web Application Server

Enterprise-grade AdTech Web Crawler REST API featuring **MySQL Relational Persistence**, **Multi-Layered Redis Caching**, **Docker Containerization**, **Pytest Automated Test Suite**, and **Postman Collection**.

---

## 🛠️ Prerequisites & Setup

### 1. Environment File (`.env`)
Create or edit `.env` inside `fastapi_server/`:

```env
# Application Settings
PROJECT_NAME=Forbes AdTech Crawler API
VERSION=2.0.0
DEBUG=False
DEFAULT_CONCURRENCY=5

# MySQL Database Settings
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=adtech_crawler
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/adtech_crawler

# Redis Caching Settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
CACHE_TTL_SECONDS=3600

# File Storage Output Directory
OUTPUT_DIR=./output
```

---

### 2. Setup Local Python Environment (`venv`)

```bash
cd fastapi_server

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install Server Dependencies
pip install -r requirements.txt

# Install Playwright Chromium Binaries
python -m playwright install chromium
```

---

## 🚀 Running & Testing the Server

### 1. Launch FastAPI Server Locally
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

### 2. Run Automated Pytest Test Suite
```bash
python -m pytest tests/test_api.py
```

---

### 3. Run Live End-to-End Verification Suite
Tests live crawling, database persistence, cache miss, cache hit (< 8ms), and cache clear APIs:
```bash
python test_e2e_verification.py
```

---

## 🐳 Docker Deployment Commands

### 1. Build and Start API + MySQL + Redis Containers
```bash
docker compose up --build -d
```

### 2. View Live Container Status & Logs
```bash
docker compose ps
docker compose logs -f api
```

### 3. Stop Docker Containers
```bash
docker compose down
```

---

## 🗄️ Manual MySQL CLI Commands & Verification

### 1. Log into MySQL CLI manually (Windows)

#### Option A: Direct Executable Path
```powershell
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root -p
```

#### Option B: standard CLI (or inside Docker)
```bash
mysql -u root -p
```
> **Prompt Password**: `root`

---

### 2. Useful SQL Commands

Once logged into the MySQL shell (`mysql>`), run:

#### List all databases
```sql
SHOW DATABASES;
```

#### Switch to the crawler database
```sql
USE adtech_crawler;
```

#### View all populated tables
```sql
SHOW TABLES;
```

#### Query recent crawl jobs
```sql
SELECT job_id, target_url, status, quality_score, quality_rating, created_at 
FROM crawl_jobs 
ORDER BY created_at DESC;
```

#### Query extracted ad slots and winning CPM bids
```sql
SELECT slot_id, width, height, is_visible, winning_bidder, winning_cpm 
FROM ad_slots 
LIMIT 10;
```

#### Query demand partner bidder metrics
```sql
SELECT bidder_code, bids_count, max_cpm, avg_cpm 
FROM bidder_summaries;
```

#### Exit MySQL Shell
```sql
EXIT;
```

---

## 📮 Postman Collection
Import `Postman_Collection.json` into Postman to execute pre-configured API endpoints:
- `GET /` (Health Check)
- `POST /api/v1/crawl` (Single Crawl)
- `POST /api/v1/crawl/batch` (Batch Crawl)
- `GET /api/v1/crawls` (List Jobs)
- `GET /api/v1/crawls/{job_id}` (Job Details)
- `GET /api/v1/crawls/{job_id}/report` (HTML Report)
- `GET /api/v1/cache/stats` (Cache Stats)
- `POST /api/v1/cache/clear` (Clear Cache)
