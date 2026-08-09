# Guided Practice 4 – Measuring API Performance

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~45 minutes (Live Performance Benchmarking & Bottleneck Analysis)

---

## 🏢 Engineering Scenario & Objective
> "Before attempting to optimize any production software, engineers must gather concrete, empirical performance measurements. Optimization without measurement is guessing. In this Guided Practice, you will measure the latency of multiple API endpoints across repeated executions, calculate statistical averages, identify the slowest endpoint, and analyze root-cause performance bottlenecks using empirical evidence."

**Key Learning Goals:**
1. Establish a rigorous measurement protocol (warmup discarded, repeated measured runs).
2. Bench-test three distinct read endpoints on `spring-bookstore`.
3. Calculate mean latency and identify statistical outliers.
4. Diagnose performance bottlenecks using database fetch behavior and entity mapping analysis.

---

## 📊 Performance Measurement Protocol & Results

### Measurement Setup:
- **Server:** Spring Boot 3.2.0 running on OpenJDK 17 (`http://localhost:8080`).
- **Database:** H2 In-Memory Database pre-seeded with 5 Authors, 5 Categories, and 90 Books (`DataLoader.java`).
- **Methodology:** Each endpoint executed 6 times total: Run 0 (warmup call, discarded to eliminate JVM class loading & JIT compilation cold start noise), followed by **5 measured runs (R1 to R5)**.
- **Timing Tool:** High-precision Stopwatch timer script (`measure.ps1`).

---

## 📈 Empirical Latency Data Table

| Endpoint # | Target Endpoint URL | Method | R1 (ms) | R2 (ms) | R3 (ms) | R4 (ms) | R5 (ms) | Calculated Average (ms) |
|---|---|---|---|---|---|---|---|---|
| **A** | `GET /api/books/1` | GET | 28 ms | 14 ms | 13 ms | 17 ms | 9 ms | **16.2 ms** |
| **B** | `GET /api/books?page=0&size=10` | GET | 52 ms | 50 ms | 37 ms | 32 ms | 30 ms | **40.2 ms** |
| **C** | `GET /api/books/search?title=Patterns` | GET | 18 ms | 19 ms | 17 ms | 24 ms | 28 ms | **21.2 ms** |

---

## 🔍 Bottleneck Analysis & Empirical Evidence

### 1. Slowest Endpoint Identified:
**Endpoint B: `GET /api/books?page=0&size=10`** with an average response time of **40.2 ms** (more than **2.5x slower** than single book lookup by ID).

### 2. Why is Endpoint B significantly slower?
- **Multi-Row `FetchType.EAGER` Joins:** Querying page items requires Hibernate to load multiple `Book` entities while eagerly fetching associated `Author` and `Category` entities for every row in the result page.
- **Count Query Overhead:** Spring Data JPA executes two separate database queries for paginated requests:
  1. Data query: `SELECT * FROM books LIMIT 10 OFFSET 0` (plus joins).
  2. Count query: `SELECT COUNT(*) FROM books` to compute `totalPages` and `totalElements`.
- **Object Allocation & DTO Mapping:** Mapping 10 full entity graphs into DTO instances creates significantly higher garbage collection and allocation overhead compared to indexed single-record lookup (`/api/books/1`).

### 3. Comparison with Search Endpoint C:
`GET /api/books/search?title=Patterns` averaged **21.2 ms**. Search is faster than page list because search returns a filtered list directly without executing a secondary SQL `COUNT(*)` pagination query.

---

## 💡 What to Investigate Before Optimization
Before approving any caching or code optimizations, an engineer must verify:
1. **SQL Execution Logging (`spring.jpa.show-sql=true`):** Count exact SQL queries generated per HTTP request to detect hidden N+1 queries.
2. **Database Indexing:** Ensure title searches and foreign key columns (`author_id`, `category_id`) are indexed.
3. **Single-Key vs Bulk Caching Suitability:** Determine whether caching is better applied to single-item lookups (`GET /api/books/{id}`) or search lists.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Performance measurement completed with concrete empirical evidence recorded.
- [x] Three API endpoints compared across repeated runs with warmup discarded.
- [x] Slowest endpoint and root cause bottleneck identified using architectural evidence.
- [x] Measurement plan executed strictly without modifying production code.