# 🚀 FastAPI AdTech Web Crawler REST Service

> **High-Performance Asynchronous Python Web Crawler REST API**  
> Built with **FastAPI**, **Playwright Async API**, **SQLAlchemy ORM**, **SQLite / MySQL Persistence**, **Redis Caching**, **Pytest Test Suite**, and **Docker**.

---

## ⚡ How Asynchronous Parallel Crawling Works in Code (`app/main.py`)

In FastAPI, async concurrency allows handling multiple REST API requests and crawling multiple website URLs simultaneously without blocking the main event loop.

### 1. Code Implementation (`trigger_batch_crawl`)
In `app/main.py`, batch crawling is handled asynchronously using `asyncio.Semaphore` and `asyncio.gather()`:

```python
# File: app/main.py
@app.post("/api/v1/crawl/batch")
async def trigger_batch_crawl(req: BatchCrawlRequest, db: Session = Depends(get_db)):
    # Create worker concurrency limiter from payload or default settings
    semaphore = asyncio.Semaphore(req.concurrency or settings.DEFAULT_CONCURRENCY)
    service = CrawlService(db=db)

    async def crawl_with_sem(url: str):
        async with semaphore:  # Bounded worker lock
            return await service.crawl_url(url, force_refresh=req.force_refresh)

    # Spawn async tasks concurrently
    tasks = [crawl_with_sem(u) for u in req.urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {"total_urls": len(req.urls), "results": results}
```

### 2. Architectural Highlights to Explain in Code Reviews
* **FastAPI Async Routes (`async def`)**: Routes are declared as `async def` so Uvicorn delegates I/O wait times (network traffic, Playwright navigation) to the event loop.
* **Non-Blocking Redis Caching (`app/redis_cache.py`)**: Checks Redis cache keys before triggering Playwright. If cached, returns responses in `<10ms`!
* **Database Thread Offloading (`SQLAlchemy`)**: Heavy database writes are handled cleanly so the API remains responsive to incoming HTTP requests.

---

## 🛠️ How to Customize URLs & Concurrency Parameters

You can customize target URLs and parallel concurrency levels directly in your API request payloads.

### 1. Single URL Crawl Request
**`POST /api/v1/crawl`**
```json
{
  "url": "https://www.yourcustomwebsite.com",
  "force_refresh": false
}
```

---

### 2. Custom Batch Parallel Crawl Request
**`POST /api/v1/crawl/batch`**
Pass any array of custom URLs and set `concurrency` (e.g. `4` parallel workers):

```json
{
  "urls": [
    "https://www.forbes.com",
    "https://www.bloomberg.com",
    "https://www.reuters.com",
    "https://www.techcrunch.com",
    "https://www.wsj.com"
  ],
  "concurrency": 4,
  "force_refresh": false
}
```

*Example cURL Command:*
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://www.forbes.com", "https://www.techcrunch.com"],
    "concurrency": 2,
    "force_refresh": false
  }'
```

---

## 🚀 Quick Setup & Execution Guide

### Step 1: Navigate to Project Directory
```bash
cd fastapi_server
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive documentation is available immediately at:
* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

---

## 🧪 Automated Testing Guide

Run the full pytest suite:

```bash
pytest -v
```

### Test Coverage:
* `test_read_root`: Verifies root health check endpoint.
* `test_cache_stats_endpoint`: Verifies Redis/in-memory cache statistics retrieval.
* `test_cache_clear_endpoint`: Verifies cache flush mechanics.
* `test_invalid_crawl_request`: Verifies Pydantic request payload validation (422 Unprocessable Entity).

---

## 📁 Codebase Structure & Key Modules

```text
fastapi_server/
├── app/
│   ├── main.py                  # FastAPI Application Routes & Async Batch Handler
│   ├── config.py                # Environment Variables & Settings (Pydantic Settings)
│   ├── db.py                    # SQLAlchemy Database Connection & Session Factory
│   ├── models.py                # Database ORM Entities (CrawlJob, CrawlPayload)
│   ├── schemas.py               # Pydantic Schemas for API Requests/Responses
│   ├── redis_cache.py           # Redis Cache Manager with In-Memory Fallback
│   └── services/
│       ├── crawl_service.py     # Business Service Layer handling Crawl & Cache Lookup
│       ├── crawler_engine.py    # Playwright Async Engine Integration
│       └── reporter.py          # Dark-Mode HTML Report Generator
├── tests/
│   └── test_api.py              # Pytest API Test Suite
├── requirements.txt             # Python Dependencies List
└── test_e2e_verification.py    # End-to-End API Integration Script
```
