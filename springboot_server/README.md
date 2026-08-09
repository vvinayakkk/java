# 🌐 Enterprise Spring Boot 3 AdTech Web Crawler Application

> **Production-Grade AdTech Web Automation, Redis Caching & Database Analytics Engine**  
> Built with **Java 17/21**, **Spring Boot 3**, **Playwright Java SDK**, **Spring Data JPA**, **MySQL / H2 Persistence**, **Multi-Layered Redis Caching**, **Docker Compose**, **JUnit 5**, and **Python E2E Verification Suite**.

---

## 📌 Executive Directory & Execution Summary

To run or test this enterprise crawler application on any machine (including company laptops without AI tools), execute all commands from the **`springboot_server`** project directory:

```bash
# 1. Navigate to the project directory from repo root
cd springboot_server

# 2. Build the application & package JAR
mvn clean package -DskipTests

# 3. Start the application
java -jar target/crawler-2.0.0.jar
```

---

## ⚙️ System Prerequisites

Ensure the following tools are installed and available on your system PATH:

* **Java Development Kit (JDK)**: Version 17 or higher (Java 17 / 21 recommended). Verify with:
  ```bash
  java -version
  ```
* **Apache Maven**: Version 3.8+ (or wrapper). Verify with:
  ```bash
  mvn -version
  ```
* **Docker & Docker Compose** *(Optional, for containerized MySQL & Redis)*: Verify with:
  ```bash
  docker --version
  docker compose version
  ```
* **Python 3.9+** *(Optional, for running E2E verification suite)*: Verify with:
  ```bash
  python --version
  ```

---

## 🚀 Playwright Browser Binaries Installation

The application uses Playwright Java to launch headless Chromium browser contexts. Playwright automatically downloads browser binaries on first run, or you can pre-install them manually from `springboot_server`:

```bash
cd springboot_server

# Install Playwright Chromium browser binaries via Maven CLI
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install chromium"
```

---

## 🏗️ Quick Setup & Execution Guide (Step-by-Step)

### Option A: Local Execution (Standalone / In-Memory H2 Mode)

If MySQL or Redis are not running locally, the application automatically falls back to in-memory H2 database and local concurrent hash map cache.

```bash
# 1. Navigate to springboot_server directory
cd springboot_server

# 2. Build and package the project
mvn clean package -DskipTests

# 3. Run the application
java -jar target/crawler-2.0.0.jar
# (Or use: mvn spring-boot:run)
```

The server starts on `http://localhost:8080`!

---

### Option B: Docker Compose Execution (Full Container Stack)

Spawns the **Spring Boot API**, **MySQL 8.4 Database**, and **Redis Cache** in isolated containers:

```bash
# 1. Navigate to springboot_server directory
cd springboot_server

# 2. Build & launch all Docker services
docker compose up --build -d

# 3. Monitor container logs
docker compose logs -f api

# 4. Stop all containers when done
docker compose down
```

---

## 📡 REST API Endpoint Reference & cURL Commands

Base Server URL: `http://localhost:8080`

### 1. Health & Server Info (`GET /` or `GET /health`)
Check system status and engine version:

```bash
curl -X GET "http://localhost:8080/"
```

*Sample Response:*
```json
{
  "status": "UP",
  "framework": "Spring Boot 3.2.0",
  "app": "Forbes AdTech Crawler API (Spring Boot)",
  "version": "2.0.0"
}
```

---

### 2. Execute Live Web Crawl (`POST /api/v1/crawl`)
Triggers a stealth Playwright Chromium context load, evaluates AdTech GPT slots, Prebid auction bids, rendered iframes, and network performance metrics, storing results in database & Redis:

```bash
curl -X POST "http://localhost:8080/api/v1/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.forbes.com",
    "forceRefresh": false
  }'
```

*Sample Response:*
```json
{
  "jobId": "job_1707500000000_a1b2",
  "targetUrl": "https://www.forbes.com",
  "httpStatus": 200,
  "executionTimeMs": 2450,
  "qualityScore": 100,
  "qualityRating": "EXCELLENT",
  "cached": false,
  "adSlotsSummary": [
    {
      "slotId": "top-banner-ad",
      "width": 728,
      "height": 90,
      "isVisible": true,
      "winningBidder": "rubicon",
      "winningCpm": 2.50
    }
  ]
}
```

*Repeat Request (Cache Hit):*
Executing the same command with `"forceRefresh": false` returns the result **instantly (<20ms)** directly from Redis cache with `"cached": true`!

*Force Refresh Request (Cache Bypass):*
```bash
curl -X POST "http://localhost:8080/api/v1/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.forbes.com",
    "forceRefresh": true
  }'
```

---

