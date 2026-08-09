# Enterprise Spring Boot 3 AdTech Web Crawler Application

Enterprise-grade AdTech Web Crawler REST API built with **Java 17 / 21**, **Spring Boot 3**, **Playwright Java SDK**, **Spring Data JPA**, **MySQL Persistence**, **Multi-Layered Redis Caching**, **SOLID Architecture**, **Docker**, **JUnit 5**, and **Postman Collection**.

---

## 🏗️ SOLID Architecture & Design Patterns

1. **Single Responsibility Principle (SRP)**:
   - `CrawlController`: Handles HTTP REST API contracts & JSON serialization.
   - `CrawlService`: Manages business flow, Redis caching, and MySQL database persistence.
   - `PlaywrightCrawlerEngine`: Manages browser context creation, network listeners, and stealth page automation.
   - `RedisCacheService`: Manages MD5 key hashing, TTL eviction, and fallback caching.
   - `HtmlReportGenerator`: Renders dark-mode visual dashboards.

2. **Open/Closed Principle (OCP)**:
   - `AdTechExtractor` interface allows adding new parameter extractors (`GptExtractor`, `PrebidExtractor`, `DomExtractor`, `PerformanceExtractor`) without modifying core engine logic.

3. **Concurrency & Session Isolation**:
   - `Executors.newFixedThreadPool(concurrency)` worker queue for parallel batch lookups.
   - Isolated Playwright `BrowserContext` per request to guarantee zero session cross-talk.

---

## 🛠️ Setup & Execution Guide

### 1. Environment Configuration (`.env`)
Create or edit `.env` inside `springboot_server/`:

```env
PROJECT_NAME=Forbes AdTech Crawler API (Spring Boot)
VERSION=2.0.0
PORT=8080

# MySQL Database Credentials
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=adtech_crawler
DATABASE_URL=jdbc:mysql://localhost:3306/adtech_crawler?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC

# Redis Caching Settings
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL_SECONDS=3600

# Storage Output Directory
OUTPUT_DIR=./output
```

---

### 2. Build & Run Spring Boot App

```bash
cd springboot_server

# Build Application
mvn clean package -DskipTests

# Run Application
java -jar target/crawler-2.0.0.jar
```
Server starts on port `8080`!

---

### 3. Run Automated JUnit 5 Test Suite
```bash
mvn test
```

---

### 4. Run Live End-to-End Verification Test
```bash
python test_e2e_verification.py
```

---

## 🐳 Docker Deployment Commands

### 1. Build and Start API + MySQL + Redis Containers
```bash
docker compose up --build -d
```

### 2. Check Container Logs
```bash
docker compose logs -f api
```

### 3. Stop Containers
```bash
docker compose down
```

---

## 🗄️ Manual MySQL Verification Commands

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root -p
# Password: root

USE adtech_crawler;
SHOW TABLES;
SELECT job_id, target_url, status, quality_score, quality_rating, created_at FROM crawl_jobs;
SELECT slot_id, width, height, is_visible, winning_bidder, winning_cpm FROM ad_slots;
```

---

## 📮 Postman Collection
Import `Postman_Collection.json` into Postman to execute pre-configured endpoints on `http://localhost:8080`.
