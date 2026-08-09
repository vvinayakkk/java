# Enterprise AdTech Web Crawler Architecture

An enterprise-grade, stealth web crawling and adtech quality validation architecture built with **Playwright**, **FastAPI**, **Spring Boot 3**, **MySQL**, **Redis**, and **Docker**.

## 📁 Repository Structure

```
makdi/
├── cli_crawler/          # 1. Standalone CLI Scraper & Batch Benchmark Engine (Python)
├── fastapi_server/       # 2. Enterprise FastAPI Web Server (Python 3.10+ / MySQL / Redis)
├── springboot_server/    # 3. Enterprise Spring Boot 3 Web Server (Java 17+ / JPA / Redis / SOLID)
└── alternative_scrapers/ # 4. Scraper Benchmark Suite & Playwright Technical Justification
```

---

## ⚡ Architecture Breakdown & Quick Start Options

### Option 1: Standalone CLI Crawler (Python)
If you want to run single-line CLI web crawls or execute 20-site publisher benchmarks without setting up a web server:
👉 See [cli_crawler/README.md](file:///c:/Users/Lenovo/Desktop/makdi/cli_crawler/README.md)

### Option 2: FastAPI Web Server (Python)
If you want to run the FastAPI REST API server with MySQL relational persistence, Redis caching, Docker Compose, Pytest suite, and Postman API collection:
👉 See [fastapi_server/README.md](file:///c:/Users/Lenovo/Desktop/makdi/fastapi_server/README.md)

### Option 3: Spring Boot 3 Web Server (Java 17+)
If you want to run the enterprise Spring Boot 3 REST API server built with Playwright Java SDK, Spring Data JPA, Redis, SOLID design patterns, Docker Compose, JUnit 5 test suite, and Postman API collection:
👉 See [springboot_server/README.md](file:///c:/Users/Lenovo/Desktop/makdi/springboot_server/README.md)

### Option 4: Alternative Scrapers Benchmark & Playwright Deep-Dive
If you want to see comparative benchmarks across 5 alternative tools (`requests+bs4`, `selenium`, `httpx`, `pyppeteer`, `urllib`) and a complete beginner-to-advanced technical deep dive explaining why Playwright was chosen:
👉 See [alternative_scrapers/README.md](file:///c:/Users/Lenovo/Desktop/makdi/alternative_scrapers/README.md)
