# Day 7 Artefact — Bookstore Incident Context

Use this as the evidence pack for Guided Practice 7. Treat it as what on-call handed you.

---

## Incident summary (given)

Over the past 24 hours, customer complaints increased. Users report **slow book reads** and **occasional create failures** following the latest deployment (caching + async catalog sync). Dashboards show elevated latency; root cause not yet identified.

**Tech Lead instruction:** Do **not** implement a fix yet. Investigate and recommend.

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| D-1 16:00 | PR merged: Spring Cache on `books` + `@Async` catalog sync |
| D-1 16:40 | Deployed to production (single instance → rolled to 2 instances behind LB) |
| D-1 17:15 | Cache hit ratio climbs to 88% on instance A; instance B starts cold |
| D-0 09:10 | Support: “Book detail sometimes shows old price after admin update” |
| D-0 10:05 | p95 `GET /api/books/{id}` up from 40ms → 180ms (noisy) |
| D-0 11:20 | Error spike: `RejectedExecutionException` on catalog-sync executor |
| D-0 12:00 | You begin investigation |

---

## Metrics snapshot

| Metric | Before deploy | Now |
|--------|---------------|-----|
| p50 GET by-id | 18ms | 22ms |
| p95 GET by-id | 40ms | 180ms |
| POST /api/books success rate | 99.9% | 97.2% |
| Catalog sync queue depth | n/a | 200–500 (spiky) |
| Cache hit % instance A | n/a | 88% |
| Cache hit % instance B | n/a | 41% |
| DB CPU | 22% | 25% |

---

## Log excerpts

```text
11:18:01 INFO  BookService - updateBook id=42 price=19.99
11:18:01 INFO  Cache - evict books::42 on instance A
11:18:44 INFO  BookController - GET /api/books/42 instance=B cache=HIT price=14.99
11:20:11 ERROR catalog-sync-2 - Task rejected from ThreadPoolTaskExecutor
11:20:11 ERROR BookService - Unexpected error during createBook: RejectedExecutionException
11:21:03 WARN  CatalogSyncService - Completed catalog sync for book id=9102 (delay 2400ms)
```

---

## Recent code behaviours (from Days 5–6)

- `@Cacheable` on `getBookById`; `@CacheEvict` on update/delete
- Local `ConcurrentMap` / Caffeine cache **per JVM** (not Redis)
- `CatalogSyncService.syncAfterCreate` runs `@Async` with small thread pool
- Sync still uses configured delay (simulating slow downstream)

---

## Constraints

- You may propose remediation in the report
- You must evaluate **≥3 hypotheses**
- Separate symptoms from root causes
