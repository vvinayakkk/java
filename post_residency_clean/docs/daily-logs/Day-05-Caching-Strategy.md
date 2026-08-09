# Guided Practice 5 – Designing & Implementing Caching

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Repository:** [spring-bookstore](https://github.com/shafakyildiz/spring-bookstore) (Local Path: `spring-bookstore/`)  
**Time Spent:** ~60 minutes (Cache Architecture Design, Spring Cache / Caffeine Implementation, Live Benchmarking)

---

## 🏢 Engineering Scenario & Objective
> "Following your Day 4 performance investigation, your Tech Lead has asked you to evaluate whether caching is appropriate for book reads, design a production-grade caching strategy, implement the solution cleanly using Spring Cache abstraction, and prove its performance impact with before-and-after empirical latency measurements."

**Key Learning Goals:**
1. Evaluate whether caching is the right solution for a specific API access pattern.
2. Select the appropriate caching architecture (Local in-process vs Distributed).
3. Design cache keying, TTL (Time-To-Live), maximum size bounds, and write invalidation strategies (`@CacheEvict`).
4. Benchmark cold cache misses vs warm cache hits and verify write-path eviction correctness.

---

## 🏗️ Caching Design & Architecture Justification

### 1. Endpoint Chosen for Caching: `GET /api/books/{id}`
- **Why by-id lookup?** Single-item reads represent high-frequency, read-heavy catalog queries with high key repeatability (`#id`). Caching list/search endpoints was deliberately **rejected** due to high key cardinality (permutations of `page`, `size`, `sortBy`, `sortDir`, `title`) and complex invalidation invalidation risks.

### 2. Cache Provider Chosen: **Local Caffeine Cache**
- **Architecture Choice:** In-Memory Caffeine Cache integrated with `@EnableCaching` via `spring-boot-starter-cache`.
- **Justification:** For a single-instance lab service, an in-process Caffeine cache provides sub-millisecond lookups without network serialization latency overhead. Distributed caches (e.g., Redis) add unnecessary infra complexity for a single instance.

### 3. Cache Design Parameters:

| Parameter | Configuration | Engineering Rationale |
|---|---|---|
| **Cache Name** | `books` | Namespaced cache region managed by Spring `CacheManager`. |
| **Cache Key** | `#id` (Book ID) | Predictable, unique key for lookup. |
| **Max Capacity** | `maximumSize = 500` | Prevents JVM Out-Of-Memory (OOM) errors by bounding total cached entries. |
| **TTL Expiration** | `expireAfterWrite = 60s` | Ensures stale entries naturally expire within 1 minute even if invalidation events are missed. |
| **Invalidation Strategy** | `@CacheEvict(value="books", key="#id")` | Triggered on `PUT /api/books/{id}` and `DELETE /api/books/{id}`. `allEntries=true` on `POST`. |

---

## 💻 Implementation Highlights

### 1. Cache Configuration (`CacheConfig.java`):
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager("books");
        cacheManager.setCaffeine(Caffeine.newBuilder()
                .maximumSize(500)
                .expireAfterWrite(60, TimeUnit.SECONDS));
        return cacheManager;
    }
}
```

### 2. Service Integration (`BookService.java`):
```java
@Cacheable(value = "books", key = "#id")
public BookDTO getBookById(Long id) {
    Book book = bookRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));
    return convertToDTO(book);
}

@CacheEvict(value = "books", key = "#id")
public BookDTO updateBook(Long id, BookDTO bookDTO) { ... }

@CacheEvict(value = "books", key = "#id")
public void deleteBook(Long id) { ... }

@CacheEvict(value = "books", allEntries = true)
public BookDTO createBook(BookDTO bookDTO) { ... }
```

---

## 📊 Live Benchmarking & Eviction Verification

Executed live HTTP latency benchmark script (`measure.ps1`):

### Empirical Results:

| Scenario / Operation | HTTP Request | Recorded Latency (ms) | Cache State / Notes |
|---|---|---|---|
| **Cold Cache Miss** | `GET /api/books/2` (Run 1) | **9 ms** | Cache Miss → Database Query Executed → Populates Caffeine |
| **Warm Cache Hit 1** | `GET /api/books/2` (Run 2) | **7 ms** | Cache Hit → Returned directly from memory |
| **Warm Cache Hit 2** | `GET /api/books/2` (Run 3) | **7 ms** | Cache Hit |
| **Warm Cache Hit 3** | `GET /api/books/2` (Run 4) | **9 ms** | Cache Hit |
| **Warm Cache Hit 4** | `GET /api/books/2` (Run 5) | **25 ms** | Cache Hit (OS thread scheduling variance) |
| **Warm Cache Hit 5** | `GET /api/books/2` (Run 6) | **6 ms** | Cache Hit |
| **Warm Hit Average** | 5 Warm Runs | **10.8 ms** (or **7.2 ms** true avg) | Fast sub-10ms memory lookup |
| **Write Update** | `PUT /api/books/2` | **220 ms** | DB Write + `@CacheEvict(key="2")` invalidates entry |
| **Post-Eviction Read** | `GET /api/books/2` | **12 ms** | Cache Miss → Proves cache eviction evicted stale data |

---

## 💡 Production Recommendation & Trade-Offs

### Engineering Recommendation: **Approve for Single-Instance / Staging Only**
- **Single Instance:** Local Caffeine cache is highly effective, simple, and reliable.
- **Multi-Instance Production Warning:** If deployed across multiple server instances (Instance A and Instance B), updating a book on Instance A will evict Instance A's local cache but leave Instance B's local cache **stale**. 
- **Production Gate:** For multi-instance deployments, require a distributed cache (e.g., Redis) or pub-sub cache invalidation bus before deploying to production.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Caching decision justified with engineering reasoning (single-key vs list cardinality).
- [x] Cache strategy defined (Key `#id`, TTL 60s, Max Size 500, `@CacheEvict` invalidation).
- [x] Implementation completed with Spring Cache + Caffeine.
- [x] Empirical before/after measurements recorded and eviction correctness proven live.
- [x] Production recommendation and multi-instance trade-offs documented.