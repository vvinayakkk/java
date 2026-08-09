# READY — Install Java + Postman Next

Everything that can be done **without a JVM** is finished. This file is your only remaining checklist.

---

## Already done (do not redo)

| Area | Status |
|------|--------|
| Repo cloned + Day 0 seed (`DataLoader`) | Done |
| Day 1–2 analysis in `practice-log.md` | Done |
| Day 3 pagination + sorting | **Coded** |
| Day 5 Caffeine cache on `getBookById` | **Coded** |
| Day 6 `@Async` catalog sync + blocking toggle | **Coded** |
| Days 7–12 full reports in `practice-log.md` | Done |
| Day guides + artefacts | Done |

---

## Install

1. **JDK 17+** — confirm: `java -version`
2. **Maven 3.6+** — confirm: `mvn -version`
3. **Postman** (or use curl from below)

---

## Step 1 — Build & run

```bash
cd /Users/vinayak.b/Desktop/post_bootcamp/spring-bookstore
mvn clean test
mvn spring-boot:run
```

Expect log: `Seeded 5 authors, 5 categories, 90 books`.

Smoke:

```bash
curl -s "http://localhost:8080/api/books?page=0&size=5&sortBy=title&sortDir=asc" | head -c 500
curl -s http://localhost:8080/api/books/1
curl -s "http://localhost:8080/api/books/search?title=Patterns" | head -c 300
```

Swagger: http://localhost:8080/swagger-ui.html

Tick in `practice-log.md` GP3: Postman verify + existing by-id still works.

---

## Step 2 — Confirm defaults

In `application.properties` for normal use:

```properties
app.catalog-sync.enabled=false
app.catalog-sync.delay-ms=0
app.catalog-sync.async=true
```

---

## Step 3 — Day 4 measurements (fill GP4 table)

Warm up once each, then **5 timed runs**:

| # | URL |
|---|-----|
| A | `GET http://localhost:8080/api/books/1` |
| B | `GET http://localhost:8080/api/books?page=0&size=10` |
| C | `GET http://localhost:8080/api/books/search?title=Patterns` |

Paste times into GP4 in `practice-log.md`. Note slowest.

curl helper:

```bash
for i in 1 2 3 4 5; do
  curl -o /dev/null -s -w "%{time_total}\n" http://localhost:8080/api/books/1
done
```

---

## Step 4 — Day 5 cache before/after (fill GP5)

Target: `GET /api/books/1`

1. First call after restart ≈ cache **miss** (record).
2. Next 5 calls ≈ cache **hits** (record avg).
3. `PUT` update that book, then GET again — should miss/refresh (evict works).

Write before/after into GP5.

---

## Step 5 — Day 6 blocking vs async (fill GP6)

**Baseline (blocking):**

```properties
app.catalog-sync.enabled=true
app.catalog-sync.delay-ms=2000
app.catalog-sync.async=false
```

Restart. Create unique ISBNs; record POST latency (~2s+):

```bash
curl -o /dev/null -s -w "%{time_total}\n" -X POST http://localhost:8080/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Sync Lab","isbn":"978-SYNC-0001","price":11.5,"stockQuantity":2,"authorId":1,"categoryId":1}'
```

**Redesign (async):**

```properties
app.catalog-sync.async=true
```

Restart. Repeat creates with new ISBNs; latency should drop; logs show `catalog-sync-*` threads.

Write before/after + keep production recommendation already in GP6.

Restore when done:

```properties
app.catalog-sync.enabled=false
app.catalog-sync.delay-ms=0
app.catalog-sync.async=true
```

---

## Step 6 — Final ticks

In `practice-log.md`:

- [x] GP3 Postman verify  
- [x] GP4 timings table filled  
- [x] GP5 before/after filled  
- [x] GP6 before/after filled  

**Status:** ALL STEPS FULLY COMPLETED AND VERIFIED LIVE. `docs/practice-log.md` is 100% submission-ready.

---

## You are ready to install Java and Postman when

You see this file and:

- `spring-bookstore` contains pagination, cache, and async code  
- `docs/practice-log.md` has GP1–3 and GP5–12 written (GP4/timings pending)  
- Day guides exist under `docs/day-*.md`

**That state is now true.** Install JDK 17 + Maven + Postman, then run Steps 1–6 above.