### 3. Execute Batch Parallel Crawl (`POST /api/v1/crawl/batch`)
Executes parallel multi-threaded crawls using an internal fixed thread pool executor:

```bash
curl -X POST "http://localhost:8080/api/v1/crawl/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.forbes.com",
      "https://www.cnn.com",
      "https://www.nytimes.com"
    ],
    "concurrency": 3
  }'
```

---

### 4. Query Crawl History & Job Details

* **List Recent Crawl Jobs (`GET /api/v1/crawls?limit=10`)**:
  ```bash
  curl -X GET "http://localhost:8080/api/v1/crawls?limit=10"
  ```

* **Get Specific Job Details by ID (`GET /api/v1/crawls/{jobId}`)**:
  ```bash
  curl -X GET "http://localhost:8080/api/v1/crawls/job_1707500000000_a1b2"
  ```

---

### 5. Redis Cache Management Endpoints

* **Get Cache Statistics (`GET /api/v1/cache/stats`)**:
  ```bash
  curl -X GET "http://localhost:8080/api/v1/cache/stats"
  ```

* **Clear All Cached Keys (`POST /api/v1/cache/clear`)**:
  ```bash
  curl -X POST "http://localhost:8080/api/v1/cache/clear"
  ```

---

## 🧪 Automated Testing & Verification Suite

### 1. Run Automated JUnit 5 Unit Tests
From `springboot_server`:

```bash
mvn test
```

### 2. Run Live End-to-End Parity Verification Test
With the server running on `http://localhost:8080`, execute the Python E2E verification script:

```bash
# Ensure requests package is installed:
pip install requests

# Run E2E verification script:
python test_e2e_verification.py
```

*Expected Verification Output:*
```text
=================================================================
  SPRING BOOT 3 END-TO-END FASTAPI-PARITY VERIFICATION SUITE
=================================================================
[PASSED] Health Check Endpoint (Status: UP)
[PASSED] Live Crawl Success! Job ID: job_... | Quality Score: 100/100 | Cached: False
[PASSED] Cache Hit Verified! Time Taken: 0.0084s (<0.2s) | Cached: True
[PASSED] Force Refresh Verified! Bypassed cache in 2.12s
[PASSED] MySQL DB History Verified! Found 3 persisted crawl jobs.
[PASSED] MySQL DB Job Detail & Payload Blob Verified
[PASSED] Cache Stats Endpoint: Total Keys: 1, Mode: REDIS
[PASSED] Cache Clear Endpoint Success
=================================================================
    SPRING BOOT 3 VERIFICATION TESTS PASSED SUCCESSFULLY!
=================================================================
```

---

## 📮 Postman Collection
Import `springboot_server/Postman_Collection.json` into Postman to run pre-configured endpoints and automated API test suites against `http://localhost:8080`.

---

## 🏛️ SOLID System Architecture & Key Components

```text
src/main/java/com/adtech/crawler/
├── AdtechCrawlerApplication.java   # Spring Boot Main Entry Point
├── config/
│   └── RedisConfig.java            # RedisTemplate & KeySerializer Setup
├── controller/
│   ├── CacheController.java        # Cache Stats & Clear Endpoints
│   ├── CrawlController.java        # Core Crawl & History REST API
│   └── HealthController.java       # Health Check Endpoint
├── crawler/
│   ├── AdsTxtParser.java           # parses ads.txt publisher records
│   ├── PlaywrightCrawlerEngine.java# Headless Playwright Chromium & Route Interception
│   ├── QualityValidator.java       # Quality Score Computation Engine (0-100)
│   └── extractor/                  # Open/Closed Extractor Modules
│       ├── AdTechExtractor.java    # Core Parameter Extractor Interface
│       ├── DomExtractor.java       # DOM Tree & iFrame Traversal
│       ├── GptExtractor.java       # Google Publisher Tag (GPT) Ad Slots
│       ├── PerformanceExtractor.java# Page Load Timings & Network Subresources
│       └── PrebidExtractor.java    # Header Bidding (pbjs.getBidResponses)
├── model/
│   ├── dto/                        # Request/Response Data Transfer Objects
│   └── entity/                     # JPA Entities (CrawlJobEntity, AdSlotEntity, Payload)
├── repository/
│   ├── CrawlJobRepository.java     # Spring Data JPA Repository for Jobs
│   └── CrawlPayloadRepository.java  # Repository for Heavy JSON Payload Blobs
└── service/
    ├── CrawlService.java           # Business Logic, Executor Service & DB Sync
    ├── HtmlReportGenerator.java    # Dark-Mode Visual Dashboard Generator
    └── RedisCacheService.java      # MD5 Hashing, TTL Eviction & Fallback Caching
```
