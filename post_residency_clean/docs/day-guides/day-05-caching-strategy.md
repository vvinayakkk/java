# Day 5 — Designing & Implementing a Caching Strategy

**Unit:** Cache with Purpose  
**Time:** ~2 hours  
**Depends on:** Day 4 slowest endpoint  
**Log section:** Guided Practice 5

---

## Goal

Decide whether caching is appropriate for the Day-4 slowest endpoint, design keys/TTL/invalidation, implement if justified, and measure before/after.

---

## Skip-video brief

### When caching helps

Caching helps when:

- Reads dominate writes
- Same keys repeat
- Computation/IO cost ≫ memory cost
- Stale data within TTL is acceptable

Caching hurts when:

- Data must always be fresh
- Key cardinality explodes (unique per request)
- You lack invalidation and correctness matters
- The bottleneck is elsewhere (e.g. huge payloads to client)

### Spring Cache abstraction

Enable with `@EnableCaching`. Annotate service methods:

| Annotation | Role |
|------------|------|
| `@Cacheable` | Return cached value if present; else run method and store |
| `@CachePut` | Always run method; update cache |
| `@CacheEvict` | Remove entries on write |

### Local vs distributed

| Approach | Use when |
|----------|----------|
| **No cache** | Evidence doesn’t support it |
| **Local** (`ConcurrentMap` / Caffeine) | Single instance lab / sticky low scale |
| **Distributed** (Redis) | Multi-instance, shared cache needed |

For this residency app (single local process): **local cache is the justified default**. Say so explicitly in the log.

### Cache-aside mental model

1. Look up key
2. On miss → load from DB → populate cache
3. On write → update DB → evict/update cache

**Optional deep links:** [Spring Cache](https://docs.spring.io/spring-framework/reference/integration/cache.html) · [Spring Boot Caching](https://docs.spring.io/spring-boot/reference/io/caching.html) · [Cache-aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

---

## Decision framework (fill in your Day-4 numbers)

| Question | Your answer |
|----------|-------------|
| Slowest endpoint? | |
| Avg latency? | |
| Is it read-heavy / repeatable keys? | |
| Freshness tolerance? | |
| Cache approach? | No / Local / Distributed |

---

## Recommended target (if list or by-id was slowest)

### Option A — cache by-id

- Method: `BookService.getBookById`
- Cache name: `books`
- Key: `#id`
- Evict on update/delete/create (create less critical for by-id)

### Option B — cache list first page

Harder because query params vary. Prefer caching **by-id** or a stable `getAvailableBooks` only if Day 4 says so.

If Day 4 slowest was full list **before** pagination, caching the entire list is a blunt instrument — mention that pagination may already be enough, and only cache if still slow.

---

## Implementation sketch (local cache)

### 1. Dependency

Spring Boot cache starter if not present:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

Optional Caffeine for TTL:

```xml
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
</dependency>
```

### 2. Enable

```java
@SpringBootApplication
@EnableCaching
public class BookstoreApplication { ... }
```

### 3. Simple config (ConcurrentMap)

```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("books");
    }
}
```

### 4. Service annotations

```java
@Cacheable(cacheNames = "books", key = "#id")
public BookDTO getBookById(Long id) { ... }

@CacheEvict(cacheNames = "books", key = "#id")
public BookDTO updateBook(Long id, BookDTO bookDTO) { ... }

@CacheEvict(cacheNames = "books", key = "#id")
public void deleteBook(Long id) { ... }

@CacheEvict(cacheNames = "books", allEntries = true)
public BookDTO createBook(BookDTO bookDTO) { ... }
```

Adjust if you cached a different method.

### 5. Properties (Caffeine example)

```properties
spring.cache.type=caffeine
spring.cache.cache-names=books
spring.cache.caffeine.spec=maximumSize=500,expireAfterWrite=60s
```

---

## Measure

Repeat Day-4 protocol on the cached endpoint:

| Phase | R1–R5 | Avg |
|-------|-------|-----|
| Before cache | from Day 4 | |
| After cache (warm) | | |

Expect first post-deploy call ≈ miss; subsequent calls faster if cache works.

---

## Production recommendation (template)

Pick one and justify:

- **Approve for prod** — only if multi-instance strategy, monitoring, and invalidation are addressed (likely **not** for bare ConcurrentMap).
- **Approve for single-instance / staging only**
- **Reject** — caching wrong layer; fix query/EAGER/pagination first

---

## What to record

Endpoint, evidence, decision, design, key, TTL, invalidation, before/after, trade-offs, production recommendation.

---

## Cursor prompts

```text
Challenge my cache key and invalidation plan for stale reads after updateBook.
What edge cases did I miss?
```

---

## Done checklist

- [ ] Caching appropriateness decided with evidence
- [ ] Design documented
- [ ] Implemented if appropriate
- [ ] Before/after measured
- [ ] Production recommendation written
- [ ] Practice log GP5 filled

**Next:** [`day-06-workflow-redesign.md`](day-06-workflow-redesign.md)
